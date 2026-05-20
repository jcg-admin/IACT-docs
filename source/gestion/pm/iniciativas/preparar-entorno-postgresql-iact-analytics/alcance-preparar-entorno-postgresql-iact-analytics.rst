.. meta::
   :artefacto: ALCANCE-PREPARAR-ENTORNO-POSTGRESQL-IACT-ANALYTICS
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/preparar-entorno-postgresql-iact-analytics
   :repo_objetivo: IACT-db
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:40:45
   :ultimo_cambio: 2026-05-19T18:40:45
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-preparar-entorno-postgresql-iact-analytics:

==============================================================
Alcance: Preparar Entorno PostgreSQL iact_analytics
==============================================================

Por que existe
==============

IACT-api tiene dos bases de datos declaradas: ``ivr_legacy``
(MariaDB, READ-ONLY, ya cubierta por la iniciativa hermana
``preparar-entorno-mariadb-ivr-legacy``) y ``iact_analytics``
(PostgreSQL 16, default Django). Sin la segunda, ``manage.py
migrate`` ni los tests pueden ejecutarse: Django falla al
abrir conexion default.

PostgreSQL 16 ya estaba instalado en el contenedor, pero el
cluster ``16/main`` estaba detenido. El repositorio IACT-db
provee ``provisioners/postgres/setup.sh`` para crear BD,
usuario, grants y extensiones.

Criterio de completitud verificable
=====================================

* Cluster PostgreSQL 16 ``main`` arriba, ``pg_isready`` retorna
  ``accepting connections`` en ``127.0.0.1:5432``.
* Base de datos ``iact_analytics`` existe.
* Usuario ``django_user`` existe con la contraseña declarada
  en ``.env``, con privilegios sobre ``iact_analytics.*`` y
  ``CREATEDB`` (necesario para que pytest cree
  ``test_iact_analytics``).
* Extensiones ``uuid-ossp``, ``pg_trgm``, ``hstore`` y
  ``citext`` instaladas en ``iact_analytics``.
* Conexion como ``django_user`` verificada.

In-scope
========

* Arranque del cluster PostgreSQL 16 ``main`` via
  ``pg_ctlcluster``.
* Ejecucion de ``provisioners/postgres/setup.sh`` (creacion
  idempotente).
* Verificacion de conexion como ``django_user``.

Out-of-scope
============

* Cualquier trabajo sobre ``uc-opr-*``, ``uc-sup-*`` y
  ``uc-cli-01..05``.
* Migraciones de Django (``manage.py migrate``): pertenecen al
  alcance de la iniciativa de IACT-api que sigue.
* Tuning de PostgreSQL (``postgresql.conf``,
  ``pg_hba.conf``): el default del cluster 16/main funciona
  para tests; tuning es deuda futura.
* Carga de datos analiticos reales: ``iact_analytics`` queda
  vacia (las migraciones de Django llenan su DDL; las pruebas
  pueden cargar fixtures).
