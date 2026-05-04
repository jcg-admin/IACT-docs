8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_16\nReporte Menus IVR" as UC16
   usecase "Ver menus redirigidos" as VerMenusRedirigidos
   usecase "Ver errores de menu" as VerErroresDeMenu
 }
 view_reports --> UC16
 UC16 ..> INC : <<include>>
 UC16 ..> VerMenusRedirigidos : <<extend>>
 UC16 ..> VerErroresDeMenu : <<extend>>
 @enduml

