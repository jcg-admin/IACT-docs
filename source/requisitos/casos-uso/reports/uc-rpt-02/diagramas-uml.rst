.. _uc-rpt-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_02 — realtime

 @startuml
 left to right direction

 actor "view_kpis" as view_kpis
 actor "AnalyticsStream" as Analyticsstream

 rectangle "MOD_Reports" {
   usecase "UC_RPT_02\nRealtime Metrics" as UC02
   usecase "Suscribir stream" as SUB
   usecase "Throttle" as Throttle
   usecase "Heartbeat" as Heartbeat
 }

 view_kpis --> UC02
 UC02 ..> SUB : <<include>>
 UC02 ..> Throttle : <<include>>
 UC02 ..> Heartbeat : <<include>>
 SUB --> Analyticsstream

 note bottom
   Stream push via SSE / WS / poll.
   Reconnect via Last-Event-ID.
 end note

 @enduml

8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_02 — flujo

 @startuml

 start
 :Frontend abre conexion stream;
 if (JWT?) then (no)
   :401; stop
 endif
 if (view_kpis?) then (no)
   :403 + audit; stop
 endif
 if (Sin segmento?) then (si)
   :400; stop
 endif
 :Suscribir a AnalyticsStream
  con filtro segmento;
 :Audit REALTIME_STREAM_OPENED;

 while (Conexion abierta?)
   if (Evento del stream?) then (si)
     :Construir snapshot;
     :Throttle 1/5s;
     :Emit event: metrics;
   else (no)
     if (>= 30s sin data?) then (si)
       :Emit event: heartbeat;
     endif
   endif
 endwhile

 :Audit REALTIME_STREAM_CLOSED;
 :Limpieza;
 stop

 @enduml

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

8.4 Diagrama de estado
======================

.. uml::
 :caption: Estado de conexion

 @startuml
 [*] --> Handshake
 Handshake --> Authorized : ok
 Handshake --> Closed : 401/403
 Authorized --> Streaming : suscrito
 Streaming --> Streaming : event / heartbeat
 Streaming --> Reconnecting : red caida
 Reconnecting --> Streaming : recuperado
 Reconnecting --> Closed : timeout
 Streaming --> Closed : user close
 Closed --> [*]
 @enduml
