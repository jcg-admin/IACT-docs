.. meta::
 :artefacto: AT_DM_CLASS_ETL_EJECUCION
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: PipelineETL
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_etl_ejecucion:

=============
ETLEjecucion
=============

Registro de una ejecucion del Servicio ETL. Persistida en la tabla
``etl_runs`` del Almacen de Datos (propiedad IACT). Los errores no
son entidades separadas: el campo ``mensaje_error`` captura el fallo.
El Scheduler es infraestructura, no dominio.

.. uml::
 :caption: Clase ETLEjecucion — registro de ejecucion del pipeline ETL.

 @startuml

 class ETLEjecucion {
   + id : Integer
   + tabla_origen : String
   + trimestre : String
   + iniciado_en : DateTime
   + finalizado_en : DateTime
   + estado : EstadoEjecucion
   + registros_base : Integer
   + mensaje_error : String
   + ejecutado_por : String
   --
   + es_exitosa() : Boolean
   + es_fallida() : Boolean
   + duracion_segundos() : Integer
 }

 enum EstadoEjecucion {
   en_ejecucion
   exitoso
   fallido
 }

 ETLEjecucion -- EstadoEjecucion

 note right of ETLEjecucion
   CNST-007: tbl_historico_* es solo lectura.
   CNST-008: ETL en ventana de 6-12 horas.
   Persistida en etl_runs (Almacen de Datos IACT).
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/bc-pipeline-etl`
