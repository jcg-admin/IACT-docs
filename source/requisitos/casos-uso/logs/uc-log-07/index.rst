.. meta::
 :artefacto: UC_LOG_07
 :tipo: Caso de Uso (Spec Completa)
 :dominio: requisitos
 :subdominio: casos_uso/logs
 :estado: Vigente
 :version: 5.0.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-01
 :autor: NestorMonroy
 :clasificacion: Importante
 :normativa: CNST-009

.. _uc-log-07:

==============================================
UC_LOG_07 — Ver Metricas Tecnicas
==============================================

Resumen
=======

Vista de metricas tecnicas del sistema:
QPS, latencia P50/P95/P99, tasa de errores
HTTP, GC pause, memory usage, request rate
por endpoint.

.. list-table::
 :widths: 25 75

 * - **Funcion RBAC**
   - ``view_technical_metrics``

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
