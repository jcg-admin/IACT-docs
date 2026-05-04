.. meta::
 :artefacto: AT_DM_CLASS_EXPORT_WORKER
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_export_worker:

============
ExportWorker
============

Worker de exportacion asincrona de resultados de AuditQueryService.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase ExportWorker — stub pendiente de desarrollo.

 @startuml

 class ExportWorker {
  + enqueue(job)
  + process(job)
 }

 @enduml
