.. meta::
 :artefacto: AT_UML_SISTEMA_12_ESTADOS_ETL
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_submaquina_etl:

====================================================
Sistema IACT — Sub-maquina de Estados: Ejecucion ETL
====================================================

12. Sub-maquina de Estados — Ejecucion ETL
============================================

Sub-estado interno de ``Gestion Pipeline ETL``. Muestra la
ejecucion paralela de ``sp_etl_base_detalle`` y
``sp_etl_base_clientes`` (disparados internamente por
``sp_etl_maestro``) con fork/join antes de actualizar el
estado en ``etl_runs``.

.. uml::
 :caption: Figura 13 — Sub-maquina de estados: Ejecucion ETL

 @startuml

 state "Ejecucion ETL" as ETL_EXEC {

   state "Recibir Solicitud ETL" as RECIBIR_SOLICITUD_ETL
   RECIBIR_SOLICITUD_ETL : entry / validar funcion view_pipeline_status en JWT
   RECIBIR_SOLICITUD_ETL : do / registrar etl_runs (estado=en_ejecucion)
   RECIBIR_SOLICITUD_ETL : exit / ID de ejecucion asignado

   state fork_etl <<fork>>

   state "sp_etl_base_detalle" as SP_RPT_CENTROS_XSEGMENTO
   SP_RPT_CENTROS_XSEGMENTO : entry / leer tbl_historico_detalle (fuente IVR)
   SP_RPT_CENTROS_XSEGMENTO : do / TRUNCATE + registrar base_ivr_detalle
   SP_RPT_CENTROS_XSEGMENTO : exit / rows_detalle registrados en etl_runs

   state "sp_etl_base_clientes" as SP_RPT_LLAMADAS_ABANDONADAS
   SP_RPT_LLAMADAS_ABANDONADAS : entry / leer tbl_historico_clientes (fuente IVR)
   SP_RPT_LLAMADAS_ABANDONADAS : do / TRUNCATE + registrar base_ivr_clientes
   SP_RPT_LLAMADAS_ABANDONADAS : exit / rows_clientes registrados en etl_runs

   state join_etl <<join>>

   state "Verificar Resultado" as VERIFICAR_RESULTADO_ETL
   VERIFICAR_RESULTADO_ETL : entry / consolidar resultado de ambos sp_etl_*
   VERIFICAR_RESULTADO_ETL : do / actualizar etl_runs SET estado, finalizado_en
   VERIFICAR_RESULTADO_ETL : exit / fin de cadena ETL

   state "ETL Exitoso" as ETL_EXITOSO
   ETL_EXITOSO : entry / estado = exitoso
   ETL_EXITOSO : do / notificar request_pipeline_retry
   ETL_EXITOSO : exit / datos disponibles en base_ivr_*

   state "ETL Fallido" as ETLFallido
   ETLFallido : entry / estado = fallido
   ETLFallido : do / generar alerta BR-016 si aplica
   ETLFallido : exit / reintento disponible via sp_etl_historico

   [*] --> RECIBIR_SOLICITUD_ETL
   RECIBIR_SOLICITUD_ETL --> fork_etl
   fork_etl --> SP_RPT_CENTROS_XSEGMENTO
   fork_etl --> SP_RPT_LLAMADAS_ABANDONADAS
   SP_RPT_CENTROS_XSEGMENTO --> join_etl
   SP_RPT_LLAMADAS_ABANDONADAS --> join_etl
   join_etl --> VERIFICAR_RESULTADO_ETL
   VERIFICAR_RESULTADO_ETL --> ETL_EXITOSO : [sp_etl exitosos]
   VERIFICAR_RESULTADO_ETL --> ETLFallido : [sp_etl fallido]
   ETL_EXITOSO --> [*]
   ETLFallido --> [*]
 }

 [*] --> ETL_EXEC
 ETL_EXEC --> [*]

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
