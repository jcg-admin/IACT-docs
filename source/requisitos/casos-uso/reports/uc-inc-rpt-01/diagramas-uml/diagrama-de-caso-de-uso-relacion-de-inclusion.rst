.. _uc-inc-rpt-01-parte-08-diagrama-caso-de-uso-relacion-inclusion:

8.1 Diagrama de caso de uso — Relacion de inclusion
=====================================================

.. uml::
 :caption: UC_INC_RPT_01 — UC de inclusion consumido por todos los UC_RPT_*.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "RBACRepo" as RBACRepo <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_NN\n(cualquier reporte)" as UC_RPT_GENERICO
   usecase "UC_INC_RPT_01\nResolver Segmento" as UC_INC_RPT_01
 }

 view_reports --> UC_RPT_GENERICO
 UC_RPT_GENERICO ..> UC_INC_RPT_01 : <<include>>
 UC_INC_RPT_01 --> SegmentResolver
 SegmentResolver --> RBACRepo

 note bottom of UC_INC_RPT_01
   UC de inclusion: NO se ejecuta
   independiente. Es invocado por
   UC_RPT_01..UC_RPT_17 antes de
   cualquier query a la Base
   Analitica IVR.
 end note

 @enduml

.. seealso::

 - :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/index`.
 - :doc:`/requisitos/reglas-negocio/br-012-usuario-segmento-unico`.
