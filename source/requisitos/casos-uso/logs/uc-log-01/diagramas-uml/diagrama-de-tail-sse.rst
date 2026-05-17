.. _uc-log-01-parte-08-diagrama-tail-sse:

8.4 Diagrama de tail con SSE
=============================

.. uml::
 :caption: UC_LOG_01 — tail en tiempo real con Server-Sent Events.

 @startuml

 actor "view_application_logs" as view_application_logs
 participant "Servicio de Aplicacion" as SvcAplicacion
 queue       "LogStore" as LogStore

 view_application_logs -> SvcAplicacion: GET /api/v1/logs/system/tail (SSE)

 loop tail continuo
   LogStore -> SvcAplicacion: nueva entry
   SvcAplicacion -> view_application_logs: data: { entry }
 end

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/application-log`.
