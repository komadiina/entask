from pydantic import BaseModel


class RegisterPayload(BaseModel):
  service: str
  instance_id: str
  load_balancer_url: str
  

class HeartbeatPayload(BaseModel):
  service: str
  instance_id: str