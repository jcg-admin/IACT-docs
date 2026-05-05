8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_INC_RPT_01 — UC de inclusion (segment resolver)

 @startuml

 left to right direction

 actor "Caller UC\n(UC_RPT_01..17)" as CALLER_UC <<sistema>>
 actor "PermissionService" as PERM <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento\ndel Usuario" as UC_INC_RPT_01
   usecase "Consultar funciones\nview_*_reports del User" as CONSULTAR
   usecase "Listar segmentos\naccesibles" as LISTAR
   usecase "Aplicar isolation\nCNST-008" as ISOLATION
 }

 CALLER_UC --> UC_INC_RPT_01

 UC_INC_RPT_01 ..> CONSULTAR : <<include>>
 UC_INC_RPT_01 ..> LISTAR : <<include>>
 UC_INC_RPT_01 ..> ISOLATION : <<include>>

 CONSULTAR --> PERM

 note bottom of UC_INC_RPT_01
   UC de inclusion — no se ejecuta
   independientemente. Es incluido
   por TODOS los UC_RPT_01..17 para
   limitar el scope de datos a los
   segmentos accesibles del User.
 end note

 note bottom of ISOLATION
   CNST-008: cada User solo ve datos
   de los segmentos a los que tiene
   acceso. Out-of-segment retorna
   vacio (sin error 403).
 end note

 @enduml
