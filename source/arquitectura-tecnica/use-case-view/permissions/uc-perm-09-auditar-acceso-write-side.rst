.. meta::
 :artefacto: AT_UC_PERM_09_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_perm_09_auditar_acceso_write_side:

==============================================
UC_PERM_09 — Auditar Acceso (write side)
==============================================

UC interno que emite ``AuditEvent`` desde TODA escritura RBAC de los
otros UCs (UC_ACC_01..09, UC_PERM_*, UC_ADM_*). NO tiene endpoint
ni RBAC propio — es invocado internamente por servicios. Garantiza
P-39 / CNST-025 inmutabilidad y trazabilidad. Side effect transversal.

.. uml::
 :caption: UC_PERM_09 — actores y casos asociados (UC interno).

 @startuml

 left to right direction

 actor "Caller UC interno\n(UC_ACC_*, UC_PERM_*, UC_ADM_*)" as Caller_UC <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuditService" as AuditService <<sistema>>
 actor "AuditValidator" as AuditValidator <<sistema>>
 actor "PIIScanner" as PIIScanner <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>
 actor "AuditRepo" as AuditRepo <<sistema>>
 actor "AlertHook" as AlertHook <<sistema>>

 rectangle "MOD_Permissions (interno)" {
   usecase "UC_PERM_09\nAuditar Acceso\n(write side)" as UC_PERM_09
   usecase "Validar payload\nrequerido (event_type,\nactor, target, payload, ctx)" as VALIDAR_PAYLOAD
   usecase "Sanitize PII\n(CNST-026)" as SANITIZAR
   usecase "Persistir AuditEvent\n(append-only CNST-025)" as PERSISTIR
   usecase "Trigger alertas\n(eventos criticos)" as TRIGGER_ALR
 }

 Caller_UC --> UC_PERM_09

 UC_PERM_09 ..> VALIDAR_PAYLOAD : <<include>>
 UC_PERM_09 ..> SANITIZAR : <<include>>
 UC_PERM_09 ..> PERSISTIR : <<include>>
 UC_PERM_09 ..> TRIGGER_ALR : <<include>>

 VALIDAR_PAYLOAD --> AuditValidator
 SANITIZAR --> PIIScanner
 SANITIZAR --> Sanitizer
 PERSISTIR --> AuditRepo
 PERSISTIR --> AuditService
 TRIGGER_ALR --> AlertHook
 AuditService --> view_audit_log

 note bottom of UC_PERM_09
   UC INTERNO sin endpoint. Invocado
   por todo write-side RBAC. Garantiza
   P-39 / CNST-025 inmutabilidad.
   No DELETE, no UPDATE.
 end note

 note bottom of TRIGGER_ALR
   Eventos criticos (FAILED_LOGIN
   x N, EXCEPTIONAL_GRANTED, etc.)
   disparan AlertHook → alerta.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura inmutable.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   servicio orquestador.
 - :doc:`/arquitectura-tecnica/domain-model/audit-validator` —
   valida payload requerido.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   append-only persist.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner` —
   detector PII.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   reemplaza PII detectada.
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook` —
   trigger de alertas en eventos criticos.
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-09/index` —
   spec textual.
