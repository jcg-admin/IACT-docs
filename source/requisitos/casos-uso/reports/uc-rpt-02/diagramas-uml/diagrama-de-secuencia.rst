8.3 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_RPT_02 — SSE

 @startuml

 actor "User" as User
 participant "Frontend" as Frontend
 participant "StreamGateway" as Streamgateway
 participant "Subscriber" as Subscriber
 queue "AnalyticsStream" as AnalyticsStream
 participant "AuditService" as Auditservice

 User -> Frontend: abrir vista realtime
 Frontend -> Streamgateway: GET /realtime (SSE)
 Streamgateway -> Streamgateway: JWT + RBAC + segmento
 Streamgateway -> Auditservice: emit STREAM_OPENED
 Streamgateway -> Subscriber: subscribe(segments)
 Subscriber -> AnalyticsStream: subscribe(topics)

 loop hasta cierre
   AnalyticsStream -> Subscriber: event
   Subscriber -> Streamgateway: snapshot (throttled)
   Streamgateway -> Frontend: data: {...}
 end

 User -> Frontend: cerrar
 Frontend -> Streamgateway: close
 Streamgateway -> Subscriber: unsubscribe
 Streamgateway -> Auditservice: emit STREAM_CLOSED

 @enduml

