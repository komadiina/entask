import asyncio
import logging
import os
from typing import Any, Dict, Optional

import httpx
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Request, Response
from models.payloads import HeartbeatPayload, RegisterPayload

REDIS_HOST = os.getenv("G_REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("G_REDIS_PORT", 6380)
REDIS_INDEX = os.getenv("G_REDIS_INDEX", 0)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_INDEX}"
HEARTBEAT_TTL = 30
REGISTRY_PREFIX = "registry"  # hash: registry:{service} => {instance_id: lb_url}
HEARTBEAT_PREFIX = "heartbeat"  # key: heartbeat:{service}:{instance_id} -> 1 (EX TTL)

app = FastAPI()
r = redis.from_url(REDIS_URL, decode_responses=True)
logger = logging.getLogger(__name__)

# round-robin
counters: Dict[str, int] = {}
locks: Dict[str, asyncio.Lock] = {}


@app.post("/register", status_code=201)
async def register(p: RegisterPayload) -> Dict[str, Any]:
    reg_key = f"{REGISTRY_PREFIX}:{p.service}"
    hb_key = f"{HEARTBEAT_PREFIX}:{p.service}:{p.instance_id}"

    await r.hset(reg_key, p.instance_id, p.load_balancer_url)
    await r.set(hb_key, "1", ex=HEARTBEAT_TTL)

    locks.setdefault(p.service, asyncio.Lock())
    counters.setdefault(p.service, 0)

    return {"ok": True}


@app.post("/heartbeat", status_code=200)
async def heartbeat(p: HeartbeatPayload) -> Dict[str, Any]:
    hb_key = f"{HEARTBEAT_PREFIX}:{p.service}:{p.instance_id}"
    exists = await r.exists(hb_key)

    if not exists:
        raise HTTPException(status_code=404, detail="instance not registered")

    await r.expire(hb_key, HEARTBEAT_TTL)

    return {"ok": True}


async def get_alive_instances(service: str) -> Dict[str, str]:
    reg_key = f"{REGISTRY_PREFIX}:{service}"
    entries = await r.hgetall(reg_key)  # instance_id -> lb_url
    alive: Dict[str, str] = {}

    for uuid, url in entries.items():
        hb_key = f"{HEARTBEAT_PREFIX}:{service}:{uuid}"
        if await r.exists(hb_key):
            alive[uuid] = url
        else:
            # stale entry
            pass

    return alive


async def choose_instance(service: str) -> Optional[str]:
    alive = await get_alive_instances(service)
    if not alive:
        return None

    # round-robin by sorted instance list to keep deterministic order
    ids = sorted(alive.keys())
    lock = locks.setdefault(service, asyncio.Lock())

    async with lock:
        idx = counters.setdefault(service, 0)
        url = alive[ids[idx % len(ids)]]
        counters[service] = (idx + 1) % len(ids)

    return url


# proxy: forwards method, headers, body to chosen lb_url + path, all methods must be allowed
@app.api_route(
    "/proxy/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
)
async def proxy(service: str, path: str, request: Request) -> Response:
    target = await choose_instance(service)
    resp = None

    if not target:
        raise HTTPException(status_code=503, detail="service unavailable")

    # build target url
    target_url = f"{target.rstrip('/')}/{path.lstrip('/')}"

    # forward request
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            content = await request.body()

            headers = dict(request.headers)
            headers.pop("host", None)

            resp = await client.request(
                request.method,
                target_url,
                headers=headers,
                content=content,
                params=dict(request.query_params),
            )
        except RuntimeError as e:
            logger.error(f"RequestRouter RuntimeError: {e}")
        except Exception as e:
            logger.exception(f"RequestRouter Exception: {e}")
        finally:
            await client.aclose()

    # build response back to caller
    if resp is not None:
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers={
                k: v
                for k, v in resp.headers.items()
                if k.lower()
                not in ("content-encoding", "transfer-encoding", "connection")
            },
            media_type=resp.headers.get("content-type"),
        )

    raise HTTPException(status_code=503, detail="service unavailable")


@app.get("/services/{service}/instances")
async def list_instances(service: str) -> Dict[str, Any]:
    alive = await get_alive_instances(service)
    return {"instances": alive}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=int(os.getenv("G_ROUTER_PORT", 8080)),
        reload=False,
    )
