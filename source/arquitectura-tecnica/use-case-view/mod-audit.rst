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
   usecase "UC_AUD_01\nVer Auditoria\nGeneral" as A01
   usecase "UC_AUD_02\nBuscar en\nAuditoria" as A02
   usecase "UC_AUD_03\nExportar\nAuditoria" as A03
   usecase "UC_AUD_04\nGenerar Reporte\nCompliance" as A04
 }

 view_audit_log --> A01
 search_audit_log --> A02
 export_audit_log --> A03
 generate_compliance_report --> A04

 A01 ..> A02 : <<extend>>
 A02 ..> A03 : <<extend>>
 A04 ..> A02 : <<include>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
