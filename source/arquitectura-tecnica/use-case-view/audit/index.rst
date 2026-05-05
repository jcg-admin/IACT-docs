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

 rectangle "MOD_Audit" {
   usecase "UC_AUD_01\nVer Auditoria\nGeneral" as VER_AUDITORIA
   usecase "UC_AUD_02\nBuscar en\nAuditoria" as BUSCAR_AUDITORIA
   usecase "UC_AUD_03\nExportar\nAuditoria" as EXPORTAR_AUDITORIA
   usecase "UC_AUD_04\nGenerar Reporte\nCompliance" as REPORTE_COMPLIANCE
 }

 Auditor --> VER_AUDITORIA
 Auditor --> BUSCAR_AUDITORIA
 Auditor --> EXPORTAR_AUDITORIA
 Auditor --> REPORTE_COMPLIANCE

 VER_AUDITORIA ..> BUSCAR_AUDITORIA : <<extend>>
 BUSCAR_AUDITORIA ..> EXPORTAR_AUDITORIA : <<extend>>
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

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
