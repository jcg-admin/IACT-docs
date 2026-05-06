.. meta::
 :artefacto: AT_DESIGN_CLASS_AUDIT
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_audit:

============================================================
Design View — MOD_Audit: Estructura de Clases
============================================================

Modulo **transversal**: TODA escritura del sistema emite un
``AuditEvent`` aqui. Provee tambien query API para auditores
con filtros, paginacion (cursor encoder) y sin PII (CNST-026).

.. uml::
 :caption: MOD_Audit — clases canonicas y relaciones internas.

 @startuml

 class AuditEvent
 class AuditService <<sistema>>
 class AuditRepo <<sistema>>
 class AuditQueryService <<sistema>>
 class AuditValidator <<sistema>>
 class CursorEncoder <<sistema>>
 class FilterValidator <<sistema>>
 class AuthorizationGuard <<sistema>>

 AuditService ..> AuditEvent : crea
 AuditService ..> AuditRepo : persiste
 AuditService ..> AuditValidator : valida sin PII
 AuditRepo ..> AuditEvent

 AuditQueryService ..> AuditRepo : query con filtros
 AuditQueryService ..> CursorEncoder : pagina
 AuditQueryService ..> FilterValidator : valida filtros
 AuthorizationGuard ..> AuditQueryService : verify view_audit_log

 note bottom of AuditValidator
   CNST-026: rechaza eventos con PII
   en payload (email, telefono, etc.)
 end note

 @enduml

----

UCs cubiertos
==============

UC_AUD_01..04 — consultar logs de auditoria, exportar reporte
de auditoria, configurar retencion, etc. Ver
:doc:`/arquitectura-tecnica/use-case-view/audit/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-event`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo`
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service`
 - :doc:`/arquitectura-tecnica/domain-model/audit-validator`
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder`
 - :doc:`/arquitectura-tecnica/domain-model/filter-validator`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/use-case-view/audit/index`
 - :doc:`/arquitectura-tecnica/design-view/seq-audit`
