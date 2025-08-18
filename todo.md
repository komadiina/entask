- Implement RR (round-robin) load balancers:
  - LB's register at RequestRouter Redis registry
  - API services register at their respective LoadBalancer Redis service registry
  - finish up AuthService as a whole, test, and then develop other services 
    - (user-details service, history service, s3-upload service (MinIO - s3-compatible object-store)) 
- Implement NATS (JetStream) message broker 
  - sends notifications on:
    - produce
    - consume
    - DaprWorkflowTaskEvent (update, finish)
- Dapr Workflow:
  - pubsub, statestore
  - atomicize workflows into durable atomic tasks - abort/pause/continue
    - interrupts are signaled to a topic via a unique **token**
- Implement ClientNotifier service
  - communicates with frontend webapp via websockets using (client_id), sending:
```json
  {
    message: {
      summary: '', 
      detail: '', 
      type: ''
    }, 
    metadata: {...}, 
    client_id: '',
    notifier_id: ''
  }
```