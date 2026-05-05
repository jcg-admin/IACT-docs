8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_INC_RPT_01 — UC de inclusion (segment resolver)

 @startuml

 left to right direction

 actor "Caller UC\n(UC_RPT_01..17)" as CALLER_UC <<sistema>>
 actor "PermissionService" as PS <<sistema>>
 actor "SegmentResolver" as SR <<sistema>>

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

 CONSULTAR --> PS
 LISTAR --> SR
 ISOLATION --> SR

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

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   componente principal del resolver.
 - :doc:`/arquitectura-tecnica/domain-model/permission-service` —
   verifica funciones view_*_reports del User.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   entidad User cuyos segmentos se resuelven.
