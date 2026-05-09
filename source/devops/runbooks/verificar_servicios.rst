:orphan:

.. meta::
 :artefacto: DEVOPS_RUNBOOK_VERIFICAR_SERVICIOS
 :tipo: Runbook DevOps
 :dominio: devops
 :subdominio: runbooks
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Operacional

.. _devops_runbook_verificar_servicios:

============================================================
Runbook — Verificacion de servicios IACT
============================================================

Procedimiento para verificar que los servicios criticos de
IACT estan operativos. Aplicable post-deploy, post-recovery
o como check periodico.

Servicios a verificar
======================

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Servicio
   - Como verificar
   - Resultado esperado
 * - Django app server
   - ``curl -f http://localhost:8000/api/v1/health/``
   - HTTP 200 + ``{"status": "ok"}``
 * - MariaDB IACT
   - ``mysqladmin -u $IACT_DB_USER -p$IACT_DB_PASSWORD ping``
   - ``mysqld is alive``
 * - MariaDB cliente IVR
   - ``mysqladmin -u $IVR_DB_USER -p$IVR_DB_PASSWORD ping``
   - ``mysqld is alive``
 * - APScheduler (en worker designado)
   - log: grep "alert_evaluator" en
     ``/var/log/iact/django.log``
   - mensaje "evaluator tick at <ts>" cada ~60s
 * - MySQL Event Scheduler
   - ``SELECT @@event_scheduler;``
   - ``ON``
 * - ``evt_etl_diario`` event
   - ``SELECT * FROM information_schema.events
     WHERE event_name = 'evt_etl_diario';``
   - una fila con ``STATUS = 'ENABLED'``

Diagnostico de fallos
======================

Si Django no responde
----------------------

.. code-block:: bash

   sudo systemctl status iact-django
   sudo journalctl -u iact-django -n 100
   tail -50 /var/log/iact/django.log

Si MariaDB no responde
-----------------------

.. code-block:: bash

   sudo systemctl status mariadb
   sudo journalctl -u mariadb -n 100

Si el ETL no esta corriendo a las 02:00
----------------------------------------

.. code-block:: sql

   -- Verificar que el event scheduler esta activo
   SELECT @@event_scheduler;
   -- Verificar el event
   SHOW EVENTS WHERE name = 'evt_etl_diario';
   -- Verificar la ultima ejecucion
   SELECT * FROM etl_runs
   ORDER BY inicio_at DESC LIMIT 5;
   -- Verificar checkpoints
   SELECT * FROM job_execution_log
   ORDER BY start_time DESC LIMIT 10;

----

.. seealso::

 - :doc:`/devops/adr-devops-001-vagrant-mod-wsgi-importante-produc` —
   ADR de despliegue.
 - :doc:`/arquitectura-tecnica/pipeline-etl-iact/triggers` —
   detalle de los disparadores ETL.
 - :doc:`/arquitectura-tecnica/pipeline-etl-iact/intermediate-tables` —
   tablas de control (``etl_runs``, ``job_execution_log``).
