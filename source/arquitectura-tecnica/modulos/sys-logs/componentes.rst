.. _arq-mod-008-componentes:

================================================
ARQ_MOD_008 — Componentes Tecnicos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Componentes de Aplicacion
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Descripcion
 * - apps.monitoring
   - Health checks, metricas, vistas de logs

----

Niveles de Log
==============

.. list-table::
 :widths: 15 25 60
 :header-rows: 1

 * - Nivel
   - Codigo
   - Uso
 * - DEBUG
   - 10
   - Solo en desarrollo, nunca en produccion
 * - INFO
   - 20
   - Operaciones normales (inicio servicios, conexiones)
 * - WARNING
   - 30
   - Situaciones anomalas no criticas
 * - ERROR
   - 40
   - Errores que requieren atencion
 * - CRITICAL
   - 50
   - Fallas graves, sistema comprometido

----

Configuracion de Logging
=========================

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
----

Health Check — Vista
=====================

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
----

APIs Expuestas
==============

**API_009_Health_Endpoints**

.. list-table::
 :widths: 15 40 45
 :header-rows: 1

 * - Metodo
   - Endpoint
   - Descripcion
 * - GET
   - /api/v1/health
   - Estado de salud (publico)
 * - GET
   - /api/v1/health/detailed
   - Detalle de servicios (auth)
 * - GET
   - /api/v1/logs
   - Listar logs (paginado)
 * - GET
   - /api/v1/logs/download
   - Paquete comprimido
 * - GET
   - /api/v1/metrics/technical
   - Metricas agregadas
