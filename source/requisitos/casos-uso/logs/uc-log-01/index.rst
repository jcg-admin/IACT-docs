.. meta::
 :artefacto: UC_LOG_01
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

.. _uc-log-01:

==============================================
UC_LOG_01 — Consultar Logs del Sistema
==============================================

Resumen
=======

Vista filtrable de logs operacionales
(application logs). Distintos de
AuditEvent (que son de seguridad). Para
debugging.

.. list-table::
 :widths: 25 75

 * - **Funcion RBAC**
   - ``view_application_logs``

Estructura de la spec
=====================

.. toctree::
 :maxdepth: 1
 :caption: Las 12 partes

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
