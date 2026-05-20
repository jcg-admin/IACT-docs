.. meta::
   :artefacto: ANALISIS-PREPARAR-ENTORNO-MARIADB-IVR-LEGACY
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/preparar-entorno-mariadb-ivr-legacy
   :repo_objetivo: IACT-db
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:31:19
   :ultimo_cambio: 2026-05-19T18:31:19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _analisis-preparar-entorno-mariadb-ivr-legacy:

==========================================================
Analisis: Preparar Entorno MariaDB ivr_legacy
==========================================================

Estado inicial observado en el contenedor
============================================

* MariaDB no estaba instalado al inicio de la sesion (``which
  mariadb`` vacio; ``mysql`` solo provisto por
  ``libpq5``-relacionados no, sino ausente).
* PostgreSQL 16 si estaba instalado (``psql``, ``pg_isready``
  presentes; paquete ``postgresql-16``).
* El usuario corre como ``root`` en el contenedor — no se
  necesita ``sudo``.
* El repositorio IACT-db tiene ``.env.example`` con la
  configuracion canonica; ``.env`` no existia (esta en
  ``.gitignore``).

Componentes que el repositorio IACT-db provee
================================================

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Componente
     - Funcion
   * - ``bootstrap.sh``
     - Orquesta install + config + setup + verify para todo
       el stack (MariaDB + PostgreSQL + Adminer).
   * - ``provisioners/mariadb/install.sh``
     - Instala MariaDB via apt + repositorio externo con
       version pinada (``MARIADB_VERSION=11.4`` por defecto en
       ``bootstrap.sh``; ``.env.example`` la baja a 10.11).
   * - ``provisioners/mariadb/config.sh``
     - Ajustes de ``my.cnf`` (bind-address, charset).
   * - ``provisioners/mariadb/setup.sh``
     - Crea BD ``ivr_legacy``, usuario ``django_user@'%'`` y
       ``@'localhost'``, GRANT SELECT en
       ``ivr_legacy.*`` (CNST-003), GRANT CREATE/DROP/INDEX/
       ALTER en ``test_ivr_legacy.*`` para pytest.
   * - ``provisioners/mariadb/funciones_utilidad.sql``
     - 7 funciones/SPs prerequisito de ``schema_base_ivr.sql``
       (``fn_did_segmento``, ``fn_normalizar_menu``, etc.).
   * - ``provisioners/mariadb/schema_base_ivr.sql``
     - 5 tablas base: ``base_ivr_detalle``,
       ``base_ivr_clientes``, ``job_execution_log``,
       ``etl_runs``, ``job_config``.
   * - ``provisioners/mariadb/schema_seed.sh``
     - Tabla ``tbl_temp_prueba_ivr`` (id INT
       AUTO_INCREMENT, numero CHAR(10)) y 3000 filas
       sembradas via INSERT por lotes.
   * - ``provisioners/mariadb/schema_historico.sql``
     - Tablas ``tbl_historico_*`` (volumen grande). Fuera
       de scope.
   * - ``provisioners/mariadb/objetos/``
     - SPs/funciones/jobs/vistas adicionales. Fuera de scope.
   * - ``verify.sh``
     - Verificacion completa (7 secciones, contadores
       OK/WARN/ERR).

Gaps a cerrar
==============

.. list-table::
   :header-rows: 1
   :widths: 10 35 55

   * - ID
     - Gap
     - Solucion
   * - G-01
     - MariaDB no instalado en el contenedor.
     - Instalar ``mariadb-server`` y ``mariadb-client`` via
       ``apt-get`` (10.11). No usar
       ``provisioners/mariadb/install.sh`` (depende de
       repositorios externos no disponibles).
   * - G-02
     - Sin ``.env`` en IACT-db.
     - ``cp .env.example .env`` (idempotente; ``.env`` esta
       gitignored — no hay commit).
   * - G-03
     - Base de datos ``ivr_legacy`` no existe.
     - Ejecutar ``provisioners/mariadb/setup.sh`` (idempotente).
   * - G-04
     - Usuario ``django_user`` no existe.
     - Cubierto por ``setup.sh`` (paso 3) en ``@'%'`` y
       ``@'localhost'``.
   * - G-05
     - Esquema base no aplicado.
     - ``mysql ivr_legacy < funciones_utilidad.sql`` (orden
       importante por dependencias) y
       ``mysql ivr_legacy < schema_base_ivr.sql``. No usar
       ``mysql -e`` por DELIMITER en los SPs.
   * - G-06
     - Sin datos de prueba para
       ``tbl_temp_prueba_ivr``.
     - Ejecutar
       ``provisioners/mariadb/schema_seed.sh`` (3000 filas
       por defecto).
   * - G-07
     - Sin verificacion de conexion como
       ``django_user`` por TCP.
     - ``mysql -h 127.0.0.1 -u django_user -pdjango_pass
       ivr_legacy -e "SELECT 1;"``.

Priorizacion
=============

Todos los gaps son **Must**: sin ellos las pruebas no corren.
No hay Should ni Could en este alcance.

Cobertura analisis -> tarea
============================

.. list-table::
   :header-rows: 1
   :widths: 8 8 30 54

   * - Gap
     - Tarea
     - Comando ejecutado
     - Resultado esperado
   * - G-01
     - T-001
     - ``apt-get install mariadb-server mariadb-client``
     - Servicio ``mariadb`` activo.
   * - G-02
     - T-002
     - ``cp .env.example .env``
     - ``.env`` presente con valores por defecto.
   * - G-03, G-04
     - T-003
     - ``bash provisioners/mariadb/setup.sh``
     - BD + usuarios + grants creados.
   * - G-05 (funciones)
     - T-004
     - ``mysql ivr_legacy < funciones_utilidad.sql``
     - 7 funciones/SPs en ``ivr_legacy``.
   * - G-05 (schema)
     - T-005
     - ``mysql ivr_legacy < schema_base_ivr.sql``
     - 5 tablas base en ``ivr_legacy``.
   * - G-06
     - T-006
     - ``bash provisioners/mariadb/schema_seed.sh``
     - ``tbl_temp_prueba_ivr`` con >= 3000 filas.
   * - G-07
     - T-007
     - ``mysql -h 127.0.0.1 -u django_user
       -pdjango_pass ivr_legacy -e "SELECT 1;"``
     - Resultado ``1`` retornado.

Casos especiales detectados
=============================

* ``provisioners/mariadb/setup.sh`` ya hace verificacion TCP
  como paso 5. Si pasa, T-007 puede absorberse como
  evidencia del log; se conserva como tarea explicita para
  trazabilidad propia de la iniciativa.
* ``funciones_utilidad.sql`` y ``schema_base_ivr.sql`` no
  estan invocados desde ``bootstrap.sh``: la pipeline
  oficial del repo IACT-db los considera optativos
  (dependientes de la iniciativa que los necesite). Esta
  iniciativa los aplica explicitamente.
* El ``setup.sh`` paso 5 tambien intenta conexion via
  socket Unix; ``IACT-api`` lo necesita en produccion. Se
  conserva la conexion socket como evidencia colateral.
