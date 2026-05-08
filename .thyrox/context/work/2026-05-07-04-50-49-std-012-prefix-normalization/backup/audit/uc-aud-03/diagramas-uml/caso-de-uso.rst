8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "export_audit_log" as export_audit_log
 actor "ExportWorker" as Exportworker
 actor "InternalMailbox" as Internalmailbox
 rectangle "MOD_Audit" {
   usecase "UC_AUD_03\nExportar Audit Log" as UC_AUD_03
   usecase "Seleccionar\nperiodo y filtros" as VistaSeleccion
   usecase "Notificar\nvia Mailbox" as NotificacionMailbox
 }
 export_audit_log --> UC_AUD_03
 UC_AUD_03 ..> SEL : <<extend>>
 UC_AUD_03 ..> Exportworker : <<include>>
 Exportworker ..> NOT : <<include>>
 NOT --> Internalmailbox
 @enduml

