.. meta::
   :artefacto: ALCANCE-PREPARAR-ENTORNO-MARIADB-IVR-LEGACY
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/preparar-entorno-mariadb-ivr-legacy
   :repo_objetivo: IACT-db
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:31:19
   :ultimo_cambio: 2026-05-19T18:31:19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-preparar-entorno-mariadb-ivr-legacy:

==========================================================
Alcance: Preparar Entorno MariaDB ivr_legacy
==========================================================

Por que existe
==============

Las pruebas de IACT-api dependen del ORM legacy ``ivr`` que
conecta contra MariaDB con la base de datos ``ivr_legacy``. En
produccion ``tbl_historico_*`` tiene 11-14M filas; el entorno
de pruebas no puede replicar ese volumen ni lo necesita — usa
cantidades simuladas suficientes para validar la logica de
queries, stored procedures y mappers Django.

El repositorio IACT-db ya provee los scripts de provisionamiento
en ``provisioners/mariadb/`` (bootstrap, setup, schema base,
seed). Esta iniciativa los aplica en el contenedor de
desarrollo y deja la base en estado utilizable, con
documentacion trazable de que se ejecuto, contra que version y
que verificacion se hizo. Sin ese registro la sesion siguiente
no sabe si la BD existe, ni con que datos.

Criterio de completitud verificable
=====================================

* Servicio ``mariadb`` activo en el contenedor con socket Unix
  en ``/run/mysqld/mysqld.sock`` accesible para root.
* Base de datos ``ivr_legacy`` existe con charset
  ``utf8mb4`` y collation ``utf8mb4_unicode_ci``.
* Usuario ``django_user`` existe en hosts ``%`` y ``localhost``
  con la contraseña declarada en ``.env``, con privilegios
  ``SELECT`` en ``ivr_legacy.*`` (CNST-003) y
  ``CREATE/DROP/INDEX/ALTER`` en ``test_ivr_legacy.*``.
* ``funciones_utilidad.sql`` aplicado: las 7 funciones/SPs de
  utilidad existen en ``ivr_legacy``.
* ``schema_base_ivr.sql`` aplicado: las 5 tablas base
  (``base_ivr_detalle``, ``base_ivr_clientes``,
  ``job_execution_log``, ``etl_runs``, ``job_config``) existen.
* ``schema_seed.sh`` ejecutado: ``tbl_temp_prueba_ivr`` tiene
  al menos ``SEED_ROWS`` registros (3000 por defecto), todos
  con ``numero`` de 10 caracteres.
* Conexion TCP desde ``django_user`` (host 127.0.0.1, puerto
  3306) verificada con ``SELECT 1`` sobre ``ivr_legacy``.

In-scope
========

* Generacion local de ``IACT-db/.env`` a partir de
  ``.env.example`` (archivo gitignored — no hay commit en
  IACT-db).
* Aseguramiento del servicio MariaDB activo (instalado desde
  ``apt`` como evidencia colateral de esta sesion).
* Ejecucion de ``provisioners/mariadb/setup.sh`` (creacion
  idempotente de BD, usuario y grants).
* Aplicacion de ``provisioners/mariadb/funciones_utilidad.sql``
  via ``mysql --batch < ...`` (las funciones usan
  ``DELIMITER`` y no se pueden cargar con ``-e``).
* Aplicacion de ``provisioners/mariadb/schema_base_ivr.sql``
  por el mismo metodo.
* Ejecucion de ``provisioners/mariadb/schema_seed.sh`` para
  poblar ``tbl_temp_prueba_ivr`` con 3000 filas simuladas.
* Captura de la evidencia de cada paso (conteos, exit code,
  fragmento de salida) en el documento de progreso y, al
  cierre, en el documento de decisiones.

Out-of-scope
============

* Cualquier trabajo sobre los casos de uso ``uc-opr-*``,
  ``uc-sup-*`` y ``uc-cli-01..05``: declarados explicitamente
  fuera de scope por el sponsor; no se realizan ni se
  implementan.
* ``schema_historico.sql`` y ``seed_historico.sql`` (tablas
  ``tbl_historico_*`` con volumenes grandes). La iniciativa
  cubre el subset minimo necesario para que pasen las pruebas
  basicas; si una prueba especifica requiere historico, se abre
  una iniciativa dedicada con el subset minimo simulado.
* ``provisioners/mariadb/objetos/`` (funciones, jobs, sps,
  vistas adicionales): se aplican cuando una iniciativa
  posterior lo demande, no proactivamente.
* PostgreSQL ``iact_analytics``: queda como deuda nueva. El
  scope se limita al motor MariaDB porque la solicitud del
  sponsor menciona MySQL/MariaDB explicitamente y porque los
  tests de IACT-api que dependen de PostgreSQL no se han
  evaluado en esta iniciativa.
* Instalacion de Adminer (UI web). Innecesario para CI/runtime
  y agrega un servicio mas a mantener.
* Snapshot/backup automatizados. Otro repo
  (``backup_ivr_legacy.sh``) gobierna eso; queda fuera del
  alcance de preparar el entorno inicial.

Decisiones de contenido tomadas durante la lectura
====================================================

* La iniciativa se clasifica como **documental** (no hay
  Project Charter) aunque su ``:repo_objetivo:`` sea
  ``IACT-db``. La documentacion vive en IACT-docs por el
  Modelo C de PROC-GOB-013 v2.0.0 (D3 de
  ``evolucionar-proc-gob-013-multirepo``).
* MariaDB se instala con ``apt-get install
  mariadb-server mariadb-client`` (no via
  ``provisioners/mariadb/install.sh``). Razon: en el
  contenedor el script de install asume manejo de
  repositorios externos y version pinada que no aplica al
  entorno efimero. El ``apt`` del contenedor da MariaDB 10.11,
  alineado con ``MARIADB_VERSION=10.11`` de ``.env.example``.
  Decision documentada en el cierre.
* No se commitea nada al repo IACT-db: ``.env`` esta en
  ``.gitignore`` y los esquemas/seed ya existen en
  ``provisioners/mariadb/``. La iniciativa documenta una
  **aplicacion runtime**, no un cambio de codigo. Es el
  primer ejemplo del sistema con ``:repo_objetivo:`` sin
  commit en el repo objetivo.
