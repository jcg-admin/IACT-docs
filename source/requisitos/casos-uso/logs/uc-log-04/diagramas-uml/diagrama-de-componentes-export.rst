.. _uc-log-04-parte-08-diagrama-componentes-export:

8.3 Diagrama de componentes — Exportacion
============================================

.. uml::
 :caption: UC_LOG_04 — pipeline de exportacion asincrona.

 @startuml

 actor     "export_logs" as export_logs
 component "Servicio de Aplicacion" as SvcAplicacion
 component "ExportWorker (async)" as ExportWorker
 database  "LogStore" as LogStore
 component "InternalMailbox" as InternalMailbox

 export_logs --> SvcAplicacion : POST /export/
 SvcAplicacion --> ExportWorker : encolar job
 ExportWorker --> LogStore : query rango
 LogStore --> ExportWorker : entries
 ExportWorker --> InternalMailbox : adjuntar archivo
 InternalMailbox --> export_logs : notificar disponibilidad

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/export-job`.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`.
