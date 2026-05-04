.. meta::
 :artefacto: AT_UC_MOD_AUDIT
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_audit:

================================================
MOD_Audit — Auditoria de Acciones: UC por Modulo
================================================

MOD_Audit — Auditoria de Acciones
=====================================

Consulta inmutable del registro de acciones de modificacion en
``audit_log`` (PostgreSQL). Cubre altas/bajas de usuarios, cambios
RBAC, disparos de ETL y cualquier accion de escritura.

.. uml::
 :caption: Figura 23 — MOD_Audit: casos de uso

 @startuml
 left to right direction

 actor "view_audit_log" as view_audit_log
 actor "search_audit_log" as search_audit_log
 actor "export_audit_log" as export_audit_log
 actor "generate_compliance_report" as generate_compliance_report

 rectangle "MOD_Audit" {
   usecase "UC_AUD_01\nVer Auditoria\nGeneral" as VER_AUDITORIA
   usecase "UC_AUD_02\nBuscar en\nAuditoria" as BUSCAR_AUDITORIA
   usecase "UC_AUD_03\nExportar\nAuditoria" as EXPORTAR_AUDITORIA
   usecase "UC_AUD_04\nGenerar Reporte\nCompliance" as REPORTE_COMPLIANCE
 }

 view_audit_log --> VER_AUDITORIA
 search_audit_log --> BUSCAR_AUDITORIA
 export_audit_log --> EXPORTAR_AUDITORIA
 generate_compliance_report --> REPORTE_COMPLIANCE

 VER_AUDITORIA ..> BUSCAR_AUDITORIA : <<extend>>
 BUSCAR_AUDITORIA ..> EXPORTAR_AUDITORIA : <<extend>>
 REPORTE_COMPLIANCE ..> BUSCAR_AUDITORIA : <<include>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
