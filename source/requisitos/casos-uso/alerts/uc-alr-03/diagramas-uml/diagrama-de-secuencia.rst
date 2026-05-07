.. _uc-alr-03-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_ALR_03 — acknowledge dentro de transaccion.

 @startuml

 actor "acknowledge_alert" as acknowledge_alert
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "AlertRepo" as AlertRepo
 participant "AuditService" as AuditService

 acknowledge_alert -> SvcAplicacion: POST /api/v1/alerts/{id}/ack/
 SvcAplicacion -> SvcAplicacion: verificar capability\nacknowledge_alert (cache)
 SvcAplicacion -> AlertRepo: load Alert by id

 group Transaccion atomica
   SvcAplicacion -> AlertRepo: UPDATE Alert\n  SET state='acknowledged',\n      ack_by, ack_at
   SvcAplicacion -> AuditService: emit ALERT_ACKNOWLEDGED
 end

 SvcAplicacion -> SvcAplicacion: suprimir notificaciones
 SvcAplicacion --> acknowledge_alert: 200 OK

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-actividad`.
 - :doc:`/arquitectura-tecnica/domain-model/alert`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`.
