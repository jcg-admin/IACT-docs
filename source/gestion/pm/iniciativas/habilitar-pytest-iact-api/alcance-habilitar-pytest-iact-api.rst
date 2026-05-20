.. meta::
   :artefacto: ALCANCE-HABILITAR-PYTEST-IACT-API
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/habilitar-pytest-iact-api
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:48:05
   :ultimo_cambio: 2026-05-19T18:48:05
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-habilitar-pytest-iact-api:

==============================================================
Alcance: Habilitar pytest en IACT-api
==============================================================

Por que existe
==============

Las pruebas del proyecto IACT viven primariamente en IACT-api
(1397 tests segun ``pytest --collect-only``). Sin el entorno
runtime de IACT-api en el contenedor, las pruebas no pueden
ejecutarse y los cambios futuros en api/ui no pueden
validarse. La cadena ``db -> api -> ui`` exige que api este
operativo: db lo alimenta, ui lo consume.

Estado inicial: IACT-api tiene ``requirements/{base,
development, testing, production}.txt`` y un Makefile de
provisioners (``scripts/``), pero el venv no existe, el
``.env`` no esta creado, y faltan paquetes del sistema
(``libmysqlclient-dev``, ``libpq-dev``) para compilar wheels
nativos.

Criterio de completitud verificable
=====================================

* Paquetes del sistema instalados:
  ``default-libmysqlclient-dev``, ``libpq-dev``,
  ``build-essential``, ``pkg-config``.
* venv Python 3.11 creado en ``IACT-api/.venv`` con
  ``requirements/development.txt`` instalado
  (incluye base + testing).
* ``IACT-api/.env`` y ``IACT-api/callcentersite/.env``
  creados con credenciales que apuntan a las bases del
  contenedor (PostgreSQL ``127.0.0.1:5432`` /
  MariaDB ``127.0.0.1:3306``).
* ``IACT-api/logs/`` creado (requerido por el handler
  ``logging.RotatingFileHandler`` declarado en
  ``config/settings/base.py``).
* ``python manage.py check`` produce
  ``System check identified no issues``.
* ``python manage.py migrate`` aplica todas las migraciones
  contra PostgreSQL ``iact_analytics`` sin error.
* ``pytest --collect-only`` reporta tests colectados.
* ``pytest -m unit`` ejecuta y reporta 0 fallas.

In-scope
========

* Instalacion de paquetes apt requeridos para compilar
  ``mysqlclient`` y ``psycopg2``.
* Creacion del venv y instalacion de ``development.txt``
  (cubre base + testing + django-extensions necesario por
  ``settings/development.py``).
* Generacion del ``.env`` con valores apuntando a las DBs
  del contenedor. Dos copias: raiz del repo (para
  ``setup.cfg`` / herramientas) y dentro de
  ``callcentersite/`` (donde ``decouple`` lo busca por cwd).
* Aplicacion de migraciones Django sobre
  ``iact_analytics``.
* Verificacion smoke con ``pytest -m unit``.

Out-of-scope
============

* Cualquier trabajo sobre ``uc-opr-*``, ``uc-sup-*`` y
  ``uc-cli-01..05``.
* Ejecucion de la suite completa de 1397 tests: marca de
  unit son 223 tests y son suficientes para validar
  integracion runtime. La suite ``integration`` y ``api``
  puede requerir fixtures adicionales y se valida en
  iniciativas que las necesiten.
* Despliegue de IACT-api como servicio (gunicorn/Apache).
  La iniciativa habilita el modo dev/test, no el modo
  produccion.
* Configuracion de Sentry, Redis, Celery o Channels:
  prohibidos por CNST_TECNICAS de IACT-api v2.2.1.
* Coverage report agregado, gates de cobertura: deuda
  diferida.
* Habilitar pytest en IACT-ui (eslabon siguiente, requiere
  iniciativa propia tras esta).

Decisiones de contenido tomadas durante la lectura
====================================================

* Se elige ``requirements/development.txt`` en lugar de
  ``testing.txt`` porque las settings ``development.py``
  importan ``django_extensions`` (no esta en testing.txt
  segun H-E1 de las decisiones).
* Settings ``testing_local`` se usa explicitamente en cada
  comando (``DJANGO_SETTINGS_MODULE=config.settings.testing_local``):
  ``manage.py`` por defecto carga ``development``, que
  intenta abrir el server de migraciones distinto.
