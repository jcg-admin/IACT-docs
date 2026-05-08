8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_11 — actores y casos asociados

 @startuml

 left to right direction

 actor "share_reports" as INVOKER
 actor "Receptor User/AGR" as RECEPTOR <<beneficiario>>
 actor "SavedView" as SV <<sistema>>
 actor "AccessGroup" as AG <<sistema>>
 actor "AuditService" as AS <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_11\nCompartir Reporte\n(SavedView)" as UC_RPT_11
   usecase "Validar ownership\n(actor_id == owner)" as OWNER
   usecase "Validar receptor\n(user|AGR|public-segment)" as RECEPTOR_VAL
   usecase "Validar isolation\n(receptor en segmento)" as ISOLATION
   usecase "Persistir Share\nen SavedView.shared_with" as PERSIST
   usecase "Emitir AuditEvent\nVIEW_SHARED" as AUDIT
 }

 INVOKER --> UC_RPT_11
 UC_RPT_11 ..> OWNER : <<include>>
 UC_RPT_11 ..> RECEPTOR_VAL : <<include>>
 UC_RPT_11 ..> ISOLATION : <<include>>
 UC_RPT_11 ..> PERSIST : <<include>>
 UC_RPT_11 ..> AUDIT : <<include>>

 PERSIST --> SV
 RECEPTOR_VAL --> AG
 PERSIST --> RECEPTOR
 AUDIT --> AS
 AS --> view_audit_log

 note bottom of RECEPTOR_VAL
   Tipos de share: (a) User-to-User,
   (b) User-to-AGR (todos con AGR
   ven la vista), (c) Public dentro
   del segmento del owner.
 end note

 note bottom of ISOLATION
   CNST-008: receptor accede a la
   vista pero ejecuta consultas con
   SU propio scope de segmentos —
   data isolation se preserva.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/saved-view` —
   SavedView con campo shared_with (lista de targets).
 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroup destino en share type=AGR.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   User destino en share type=User-to-User.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   verifica isolation de scope (CNST-008).
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent VIEW_SHARED.
