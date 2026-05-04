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
 Endpoint -> Alertrepo: actualizar Alert
 Endpoint -> Auditsvc: emit ALERT_ACKNOWLEDGED
 Endpoint -> Alertrepo: COMMIT
 Endpoint --> acknowledge_alert: 200
 @enduml
