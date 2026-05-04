.. meta::
 :artefacto: ARQ_MOD_007_DIAG_ESTADOS_EXPORTACION
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/audit/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_007_estados_exportacion_audit:

===========================================
Estados del Proceso de Exportacion de Audit
===========================================

Estados del Proceso de Exportacion de Audit
=============================================

.. uml::
 :caption: Estado del job de exportacion de audit log (UC_AUD_03).

 @startuml

 [*] --> Queued : export_audit_log solicita exportacion
 Queued --> Processing : ExportWorker disponible
 Processing --> Done : archivo generado y firmado HMAC
 Processing --> Failed : error I/O o timeout
 Done --> [*] : notificacion enviada via InternalMailbox
 Failed --> Queued : reintento automatico

 note right of Done
   El archivo lleva firma HMAC
   para verificacion de
   integridad (generate_compliance_report).
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/audit/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
