.. meta::
   :artefacto: RUNBOOK-log-retention-policies
   :tipo: Runbook
   :dominio: devops
   :subdominio: runbooks
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-11-07
   :ultimo_cambio: 2026-05-16T23:01:11
   :autor: NestorMonroy
   :clasificacion: Operacional

.. _runbook-log-retention-policies:

==========================================
Runbook: Politicas de Retencion de Logs
==========================================

.. note::

   Politicas de retencion de logs y metricas del sistema IACT.
   Define cuanto tiempo se conserva cada tipo de dato y como
   se implementa la expiracion automatica.

1. Cuando ejecutar
==================

- Al configurar un entorno nuevo para verificar que las
  politicas esten aplicadas
- Al investigar crecimiento inesperado del almacenamiento
- Al ejecutar cleanup manual si la expiracion automatica falla

2. Politicas por capa
======================

.. list-table::
   :widths: 30 20 15 35
   :header-rows: 1

   * - Capa
     - Tecnologia
     - Retention
     - Mecanismo
   * - Infrastructure logs (Capa 3)
     - Cassandra
     - 90 dias
     - TTL automatico: ``default_time_to_live = 7776000``
   * - DORA metrics
     - MySQL
     - Permanente
     - Sin TTL — critico para analytics historicos
   * - Application logs (Capa 2)
     - Filesystem
     - 1 GB max
     - ``RotatingFileHandler`` 10 archivos x 100 MB
   * - Backups de datos
     - Filesystem
     - 30 dias
     - Script ``backup_data_centralization.sh``

3. Verificacion
===============

**Cassandra TTL activo**

.. code-block:: bash

   cqlsh -e "DESCRIBE TABLE logging.infrastructure_logs;"
   # Verificar: default_time_to_live = 7776000

**MySQL sin TTL**

.. code-block:: bash

   mysql -e "SELECT COUNT(*), MAX(created_at) FROM dora_metrics;"
   # Debe mostrar todos los registros historicos

**Application logs**

.. code-block:: bash

   ls -lh /var/log/iact/*.log
   # Verificar que ningun archivo supera 100 MB

**Backups con retention**

.. code-block:: bash

   ls -lt /var/backups/iact/ | head -35
   # No deben existir mas de 30 archivos de backup

4. Cleanup manual
=================

Solo necesario si la expiracion automatica de Cassandra falla:

.. code-block:: bash

   cqlsh -e "DELETE FROM logging.infrastructure_logs
             WHERE log_date < '$(date -d '-90 days' +%Y-%m-%d)';"

5. Trazabilidad
===============

- Fuente: ``temp-holding/FASE 01/docs/operaciones/TASK-019-log_retention_policies.md``
- Backup automatico: :doc:`runbook-cron-jobs-mantenimiento`
- Restriccion relacionada: :doc:`/normativa/restricciones/cnst-008-sincronizacion-etl-en-ventana-de-6-a-12-horas`
