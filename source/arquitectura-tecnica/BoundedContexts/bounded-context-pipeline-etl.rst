.. meta::
 :artefacto: AT_DOMINIO_05_PIPELINE
 :tipo: Diagrama Arquitectonico — Modelo de Dominio
 :dominio: arquitectura_tecnica
 :subdominio: BoundedContexts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dominio_iact_pipeline:

================================================
Modelo de Dominio — Bounded Context Pipeline ETL
================================================

4.5 Pipeline ETL
----------------

Una clase de dominio: ``ETLEjecucion``. Cada ejecucion del Servicio
ETL genera un registro en el Registro de Ejecuciones. Los errores
no son entidades separadas: el campo ``mensaje_error`` en
``ETLEjecucion`` captura la descripcion del fallo.
``Scheduler`` es infraestructura, no dominio (vive en el ADR de
despliegue ADR-DEVOPS-001).

.. uml::
 :caption: Bounded context Pipeline ETL — ejecuciones del Servicio
           ETL registradas en el Registro de Ejecuciones.

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
   Persistida en Registro de Ejecuciones
   (tabla etl_runs en MariaDB, propiedad IACT).
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
