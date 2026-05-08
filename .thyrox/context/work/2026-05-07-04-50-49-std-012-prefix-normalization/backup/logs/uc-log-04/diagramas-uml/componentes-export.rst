8.3 Componentes export
=======================

.. uml::

 @startuml
 actor "export_logs" as export_logs
 component "LogExportEndpoint" as Logexportendpoint
 component "ExportWorker\n(async)" as Exportworker
 database "LogStore" as Logstore
 component "InternalMailbox" as Internalmailbox

 export_logs --> Logexportendpoint : POST /logs/export/
 Logexportendpoint --> Exportworker : encolar job
 Exportworker --> Logstore : leer rango
 Logstore --> Exportworker : entries
 Exportworker --> Internalmailbox : entregar archivo
 Internalmailbox --> export_logs : notificacion
 @enduml

