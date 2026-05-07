.. _uc-log-05-parte-08-diagrama-secuencia-tail-sse:

8.4 Diagrama de secuencia — Consulta con tail SSE
===================================================

.. uml::
 :caption: UC_LOG_05 — flujo con tail SSE opcional.

 @startuml

 actor "view_infrastructure_logs" as view_infrastructure_logs
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "InfraLogStore" as InfraLogStore

 view_infrastructure_logs -> SvcAplicacion : GET /api/v1/logs/infra/?host=app&severity=ERROR
 SvcAplicacion -> SvcAplicacion : verificar capability
 alt sin permiso
   SvcAplicacion --> view_infrastructure_logs : 403 Forbidden
 else con permiso
   SvcAplicacion -> InfraLogStore : query WHERE host AND severity
   InfraLogStore --> SvcAplicacion : entries
   SvcAplicacion --> view_infrastructure_logs : 200 + logs
   opt tail SSE solicitado
     loop nuevas entradas
       InfraLogStore -> SvcAplicacion : new entry
       SvcAplicacion -> view_infrastructure_logs : SSE data event
     end
   end
 end

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/infra-log-store`.
 - :doc:`/arquitectura-tecnica/domain-model/infrastructure-log`.
