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

.. code-block:: python

 # config/settings/base.py

 LOGGING = {
     'version': 1,
     'disable_existing_loggers': False,
     'formatters': {
         'verbose': {
             'format': '{asctime} [{levelname}] {name} {module}: {message}',
             'style': '{',
         },
     },
     'handlers': {
         'file': {
             'level': 'INFO',
             'class': 'logging.handlers.RotatingFileHandler',
             'filename': '/var/log/iact/application.log',
             'maxBytes': 10485760,  # 10MB
             'backupCount': 10,
             'formatter': 'verbose',
         },
         'error_file': {
             'level': 'ERROR',
             'class': 'logging.handlers.RotatingFileHandler',
             'filename': '/var/log/iact/error.log',
             'maxBytes': 10485760,
             'backupCount': 20,
             'formatter': 'verbose',
         },
     },
     'loggers': {
         'django': {'handlers': ['file'], 'level': 'INFO'},
         'apps': {'handlers': ['file', 'error_file'], 'level': 'INFO'},
     },
 }

----

Health Check — Vista
=====================

.. code-block:: python

 # apps/monitoring/views.py

 class HealthCheckView(APIView):
     permission_classes = [AllowAny]

     def get(self, request):
         checks = {
             'database_analytics': self._check_analytics_db,
             'database_ivr': self._check_ivr_db,
             'cache': self._check_cache,
             'disk_space': self._check_disk,
             'memory': self._check_memory,
         }

         all_healthy = all(c['status'] == 'healthy' for c in checks.values)

         return Response({
             'status': 'healthy' if all_healthy else 'degraded',
             'timestamp': timezone.now.isoformat,
             'checks': checks,
         }, status=200 if all_healthy else 503)

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
