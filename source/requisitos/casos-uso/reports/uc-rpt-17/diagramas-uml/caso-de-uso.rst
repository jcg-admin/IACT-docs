8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_17\nClientes Unicos IVR" as UC17
 }
 view_reports --> UC17
 UC17 ..> INC : <<include>>
 @enduml

