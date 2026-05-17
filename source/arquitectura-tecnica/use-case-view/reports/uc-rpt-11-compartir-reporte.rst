.. meta::
 :artefacto: AT_UC_RPT_11_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_rpt_11_compartir_reporte:

==============================
UC_RPT_11 — Compartir Reporte
==============================

Owner comparte SavedView con otro User, AccessGroup o public-segment.
Receptor accede a la vista pero ejecuta queries con SU propio scope
(CNST-008 isolation preservada). ``share_reports``. AuditEvent
VIEW_SHARED.

.. uml::
 :caption: UC_RPT_11 — actores y casos asociados.

 @startuml

 left to right direction

 actor "share_reports" as share_reports
 actor "Receptor User/AGR" as Receptor <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SavedView" as SavedView <<sistema>>
 actor "AccessGroup" as AccessGroup <<sistema>>
 actor "User" as User <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_11\nCompartir Reporte\n(SavedView)" as UC_RPT_11
   usecase "Verificar\nshare_reports" as VERIFICAR_AGR
   usecase "Validar ownership\n(actor_id == owner)" as OWNER
   usecase "Validar receptor\n(user|AGR|public-segment)" as RECEPTOR_VAL
   usecase "Validar isolation\n(receptor en segmento)" as ISOLATION
   usecase "Persistir Share\nen SavedView.shared_with" as PERSIST
   usecase "Emitir AuditEvent\nVIEW_SHARED" as AUDITAR
 }

 share_reports --> UC_RPT_11

 UC_RPT_11 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_11 ..> OWNER : <<include>>
 UC_RPT_11 ..> RECEPTOR_VAL : <<include>>
 UC_RPT_11 ..> ISOLATION : <<include>>
 UC_RPT_11 ..> PERSIST : <<include>>
 UC_RPT_11 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 OWNER --> SavedView
 RECEPTOR_VAL --> AccessGroup
 RECEPTOR_VAL --> User
 ISOLATION --> SegmentResolver
 PERSIST --> SavedView
 PERSIST --> Receptor
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of ISOLATION
   CNST-008: receptor accede a la
   vista pero ejecuta consultas con
   SU propio scope de segmentos —
   data isolation preservada.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/saved-view` —
   SavedView con shared_with.
 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AGR target en share.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   User target.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   isolation.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor VIEW_SHARED.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-11/index` —
   spec textual.
