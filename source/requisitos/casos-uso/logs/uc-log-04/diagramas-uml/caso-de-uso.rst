8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "export_logs" as export_logs
 actor "ExportWorker" as Exportworker
 actor "InternalMailbox" as Internalmailbox
 rectangle "MOD_Logs" {
   usecase "UC_LOG_04\nExportar Logs" as UC_LOG_04
   usecase "Seleccionar\nrango y formato" as VistaSeleccion
   usecase "Notificar\nvia Mailbox" as NotificacionMailbox
 }
 export_logs --> UC_LOG_04
 UC_LOG_04 ..> SEL : <<extend>>
 UC_LOG_04 ..> Exportworker : <<include>>
 Exportworker ..> NOT : <<include>>
 NOT --> Internalmailbox
 @enduml

