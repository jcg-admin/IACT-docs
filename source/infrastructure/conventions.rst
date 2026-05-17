.. meta::
   :artefacto: INFRASTRUCTURE-CONVENTIONS
   :tipo: Conventions
   :dominio: infrastructure
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-16T23:01:11
   :ultimo_cambio: 2026-05-16T23:01:11
   :autor: NestorMonroy
   :clasificacion: Interno

.. _infrastructure-conventions:

============================
Infrastructure Conventions
============================

.. note::

   Convenciones de naming, paths, puertos y logging del entorno
   IACT. Aplica tanto al entorno de desarrollo (Vagrant) como
   al entorno de produccion.

Puertos
=======

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Puerto (host)
     - Puerto (guest/prod)
     - Servicio
   * - 127.0.0.1:15432
     - 5432
     - PostgreSQL — iact_analytics
   * - 127.0.0.1:13306
     - 3306
     - MariaDB — iact_ivr (read-only)
   * - 80 / 443
     - 80 / 443
     - Apache (HTTP / HTTPS)
   * - 8000
     - 8000
     - Django dev server (solo desarrollo directo)

Los puertos del host usan prefijo ``1`` para evitar conflictos
con instalaciones nativas en la maquina del desarrollador.

Paths del proyecto
==================

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - Path
     - Contenido
   * - ``/home/user/IACT---project/``
     - Raiz del proyecto (montado desde host via Vagrant)
   * - ``/home/user/IACT---project/api/callcentersite/``
     - Aplicacion Django
   * - ``/home/user/IACT---project/scripts/``
     - Scripts operativos (cleanup, health_check, backup)
   * - ``/home/user/IACT---project/provisioning/``
     - Scripts de aprovisionamiento Vagrant
   * - ``/etc/apache2/sites-available/iact.conf``
     - Configuracion del virtual host Apache
   * - ``/var/log/iact/``
     - Logs operativos (cleanup, health, backup)
   * - ``/var/log/apache2/``
     - Logs de Apache (access.log, error.log)
   * - ``/var/backups/``
     - Backups de bases de datos

Credenciales de base de datos
==============================

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Campo
     - Valor
     - Notas
   * - Usuario
     - ``django_user``
     - Usuario de aplicacion para ambas BDs
   * - Password
     - ``django_pass``
     - Solo desarrollo local — produccion usa variables de entorno
   * - PostgreSQL DB
     - ``iact_analytics``
     - Base de datos analitica de IACT
   * - MariaDB DB
     - ``iact_ivr``
     - Base de datos IVR (acceso read-only)

.. admonition:: Seguridad

   Las credenciales de produccion nunca se hardcodean.
   Se configuran via variables de entorno o archivo
   ``.env`` excluido de version control.

Convenciones de logging
========================

Todos los logs operativos van a ``/var/log/iact/``:

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Archivo
     - Contenido
   * - ``/var/log/iact/cleanup.log``
     - Salida de ``cleanup_sessions.sh`` (cada 6h)
   * - ``/var/log/iact/health.log``
     - Salida de ``health_check.sh`` (cada 5 min)
   * - ``/var/log/iact/backup.log``
     - Salida de ``backup_data_centralization.sh`` (2AM)

Formato: JSON estructurado. Retention: ver
:doc:`/devops/runbooks/runbook-log-retention-policies`.

Convenciones de naming del entorno
====================================

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Entorno
     - Identificador
   * - Desarrollo local
     - ``iact-dev`` (VM Vagrant)
   * - Staging
     - ``iact-staging``
   * - Produccion
     - ``iact-prod``

Variables de entorno requeridas
================================

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Variable
     - Uso
   * - ``MYSQL_PASSWORD``
     - Password de MariaDB para scripts de backup
   * - ``DJANGO_SECRET_KEY``
     - Secret key de Django (produccion)
   * - ``DATABASE_URL``
     - URL de conexion PostgreSQL (produccion)

Trazabilidad
============

- Topologia completa: :doc:`overview`
- Cron jobs y logs: :doc:`/devops/runbooks/runbook-cron-jobs-mantenimiento`
- Verificacion de servicios: :doc:`/devops/runbooks/runbook-verificar-servicios`
