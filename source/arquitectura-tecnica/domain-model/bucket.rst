.. meta::
 :artefacto: AT_DM_CLASS_BUCKET
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_bucket:

======
Bucket
======

Agrupacion de KPIs dentro de un HistoricalReport por bucket_key.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase Bucket — stub pendiente de desarrollo.

 @startuml

 class Bucket {
  + bucket_key : String
  + kpis : KPISet
 }

 @enduml
