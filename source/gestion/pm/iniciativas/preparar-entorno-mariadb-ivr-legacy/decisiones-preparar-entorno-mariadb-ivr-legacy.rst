.. meta::
   :artefacto: DECISIONES-PREPARAR-ENTORNO-MARIADB-IVR-LEGACY
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/preparar-entorno-mariadb-ivr-legacy
   :repo_objetivo: IACT-db
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:35:48
   :ultimo_cambio: 2026-05-19T18:35:48
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-preparar-entorno-mariadb-ivr-legacy:

==========================================================
Decisiones: Preparar Entorno MariaDB ivr_legacy
==========================================================

Decisiones de diseno
=====================

D1 — Instalacion via apt nativa en lugar de provisioners/mariadb/install.sh
-----------------------------------------------------------------------------

``provisioners/mariadb/install.sh`` instala MariaDB desde un
repositorio externo con version pinada
(``MARIADB_VERSION=11.4`` segun ``bootstrap.sh``;
``.env.example`` la baja a 10.11). En el contenedor de
desarrollo no hay garantia de acceso saliente al repositorio
externo de MariaDB. Considerado: usar el script tal cual y
fallar si no hay red al repo externo.

Decision tomada: instalar via ``apt-get install -y
mariadb-server mariadb-client`` directamente. El contenedor
Ubuntu 24.04 ofrece ``MariaDB 10.11.14``, que cumple
``MARIADB_VERSION=10.11`` del ``.env.example`` (la diferencia
con la version 11.4 nominal del bootstrap se atiende cuando
una iniciativa requiera caracteristicas exclusivas de 11.x;
los tests basicos no las necesitan).

D2 — :repo_objetivo: IACT-db sin commit en el repo objetivo
-------------------------------------------------------------

PROC-GOB-013 v2.0.0 (D3, Modelo C) permite que la
documentacion viva siempre en IACT-docs y la ejecucion ocurra
en el repo objetivo. En esta iniciativa la ejecucion es
**runtime puro**: instalar servicio, aplicar esquemas a la
BD, sembrar datos. No hay archivos versionados a tocar en
IACT-db.

Considerado: forzar algun commit en IACT-db (por ejemplo, un
``CHANGELOG`` o un ``manifest`` runtime). Se descarto:
introduce ruido de commits sin valor. La trazabilidad esta en
la propia iniciativa (progreso con evidencia por tarea).

Decision tomada: iniciativa con ``:repo_objetivo: IACT-db`` y
**cero commits en IACT-db**. Es el primer ejemplo del sistema
con ese patron. Si una iniciativa futura sobre IACT-db tiene
componente de codigo (nuevo script, fix de provisioner), abre
su rama y commitea normalmente. Este patron runtime queda
documentado como caso valido.

D3 — Scope minimo: base + seed, sin historicos ni objetos
-----------------------------------------------------------

``provisioners/mariadb/`` contiene mucho mas de lo aplicado:
``schema_historico.sql`` (tablas con volumen alto),
``seed_historico.sql`` / ``seed_historico_real.sql``
(historicos sembrados), ``objetos/{funciones,jobs,sps,vistas}/``.
Considerado: aplicar todo proactivamente para tener "la base
completa".

Se descarto por dos razones: (a) historicos sembrados pueden
tomar tiempo no trivial y agregan volumen al contenedor sin
demanda concreta; (b) ``objetos/`` contiene SPs/jobs que
asumen pipeline ETL operativo y no son prerequisito de
pruebas basicas.

Decision tomada: la iniciativa aplica el subset minimo
demostrado necesario por el script
``provisioners/mariadb/setup.sh`` y por la convencion del
``schema_seed.sh``. Las pruebas que requieran historicos o
SPs adicionales abren su propia iniciativa con el subset
minimo correspondiente.

D4 — funciones_utilidad.sql antes que schema_base_ivr.sql
-----------------------------------------------------------

El propio ``funciones_utilidad.sql`` declara: "PREREQUISITO de
todos los SPs del pipeline. Ejecutar antes que
schema_base_ivr.sql". El ``schema_base_ivr.sql`` no consulta
las funciones desde su DDL (es solo CREATE TABLE) pero sigue
la convencion del repo.

Decision tomada: respetar el orden documentado por IACT-db
aun cuando en este alcance no fuese estrictamente necesario.
Asi cualquier iniciativa siguiente que aplique
``sp_etl_pipeline.sql`` parte de un estado predecible.

D5 — PostgreSQL queda fuera del alcance
-----------------------------------------

``.env.example`` declara PostgreSQL 16 / ``iact_analytics`` /
``django_user``. El contenedor lo tiene instalado.
Considerado: aprovechar para preparar tambien
``iact_analytics``.

Se descarto: la solicitud del sponsor fue explicita sobre
MariaDB ("la base de datos de mysql, con informacion"). Las
pruebas IACT-api que requieren PostgreSQL no se han evaluado
en esta iniciativa. Abrir scope a PostgreSQL ahora
introduciria riesgo de fallar criterios no observados.

Decision tomada: PostgreSQL fuera de alcance. Queda como
deuda explicita (registrada abajo).

Hallazgos durante la ejecucion
================================

H-E1 — schema_base_ivr.sql tambien crea una vista (vw_monitor_dias_semana)
---------------------------------------------------------------------------

El alcance enuncia "5 tablas base" (``base_ivr_detalle``,
``base_ivr_clientes``, ``job_execution_log``, ``etl_runs``,
``job_config``). La ejecucion observada anade una vista
adicional ``vw_monitor_dias_semana``. No es ruptura: la vista
es parte del script ``schema_base_ivr.sql`` y consulta una de
las funciones de utilidad. Se registra como ajuste de
inventario, no como anomalia.

H-E2 — job_config se siembra con 2 filas por defecto
-----------------------------------------------------

``schema_base_ivr.sql`` no es DDL puro: el ``CREATE TABLE`` de
``job_config`` incluye ``INSERT`` de 2 filas semilla. No causo
problema (las filas son la configuracion canonica esperada
por el pipeline) y el script es idempotente
(``INSERT IGNORE`` o equivalente).

H-E3 — CWD persistente en Bash genera errores faciles entre repos
------------------------------------------------------------------

Lecion repetida de la iniciativa anterior
(``evolucionar-proc-gob-013-multirepo``, H-E4): el ``cd`` en
una llamada Bash persiste en llamadas siguientes y causa
``git push`` en el repo equivocado. Mitigacion aplicada: cada
comando que cambia de repo declara ``cd`` explicito.

No se trata como hallazgo de proyecto, sino como leccion
operacional para futuras iniciativas multi-repo. Se registra
aqui para reforzarla en la memoria escrita.

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 35 12 53

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - Servicio MariaDB activo con socket
       /run/mysqld/mysqld.sock
     - PASA
     - ``service mariadb start`` reporta ``done``;
       ``mysqladmin -uroot ping`` = ``mysqld is alive``;
       ``setup.sh`` paso 5 confirma "Conexion socket Unix
       OK: ivr_legacy@django_user@localhost".
   * - BD ivr_legacy con charset utf8mb4 y collation
       utf8mb4_unicode_ci
     - PASA
     - ``setup.sh`` paso 2: "Base de datos ivr_legacy
       creada (utf8mb4/utf8mb4_unicode_ci)".
   * - django_user@'%' y @'localhost' con grants
       READ-ONLY + CREATE/DROP en test_*
     - PASA
     - ``setup.sh`` pasos 3 y 4: usuarios creados, GRANT
       SELECT en ivr_legacy + GRANT CREATE/DROP en
       test_ivr_legacy. CNST-003 verificado:
       "django_user es READ-ONLY en ivr_legacy".
   * - 7 funciones/SPs de utilidad en ivr_legacy
     - PASA
     - ``information_schema.routines`` lista las 7:
       fn_did_segmento, fn_duracion_seg,
       fn_normalizar_centro, fn_normalizar_menu,
       ivr_agregar_dias_semana, ivr_contar_dias_semana,
       ivr_es_dia_semana.
   * - 5 tablas base + job_config con seed canonico
     - PASA
     - ``SHOW TABLES`` lista las 5 + 1 vista +
       tbl_temp_prueba_ivr. job_config con 2 filas
       confirmado en H-E2.
   * - tbl_temp_prueba_ivr con >= 3000 filas, todas con
       numero de 10 chars
     - PASA
     - ``schema_seed.sh`` paso 4: "tbl_temp_prueba_ivr:
       3000 registros"; "Todos los registros tienen
       numero de 10 caracteres".
   * - Conexion TCP django_user funcional
     - PASA
     - ``mysql -h 127.0.0.1 -u django_user
       -pdjango_pass ivr_legacy -e "SELECT COUNT(*)
       FROM tbl_temp_prueba_ivr;"`` retorna ``3000``.

Deuda nueva registrada
========================

* **DEBT-FUTURE-PG** (no asignada ID en deuda-tecnica-rebuild):
  iniciativa hermana para preparar el entorno PostgreSQL
  ``iact_analytics`` (D5). Aplica el mismo Modelo C: una
  iniciativa con ``:repo_objetivo: IACT-db`` que registra la
  aplicacion runtime. Pendiente de abrir cuando una prueba
  IACT-api que requiera PostgreSQL falle por
  conexion/esquema.
* **DEBT-FUTURE-HIST** (no asignada): aplicacion de
  ``schema_historico.sql`` + ``seed_historico.sql`` cuando
  una prueba especifica lo requiera (D3 del scope minimo).
* **DEBT-FUTURE-OBJETOS** (no asignada): aplicacion de
  ``provisioners/mariadb/objetos/`` cuando el pipeline ETL
  se ejercite (sp_etl_pipeline, jobs, vistas adicionales).

Estas tres deudas NO se registran en
``deuda-tecnica-rebuild.rst`` aun porque la regla del
proyecto pide IDs unicos y categoria; se documentan aqui como
hallazgos diferidos. Si el sponsor solicita formalizarlas,
abrir una iniciativa de auditoria que las catalogue.

Conclusion
==========

La iniciativa cumplio su criterio de completitud. La base
``ivr_legacy`` esta operativa en el contenedor con esquema
base y 3000 filas de seed. ``django_user`` puede leer por TCP.
Las pruebas IACT-api que dependen del ORM legacy ``ivr``
pueden ejecutarse. Patron de ``:repo_objetivo:`` distinto de
IACT-docs/multiple sin commit en el repo objetivo queda
establecido como Modelo C-runtime, ejemplo para iniciativas
futuras.
