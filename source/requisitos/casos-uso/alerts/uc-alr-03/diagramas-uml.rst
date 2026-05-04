.. _uc-alr-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "acknowledge_alert" as acknowledge_alert
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_03\nReconocer" as UC03
   usecase "Bulk ack" as BulkAck
 }
 acknowledge_alert --> UC03
 acknowledge_alert --> BulkAck
 BulkAck ..> UC03 : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST /alerts/{id}/ack/;
 :JWT + RBAC;
 :Cargar Alert;
 if (Cross-segmento?) then (si)
   :403; stop
 endif
 if (state != firing?) then (si)
   :409; stop
 endif
 :BEGIN tx;
 :UPDATE Alert state, ack_*;
 :Audit ALERT_ACKNOWLEDGED;
 :COMMIT;
 :Suprimir notify;
 :200;
 stop
 @enduml

8.3 Estado (transicion)
=======================

.. uml::

 @startuml
 [*] --> firing
 firing --> acknowledged : ack
 acknowledged --> resolved : metric normal
 firing --> resolved : metric normal
 resolved --> closed
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "acknowledge_alert" as acknowledge_alert
 participant "Endpoint" as Endpoint
 database "AlertRepo" as Alertrepo
 participant "AuditSvc" as Auditsvc

 acknowledge_alert -> Endpoint: POST ack
 Endpoint -> Endpoint: JWT + RBAC + scope
 Endpoint -> Alertrepo: BEGIN
 Endpoint -> Alertrepo: UPDATE Alert
 Endpoint -> Auditsvc: emit ALERT_ACKNOWLEDGED
 Endpoint -> Alertrepo: COMMIT
 Endpoint --> acknowledge_alert: 200
 @enduml
