.. meta::
   :artefacto: INICIATIVA-HABILITAR-PYTEST-IACT-API
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:48:05
   :ultimo_cambio: 2026-05-19T18:48:05
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-habilitar-pytest-iact-api:

==============================================================
Iniciativa: Habilitar pytest en IACT-api
==============================================================

Lleva el eslabon ``api`` de la cadena ``db -> api -> ui`` al
estado "runnable": pytest puede colectar la suite completa y
ejecutar al menos el subset ``unit`` con 0 fallas. Toma como
prerequisitos las iniciativas hermanas
``preparar-entorno-mariadb-ivr-legacy`` y
``preparar-entorno-postgresql-iact-analytics`` (ambas
cerradas) y verifica end-to-end que IACT-api se conecta a las
dos bases.

Patron Modelo C-runtime (PROC-GOB-013 v2.0.0 D3) con
``:repo_objetivo: IACT-api``: documentacion en IACT-docs,
ejecucion en IACT-api. Sin commits en IACT-api porque el
trabajo es runtime puro (instalacion de paquetes apt,
creacion de venv, generacion de ``.env`` gitignored, ejecucion
de migrate y pytest). Las dependencias declaradas
(``requirements/*.txt``) ya existian en IACT-api.

.. toctree::
   :maxdepth: 1

   alcance-habilitar-pytest-iact-api
   tareas-y-progreso-habilitar-pytest-iact-api
   decisiones-habilitar-pytest-iact-api
