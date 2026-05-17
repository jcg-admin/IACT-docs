8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 actor "view_reports" as USUARIO_VER_REPORTES
 rectangle "MOD_Reports" {
   usecase "UC_RPT_12\nReporte Agentes" as UC12
   usecase "Detalle agente" as VistaDetalle
 }
 view_reports --> UC12
 USUARIO_VER_REPORTES --> DET
 UC12 ..> DET : <<extend>>
 @enduml

