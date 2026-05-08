.. meta::
 :artefacto: ARQ_MOD_007_DIAG_COMPONENTES
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/audit/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_007_componentes_mod_audit:

===================================
Diagrama de componentes — MOD_Audit
===================================

.. uml::
 :caption: Componentes de MOD_Audit y sus dependencias.

 @startuml

 actor "view_audit_log" as view_audit_log
 actor "export_audit_log" as export_audit_log
 actor "generate_compliance_report" as generate_compliance_report

 component "AuditQueryEndpoint\n(/api/audit/)" as Auditqueryendpoint
 component "AuditExportWorker\n(async)" as Auditexportworker
 component "ComplianceWorker\n(HMAC signer)" as Complianceworker
 component "InternalMailbox" as Internalmailbox

 database "audit_log\n(PostgreSQL — append-only)" as audit_log

 view_audit_log --> Auditqueryendpoint : GET /api/audit/
 export_audit_log --> Auditqueryendpoint : POST /api/audit/export/
 generate_compliance_report --> Auditqueryendpoint : POST /api/audit/compliance/
 Auditqueryendpoint --> audit_log : consultar (lectura)
 Auditqueryendpoint --> Auditexportworker : encolar job export
 Auditqueryendpoint --> Complianceworker : encolar job compliance
 Auditexportworker --> audit_log : consultar rango
 Complianceworker --> audit_log : consultar periodo
 Auditexportworker --> Internalmailbox : archivo CSV/JSON
 Complianceworker --> Internalmailbox : archivo firmado HMAC

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/audit/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
