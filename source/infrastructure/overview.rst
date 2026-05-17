.. meta::
   :artefacto: INFRASTRUCTURE-OVERVIEW
   :tipo: Overview
   :dominio: infrastructure
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-16T23:01:11
   :ultimo_cambio: 2026-05-16T23:01:11
   :autor: NestorMonroy
   :clasificacion: Interno

.. _infrastructure-overview:

========================
Infrastructure Overview
========================

.. note::

   Topologia del entorno de servidor IACT. El entorno de desarrollo
   replica la infraestructura de produccion mediante una VM Vagrant.
   Ver :doc:`conventions` para naming, paths y puertos.

Topologia general
=================

.. code-block:: text

   Cliente (browser / API consumer)
          |
          | HTTP/HTTPS
          v
   Apache 2.4 (reverse proxy + static files)
          |
          | mod_wsgi (WSGI interface)
          v
   Django (WSGI application)
          |
          +---> PostgreSQL 127.0.0.1:15432  (iact_analytics — escritura)
          |
          +---> MariaDB    127.0.0.1:13306  (iact_ivr — solo lectura)

Entorno de desarrollo — VM Vagrant
====================================

El entorno de desarrollo usa Vagrant + VirtualBox para replicar
la infraestructura de produccion de forma aislada y reproducible.

**Decision:** :doc:`/devops/adr-devops-001-vagrant-mod-wsgi-importante-produc`

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Box**
     - ``ubuntu/focal64`` (Ubuntu 20.04 LTS)
   * - **Provider**
     - VirtualBox 7+
   * - **RAM**
     - 2048 MB
   * - **CPUs**
     - 2
   * - **Inicio**
     - ``vagrant up`` (~3 min primera vez, ~1.5 min subsecuente)

Puertos expuestos (host → guest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Host
     - Guest
     - Servicio
   * - 127.0.0.1:15432
     - 5432
     - PostgreSQL (iact_analytics)
   * - 127.0.0.1:13306
     - 3306
     - MariaDB (iact_ivr, read-only)

Apache + mod_wsgi
==================

Django se sirve mediante Apache 2.4 con mod_wsgi. Apache actua
como reverse proxy para requests dinamicos y sirve directamente
los archivos estaticos.

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Servidor web**
     - Apache 2.4
   * - **Interface WSGI**
     - mod_wsgi
   * - **Aplicacion**
     - Django (``callcentersite/wsgi.py``)
   * - **Archivos estaticos**
     - servidos directamente por Apache desde ``/static/``

Bases de datos
==============

.. list-table::
   :widths: 20 20 20 40
   :header-rows: 1

   * - Motor
     - Puerto
     - Base de datos
     - Rol
   * - PostgreSQL
     - 15432
     - iact_analytics
     - Escritura — datos analiticos IACT
   * - MariaDB
     - 13306
     - iact_ivr
     - Solo lectura — datos operativos IVR

**Restriccion:** La BD IVR es read-only para IACT per
:doc:`/normativa/restricciones/cnst-001-prohibicion-de-email-y-smtp`.

Aprovisionamiento
==================

El script ``provisioning/bootstrap.sh`` provisiona la VM
automaticamente al ejecutar ``vagrant up`` por primera vez:

- Instala PostgreSQL, MariaDB, Apache, mod_wsgi
- Crea usuarios y bases de datos con los permisos correctos
- Configura el virtual host de Apache para Django

Ver :doc:`/devops/runbooks/runbook-verificar-servicios` para
verificar el estado de los servicios despues del aprovisionamiento.
