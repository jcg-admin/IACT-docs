.. meta::
 :artefacto: ARQ_MOD_004_DIAG_SUB_ESTADOS
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/etl-monitoring/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_004_sub_estados_proceso_etl:

===========================
Sub-estados del proceso ETL
===========================

.. uml::
 :caption: Maquina de estados de una ejecucion ETL (etl_runs).

 @startuml

 [*] --> en_ejecucion : sp_etl_maestro invocado\n(automatico o manual)

 state en_ejecucion {
   [*] --> procesando_detalle : sp_etl_base_detalle
   procesando_detalle --> procesando_clientes : registrar exitoso
   procesando_clientes --> [*] : registrar exitoso
 }

 en_ejecucion --> exitoso : ambos sp_etl_* completan sin error
 en_ejecucion --> fallido : cualquier sp_etl_* lanza error

 exitoso --> [*] : datos disponibles en base_ivr_*
 fallido --> en_ejecucion : request_pipeline_retry manual (RBAC)
 fallido --> [*] : sin reintento

 note right of fallido
   BR-016: alerta si tasa
   de abandono >30% y ETL
   permanece fallido.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/etl-monitoring/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
