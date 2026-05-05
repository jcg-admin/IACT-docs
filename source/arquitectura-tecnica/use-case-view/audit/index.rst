.. meta::
 :artefacto: AT_UC_MOD_AUDIT
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_audit:

================================================
MOD_Audit — Auditoria de Acciones: UC por Modulo
================================================

Consulta inmutable del registro de acciones de modificación en
``audit_log`` (PostgreSQL). Cubre altas/bajas de usuarios,
cambios RBAC, disparos de pipeline y cualquier acción de
escritura. Append-only por CNST-025.

.. uml::
 :caption: MOD_Audit — Auditor lee y exporta;
           genera reportes de compliance.

 @startuml
 left to right direction

 actor Auditor

 rectangle "MOD_Audit" {   usecase "UC_AUD_01\nVer Auditoria\nGeneral\n.. extension points ..\nBuscar" as VER_AUDITORIA   usecase "UC_AUD_02\nBuscar en\nAuditoria\n.. extension points ..\nExportar" as BUSCAR_AUDITORIA
   usecase "UC_AUD_03\nExportar\nAuditoria" as EXPORTAR_AUDITORIA
   usecase "UC_AUD_04\nGenerar Reporte\nCompliance" as REPORTE_COMPLIANCE
 }

 Auditor --> VER_AUDITORIA
 Auditor --> BUSCAR_AUDITORIA
 Auditor --> EXPORTAR_AUDITORIA
 Auditor --> REPORTE_COMPLIANCE

 BUSCAR_AUDITORIA ..> VER_AUDITORIA : <<extend>>
 EXPORTAR_AUDITORIA ..> BUSCAR_AUDITORIA : <<extend>>
 REPORTE_COMPLIANCE ..> BUSCAR_AUDITORIA : <<include>>

 note right of MOD_Audit
   Codenames RBAC:
     Auditor (AGR-008) →
       view_audit_log,
       search_audit_log,
       export_audit_log,
       generate_compliance_report
   CNST-025: append-only sin update/delete.
 end note

 @enduml

Lectura del diagrama
====================

- ``Auditor`` (AGR-008) es el único rol con acceso al
  log de auditoría — operación read-only sobre tabla
  append-only (CNST-025).
- ``UC_AUD_01`` ``<<extend>>`` ``UC_AUD_02``: tras ver
  el log el auditor puede afinar con búsqueda.
- ``UC_AUD_02`` ``<<extend>>`` ``UC_AUD_03``: la
  exportación ocurre opcionalmente sobre el resultado
  filtrado.
- ``UC_AUD_04`` ``<<include>>`` ``UC_AUD_02``: el
  reporte de compliance se construye sobre búsquedas
  predefinidas.

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/audit-event` — AuditEvent (CNST-025 append-only).
- :doc:`/arquitectura-tecnica/domain-model/audit-service` — AuditService (P-09 audit-or-abort).
- :doc:`/arquitectura-tecnica/domain-model/audit-repo` — AuditRepo.
- :doc:`/arquitectura-tecnica/domain-model/audit-query-service` — AuditQueryService (UC_AUD_01/02).
- :doc:`/arquitectura-tecnica/domain-model/audit-validator` — AuditValidator.
- :doc:`/arquitectura-tecnica/domain-model/pii-scanner` — PiiScanner (CNST-026).
- :doc:`/arquitectura-tecnica/domain-model/sanitizer` — Sanitizer.
- :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` — CursorEncoder (paginación).
- :doc:`/arquitectura-tecnica/domain-model/export-worker` — ExportWorker (UC_AUD_03).

Casos de uso del módulo
=========================

Cada UC tiene su especificación textual completa y su diagrama
individual (con `<<include>>` y `<<extend>>` per uml-07) en
``source/requisitos/casos-uso/``:

.. list-table::
 :header-rows: 1
 :widths: 20 50 30

 * - UC
   - Nombre
   - Diagrama
 * - :doc:`UC_AUD_01 </requisitos/casos-uso/audit/uc-aud-01/index>`
   - Consultar Auditoria General
   - :doc:`Diagrama </requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_AUD_02 </requisitos/casos-uso/audit/uc-aud-02/index>`
   - Buscar Auditoria
   - :doc:`Diagrama </requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_AUD_03 </requisitos/casos-uso/audit/uc-aud-03/index>`
   - Exportar Auditoria
   - :doc:`Diagrama </requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_AUD_04 </requisitos/casos-uso/audit/uc-aud-04/index>`
   - Generar Reporte de Compliance
   - :doc:`Diagrama </requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-caso-de-uso>`

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

UC standalone uml-07
====================

Diagramas standalone uml-07 por UC (auto-explicativos):

.. toctree::
 :maxdepth: 1

 uc-aud-01-consultar-auditoria-general
 uc-aud-02-buscar-auditoria
 uc-aud-03-exportar-auditoria-async
 uc-aud-04-generar-reporte-de-compliance
