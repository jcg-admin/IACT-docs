.. meta::
 :artefacto: AT_DESIGN_MOD_AUDIT
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_audit:

============================================================
Design View — MOD_Audit: Vista de Diseño
============================================================

Caja del modulo **MOD_Audit** (registro inmutable y consulta
de eventos de seguridad). Cubre la emision de ``AuditEvent``
durante operaciones privilegiadas, la consulta paginada con
filtros y la generacion de reportes de compliance.

Materializa los UCs UC_AUD_01..04 documentados en
:doc:`/arquitectura-tecnica/use-case-view/audit/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Audit — entidad central (AuditEvent),
           servicios productor (AuditService) y consumidor
           (AuditQueryService). Detalle interno en
           :doc:`bounded-context`.

 @startuml

 package "MOD_Audit" {
   class AuditEvent <<entity>>
   class AuditService <<service>>
   class AuditQueryService <<service>>
 }

 class AuthorizationGuard <<external>>
 class PIIScanner <<external>>

 AuditService ..> AuditEvent : <<crea>>
 AuthorizationGuard ..> AuditService : <<emite eventos>>
 AuditService ..> PIIScanner : <<sanitiza>>

 AuditQueryService ..> AuditEvent : <<lee>>

 note bottom of AuditEvent
   Inmutable per CNST-025.
   Sin PII en payload (CNST-026).
   Repos y validators internos en :doc:`bounded-context`.
 end note

 @enduml

Lectura del diagrama
====================

- **Entidad central:** ``AuditEvent`` — registro inmutable
  append-only de cada operacion privilegiada (CNST-025).
- **Productor:** ``AuditService`` recibe llamadas de
  ``AuthorizationGuard`` y de cualquier modulo que ejecute
  cambios privilegiados; sanitiza el payload via
  ``PIIScanner`` (CNST-026) y persiste el evento.
- **Consumidor:** ``AuditQueryService`` provee consulta
  paginada con filtros y genera reportes de compliance.
- Repositories, validators y encoders internos viven en
  :doc:`bounded-context`; aqui solo se muestran los puntos de
  contacto inter-modulo.

Clases canonicas que materializan el modulo
============================================

- :doc:`/arquitectura-tecnica/domain-model/audit-event` —
  AuditEvent (entidad inmutable).
- :doc:`/arquitectura-tecnica/domain-model/audit-service` —
  AuditService (productor).
- :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
  AuditRepo.
- :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
  AuditQueryService (lectura).
- :doc:`/arquitectura-tecnica/domain-model/audit-validator` —
  AuditValidator (sin PII).
- :doc:`/arquitectura-tecnica/domain-model/general-audit-service` —
  GeneralAuditService.
- :doc:`/arquitectura-tecnica/domain-model/pii-scanner` —
  PIIScanner.
- :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
  CursorEncoder (paginacion).

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Audit

 bounded-context
 interaction-pattern
 audit-event-lifecycle

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/audit/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/index`.
 - :doc:`/arquitectura-tecnica/design-view/access/index` —
   modulo emisor de eventos RBAC.
 - :doc:`/arquitectura-tecnica/design-view/package-overview`.
