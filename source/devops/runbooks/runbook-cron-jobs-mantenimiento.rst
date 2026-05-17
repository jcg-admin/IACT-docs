.. meta::
   :artefacto: RUNBOOK-cron-jobs-mantenimiento
   :tipo: Runbook
   :dominio: devops
   :subdominio: runbooks
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-11-07
   :ultimo_cambio: 2026-05-16T23:01:11
   :autor: NestorMonroy
   :clasificacion: Operacional

.. _runbook-cron-jobs-mantenimiento:

==========================================
Runbook: Cron Jobs de Mantenimiento
==========================================

.. note::

   Procedimiento operativo para gestionar los cron jobs automatizados
   de mantenimiento del sistema IACT. Los tres jobs cubren limpieza
   de sesiones, health check continuo y backup diario.

   **Stack:** Django sobre Apache + mod_wsgi en VM Vagrant.
   Scripts en ``scripts/`` del repositorio.

1. Cuando ejecutar
==================

- Al provisionar un entorno nuevo (``vagrant up`` inicial)
- Al detectar que un job dejo de ejecutarse (ausencia en logs)
- Al cambiar la frecuencia o configuracion de un job
- Al agregar un nuevo job de mantenimiento

2. Precondiciones
=================

- VM Vagrant corriendo: ``vagrant status`` muestra ``running``
- Directorio de logs creado: ``/var/log/iact/``
- Scripts con permisos de ejecucion

.. code-block:: bash

   sudo mkdir -p /var/log/iact
   sudo chown $USER:$USER /var/log/iact
   sudo chmod 755 /var/log/iact
   chmod +x scripts/*.sh

3. Jobs configurados
====================

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Script
     - Frecuencia
     - Funcion
   * - ``cleanup_sessions.sh``
     - Cada 6 horas
     - Elimina sesiones expiradas de ``django_session`` en MySQL
   * - ``health_check.sh``
     - Cada 5 minutos
     - Verifica salud del sistema (Django, BD, migraciones)
   * - ``backup_data_centralization.sh``
     - Diario 2:00 AM
     - Backup de ``dora_metrics`` MySQL + JSON logs. Retention: 30 dias

4. Instalacion del crontab
===========================

.. code-block:: bash

   crontab -e

Agregar las siguientes entradas:

.. code-block:: cron

   # IACT — Automated Maintenance Jobs

   # Limpieza de sesiones expiradas — cada 6 horas
   0 */6 * * * /home/user/IACT---project/scripts/cleanup_sessions.sh --force >> /var/log/iact/cleanup.log 2>&1

   # Health check del sistema — cada 5 minutos
   */5 * * * * /home/user/IACT---project/scripts/health_check.sh --json >> /var/log/iact/health.log 2>&1

   # Backup diario de datos centralizados — 2:00 AM
   0 2 * * * MYSQL_PWD=${MYSQL_PASSWORD} /home/user/IACT---project/scripts/backup_data_centralization.sh >> /var/log/iact/backup.log 2>&1

5. Verificacion
===============

.. code-block:: bash

   # Confirmar que los jobs estan instalados
   crontab -l

   # Test manual de cada script
   scripts/cleanup_sessions.sh --dry-run
   scripts/health_check.sh --verbose
   MYSQL_PWD=<password> scripts/backup_data_centralization.sh

   # Ver logs recientes
   tail -50 /var/log/iact/cleanup.log
   tail -50 /var/log/iact/health.log
   tail -50 /var/log/iact/backup.log

   # Verificar ejecucion en syslog
   grep CRON /var/log/syslog | tail -20

6. Metricas y alertas
======================

**cleanup_sessions.sh**

- Sesiones eliminadas por ejecucion: 0–10 000 (depende del trafico)
- ALERTA si tabla ``django_session`` supera 100 000 filas
- Duracion esperada: < 30 segundos

**health_check.sh**

- Retorna exit code 0 (saludable) o 1 (no saludable)
- Validaciones: SESSION_ENGINE, conectividad PostgreSQL, MySQL,
  estado de migraciones, tamano de ``django_session``
- ALERTA si cualquier check retorna FAIL

**backup_data_centralization.sh**

- Componentes: ``dora_metrics`` MySQL + ``/var/log/iact/*.json.log``
- Retention: 30 dias (maximo 30 archivos)
- Tamano esperado comprimido: 5–200 MB

7. Troubleshooting
==================

**Cron no ejecuta los scripts**

.. code-block:: bash

   # Verificar permisos
   chmod +x scripts/*.sh

   # Verificar logs del cron del sistema
   grep CRON /var/log/syslog

**Cleanup no elimina sesiones**

.. code-block:: bash

   # Verificar sesiones expiradas
   cd api/callcentersite
   python manage.py shell -c "
   from django.contrib.sessions.models import Session
   from django.utils import timezone
   expired = Session.objects.filter(expire_date__lt=timezone.now())
   print(f'Sesiones expiradas: {expired.count()}')
   "

**Backup falla por MYSQL_PWD no configurado**

.. code-block:: bash

   # Configurar credenciales en ~/.my.cnf
   cat > ~/.my.cnf << 'MYCNF'
   [client]
   user=root
   password=<password>
   host=127.0.0.1
   port=13306
   MYCNF
   chmod 600 ~/.my.cnf

8. Rollback
===========

Para deshabilitar un job temporalmente, comentar la linea en crontab:

.. code-block:: bash

   crontab -e
   # Agregar # al inicio de la linea del job a deshabilitar

9. Escalacion
=============

Si los scripts fallan repetidamente despues de verificar
precondiciones: escalar al equipo de DevOps con el contenido
de ``/var/log/iact/*.log`` y la salida de ``crontab -l``.

Ver :doc:`runbook-verificar-servicios` para diagnostico
de servicios de base de datos.

10. Trazabilidad
================

- Fuente: ``temp-holding/FASE 01/docs/operaciones/TASK-013-cron_jobs_maintenance.md``
- Scripts: ``scripts/cleanup_sessions.sh``, ``scripts/health_check.sh``,
  ``scripts/backup_data_centralization.sh``
- Restriccion relacionada: :doc:`/normativa/restricciones/cnst-002-buzon-interno-obligatorio`
