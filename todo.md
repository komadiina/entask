- Dapr Workflow:
  - pubsub, statestore
  - atomicize workflows into durable atomic tasks - abort/pause/continue
    - interrupts are signaled to a topic via a unique **token**
- Implement ClientNotifier service
  - communicates with frontend webapp via websockets using (client_id), sending:
```py
# /services/notifier/routers/notify.py
# service receives: {data: any}, client_id from pathparam on http:// POST
# service sends: {message: string, client_id: string, status: string | enum, data: any} on ws://../notify/client

# service receives {signal: str | enum, conversion_token: str}, client_id from pathparam, on ws://../conversion/ws -> 
#   -> forwards the ws message to dapr
# service sends: {message: string, client_id: string, status: string | enum, data: any} on ws://../conversions/ws`
```

:
```ts
// notifications (/services/notifier/routers/notify.py)
export interface WSNotificationOut { // SEND ws:// (from client to notifier service)
  data: any; // could be templated but idc
}

export interface WSNotificationIn { // POST /notify/client/{client_id} (from XYZ service to client)
  message: string;
  clientId: string;
  status: string;
  data: any;
}

// workflow interrupts (/converters/**/routers/*.py -> POST /notifier/notify/client/{client_id} -> client)
export interface WSWorkflowInterruptOut { // SEND ws://..//converter/*/interrupts (from client to XYZ converter)
  signal: string;
  conversionToken: string;
}

export interface WSWorkflowInterruptIn { // POST /notify/client/{client_id} (from XYZ service to client)
  message: string;
  status: string;
  clientId: string;
  data: any
}
```
