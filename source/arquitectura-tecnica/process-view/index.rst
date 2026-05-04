.. meta::
 :artefacto: INDEX_AT_PROCESSVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-processview-index:

================================
Process View — Vista de Procesos
================================

Patrones de concurrencia y sincronizacion del sistema IACT. Cada archivo
documenta un patron transversal de alto nivel: flujos concurrentes,
coordinacion de workers, sincronizacion de cache, pool de conexiones y
timeouts. No cubre flujos UC individuales — esos viven en
``requisitos/casos-uso/``.

.. toctree::
 :maxdepth: 1
 :caption: Patrones de concurrencia

 proc-etl-pipeline
 proc-alertas-paralelas
 proc-sesiones-jwt
 proc-dashboard-concurrencia
