8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_11 — actores y casos asociados

 @startuml

 left to right direction

 actor "share_reports" as INVOKER
 actor "Receptor User/AGR" as RECEPTOR <<beneficiario>>
 actor "ReportShareRepo" as REPO <<sistema>>
 actor "AuditService" as AUDITS <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_11\nCompartir Reporte\n(SavedView)" as UC_RPT_11
   usecase "Validar ownership\n(actor_id == owner)" as OWNER
   usecase "Validar receptor\n(user|AGR|public-segment)" as RECEPTOR_VAL
   usecase "Validar isolation\n(receptor en segmento)" as ISOLATION
   usecase "Persistir Share" as PERSIST
   usecase "AuditEvent\nVIEW_SHARED" as AUDIT
 }

 INVOKER --> UC_RPT_11
 UC_RPT_11 ..> OWNER : <<include>>
 UC_RPT_11 ..> RECEPTOR_VAL : <<include>>
 UC_RPT_11 ..> ISOLATION : <<include>>
 UC_RPT_11 ..> PERSIST : <<include>>
 UC_RPT_11 ..> AUDIT : <<include>>

 PERSIST --> REPO
 PERSIST --> RECEPTOR
 AUDIT --> AUDITS
 AUDITS --> view_audit_log

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
