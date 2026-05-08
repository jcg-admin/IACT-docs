.. meta::
 :artefacto: UC_LOG_06
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

.. _uc-log-06:

==============================================
UC_LOG_06 — Ver Estado del Sistema
==============================================

Resumen
=======

Health check global: status de servicios,
dependencias (BD, cache, mensajeria),
ETL, alertas activas. Vista one-glance
para SRE.

.. list-table::
 :widths: 25 75

 * - **Funcion RBAC**
   - ``view_system_status``

.. toctree::
 :maxdepth: 1

 informacion-general
 actores-precondiciones
 flujo-principal
 flujos-alternos
 excepciones
 requisitos-no-funcionales
 datos-involucrados
 diagramas-uml
 criterios-aceptacion
 patrones-diseno
 implementacion-tecnica
 testing
