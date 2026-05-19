.. meta::
   :artefacto: INICIATIVA-PREPARAR-ENTORNO-POSTGRESQL-IACT-ANALYTICS
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-db
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:40:45
   :ultimo_cambio: 2026-05-19T18:40:45
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-preparar-entorno-postgresql-iact-analytics:

==============================================================
Iniciativa: Preparar Entorno PostgreSQL iact_analytics
==============================================================

Completa el par de bases que IACT-api necesita: la base por
defecto de Django ``iact_analytics`` en PostgreSQL 16. Sin
ella, ``manage.py migrate`` y los tests Django fallan al
primer ``setUp``.

Iniciativa hermana de ``preparar-entorno-mariadb-ivr-legacy``.
Sigue el mismo patron Modelo C-runtime (PROC-GOB-013 v2.0.0
D3): documentacion en IACT-docs, ejecucion en IACT-db.
Reconoce la cadena ``db -> api -> ui``: PostgreSQL es la mitad
faltante del eslabon ``db``; sin ella el eslabon ``api`` no
arranca.

.. toctree::
   :maxdepth: 1

   alcance-preparar-entorno-postgresql-iact-analytics
   tareas-y-progreso-preparar-entorno-postgresql-iact-analytics
   decisiones-preparar-entorno-postgresql-iact-analytics
