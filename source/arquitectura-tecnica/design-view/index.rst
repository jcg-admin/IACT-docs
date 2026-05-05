.. meta::
 :artefacto: INDEX_AT_DESIGNVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-designview-index:

=====================================
Design View — Vista de Diseno
=====================================

Patrones de interaccion del sistema IACT a nivel modulo. Cada archivo
muestra el diagrama de secuencia canonico del modulo: participantes
con nombres de servicio reales (CamelCase), clases de dominio
canonicas (``User``, ``Session``, ``AuditEvent``, ``Assignment``,
``ExceptionalPermission``, ``PipelineExecution``, ``Alert``, ``Report``,
``ExportJob``, ``ApplicationLog``, ``Call``), y flujo principal con
casos de error relevantes.

Granularidad: un diagrama canonico por modulo funcional, no uno por
caso de uso individual.

.. toctree::
 :maxdepth: 1
 :caption: Modulos funcionales

 seq-auth
 seq-users
 seq-access
 seq-permissions
 seq-admin
 seq-alerts
 seq-audit
 seq-pipeline
 seq-logs
 seq-reports
 seq-operator
 seq-caller
 seq-supervision
