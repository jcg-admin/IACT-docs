.. meta::
 :artefacto: AT_UC_INC_RPT_01_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_inc_rpt_01_resolver_segmento:

==============================================
UC_INC_RPT_01 — Resolver Segmento del Usuario
==============================================

UC de inclusion. NO se ejecuta independientemente — incluido por
TODOS los UC_RPT_01..17 para limitar scope de datos a segmentos
accesibles del User. CNST-008 isolation: out-of-segment retorna
vacio sin error 403.

.. uml::
 :caption: UC_INC_RPT_01 — UC de inclusion (segment resolver).

 @startuml

 left to right direction

 actor "Caller UC (UC_RPT_01..17)" as Caller_UC <<sistema>>
 actor "PermissionService" as PermissionService <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "User" as User <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento\ndel Usuario" as UC_INC_RPT_01
   usecase "Consultar funciones\nview_*_reports del User" as CONSULTAR
   usecase "Listar segmentos\naccesibles" as LISTAR
   usecase "Aplicar isolation\n(CNST-008)" as ISOLATION
 }

 Caller_UC --> UC_INC_RPT_01

 UC_INC_RPT_01 ..> CONSULTAR : <<include>>
 UC_INC_RPT_01 ..> LISTAR : <<include>>
 UC_INC_RPT_01 ..> ISOLATION : <<include>>

 CONSULTAR --> PermissionService
 LISTAR --> SegmentResolver
 ISOLATION --> SegmentResolver
 PermissionService --> User

 note bottom of UC_INC_RPT_01
   UC de inclusion — no aparece
   solo. Incluido por TODOS los
   UC_RPT_01..17 para limitar
   scope de datos.
 end note

 note bottom of ISOLATION
   CNST-008: cada User solo ve datos
   de los segmentos a los que tiene
   acceso. Out-of-segment → vacio
   (sin error 403).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   componente principal.
 - :doc:`/arquitectura-tecnica/domain-model/permission-service` —
   verifica funciones view_*_reports.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   entity cuyos segmentos se resuelven.
 - :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/index` —
   spec textual.
