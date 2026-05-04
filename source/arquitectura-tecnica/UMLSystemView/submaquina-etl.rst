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

   state "Recibir Solicitud ETL" as S1
   S1 : entry / validar funcion view_pipeline_status en JWT
   S1 : do / INSERT etl_runs (estado=en_ejecucion)
   S1 : exit / ID de ejecucion asignado

   state fork_etl <<fork>>

   state "sp_etl_base_detalle" as S2A
   S2A : entry / leer tbl_historico_detalle (fuente IVR)
   S2A : do / TRUNCATE + INSERT base_ivr_detalle
   S2A : exit / rows_detalle registrados en etl_runs

   state "sp_etl_base_clientes" as S2B
   S2B : entry / leer tbl_historico_clientes (fuente IVR)
   S2B : do / TRUNCATE + INSERT base_ivr_clientes
   S2B : exit / rows_clientes registrados en etl_runs

   state join_etl <<join>>

   state "Verificar Resultado" as S3
   S3 : entry / consolidar resultado de ambos sp_etl_*
   S3 : do / UPDATE etl_runs SET estado, finalizado_en
   S3 : exit / fin de cadena ETL

   state "ETL Exitoso" as SUCC
   SUCC : entry / estado = exitoso
   SUCC : do / notificar request_pipeline_retry
   SUCC : exit / datos disponibles en base_ivr_*

   state "ETL Fallido" as ETLFallido
   ETLFallido : entry / estado = fallido
   ETLFallido : do / generar alerta BR-016 si aplica
   ETLFallido : exit / reintento disponible via sp_etl_historico

   [*] --> S1
   S1 --> fork_etl
   fork_etl --> S2A
   fork_etl --> S2B
   S2A --> join_etl
   S2B --> join_etl
   join_etl --> S3
   S3 --> SUCC : [sp_etl exitosos]
   S3 --> ETLFallido : [sp_etl fallido]
   SUCC --> [*]
   ETLFallido --> [*]
 }

 [*] --> ETL_EXEC
 ETL_EXEC --> [*]

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
