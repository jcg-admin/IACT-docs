.. meta::
 :artefacto: AT_DM_CLASS_AUDIT_VALIDATOR
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_audit_validator:

==============
AuditValidator
==============

Componente que valida la estructura y el contenido de un
``AuditEvent`` antes de persistirlo. Encapsula las reglas de
forma del evento (campos requeridos, tamaños máximos, tipos
válidos) y la verificación de que ``actor_user_id`` y
``event_type`` sean coherentes con el ``target_entity_type``.

Es invocado por ``AuditService.emit()`` antes de delegar la
escritura a ``AuditRepo.append()``. Si la validación falla, el
flujo del UC invocante hace ROLLBACK (P-09 audit-or-abort,
:doc:`/requisitos/casos-uso/permissions/uc-perm-09/index`).

.. uml::
 :caption: Clase AuditValidator — gate de admisibilidad de
           eventos antes de persistir (CNST-025, P-09).

 @startuml

 class AuditValidator {
   - schema_version : Integer
   - max_details_size_bytes : Integer
   - allowed_event_types : Set<EventType>
   - allowed_target_types : Set<String>
   --
   + validate(event : AuditEvent) : ValidationResult
   + validate_required_fields(event : AuditEvent) : List<String>
   + validate_event_type_consistency(event : AuditEvent) : Boolean
   + validate_actor_exists(actor_user_id : UUID) : Boolean
   + validate_target_entity(target_entity_type : String, \
                             target_entity_id : String) : Boolean
   + validate_details_size(details : JSON) : Boolean
 }

 class ValidationResult {
   + ok : Boolean
   + errors : List<ValidationError>
   --
   + add_error(field : String, message : String) : void
   + has_errors() : Boolean
 }

 class ValidationError {
   + field : String
   + message : String
   + severity : Severity
 }

 enum Severity {
   ERROR
   WARNING
 }

 AuditValidator "1" ..> "0..*" ValidationResult : returns
 ValidationResult *-- "*" ValidationError
 ValidationError "*" -- "1" Severity

 note right of AuditValidator
   Bloquea persistencia de eventos malformados.
   Usado por AuditService.emit() antes de
   AuditRepo.append() (P-09 audit-or-abort).
 end note

 @enduml

Restricciones aplicables
========================

- **CNST-025** — eventos malformados nunca llegan al repositorio
  append-only.
- **P-09** — fallo de validación rompe la transacción del UC
  invocante (audit-or-abort).
- **CNST-026** — ``validate_details_size`` previene payloads
  abusivos que podrían filtrar PII por volumen.

Trazabilidad a UCs
==================

Invocado indirectamente vía ``AuditService.emit()`` por todos
los UCs que escriben (subset representativo):

- :doc:`/requisitos/casos-uso/auth/uc-auth-01/index` —
  ``LOGIN``
- :doc:`/requisitos/casos-uso/access/uc-acc-01/index` —
  ``PERMISSION_GRANT``
- :doc:`/requisitos/casos-uso/permissions/uc-perm-06/index` —
  ``ACCESS_GROUP_COMPOSITION_CHANGED``
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index` —
  ``ETL_RETRY``

Relaciones
==========

- ``AuditService`` depende de ``AuditValidator`` (composición:
  el servicio orquesta la validación previa al append).
- ``AuditValidator`` no persiste estado: opera por valor sobre
  cada ``AuditEvent`` recibido.
