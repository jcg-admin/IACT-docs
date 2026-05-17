.. meta::
 :artefacto: UC_LOG_02
 :tipo: Caso de Uso (Spec Completa)
 :dominio: requisitos
 :subdominio: casos_uso/logs
 :estado: Vigente
 :version: 5.0.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-01
 :autor: NestorMonroy
 :clasificacion: Importante
 :normativa: CNST-009, CNST-013, CNST-026

.. _uc-log-02:

==============================================
UC_LOG_02 — Consultar Logs del ETL
==============================================

Resumen
=======

Subset de UC_LOG_01 filtrado a service=etl.
Para data engineers analizando pipelines.

.. list-table::
 :widths: 25 75

 * - **Funcion RBAC**
   - ``view_pipeline_logs``

Estructura: las 12 partes (similar a
UC_LOG_01 con scope etl).

.. toctree::
 :maxdepth: 1

 informacion-general
 actores-precondiciones
 flujo-principal
 flujos-alternos
 excepciones
 requisitos-no-funcionales
 datos-involucrados
 diagramas-uml/index
 criterios-aceptacion
 patrones-diseno
 implementacion-tecnica
 testing
