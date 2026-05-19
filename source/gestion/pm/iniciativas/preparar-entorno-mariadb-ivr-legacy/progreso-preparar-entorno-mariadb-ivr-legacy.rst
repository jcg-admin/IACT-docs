.. meta::
   :artefacto: PROGRESO-PREPARAR-ENTORNO-MARIADB-IVR-LEGACY
   :tipo: Progreso
   :dominio: gestion
   :subdominio: pm/iniciativas/preparar-entorno-mariadb-ivr-legacy
   :repo_objetivo: IACT-db
   :estado: COMPLETADA
   :version: 1.1.0
   :fecha_creacion: 2026-05-19T18:31:19
   :ultimo_cambio: 2026-05-19T18:35:48
   :autor: NestorMonroy
   :clasificacion: Interno

.. _progreso-preparar-entorno-mariadb-ivr-legacy:

==========================================================
Progreso: Preparar Entorno MariaDB ivr_legacy
==========================================================

Estado de tareas
=================

.. list-table::
   :header-rows: 1
   :widths: 8 6 50 16 20

   * - ID
     - Repo
     - Descripcion breve
     - Estado
     - Evidencia
   * - T-001
     - IACT-db
     - Instalar MariaDB + servicio activo
     - Completada
     - apt-get install OK; ``service mariadb start``
       reporta ``done``; ``mysqladmin ping`` = ``mysqld is
       alive``. Version: ``mysql Ver 15.1 Distrib
       10.11.14-MariaDB``.
   * - T-002
     - IACT-db
     - Generar .env desde .env.example
     - Completada
     - ``cp .env.example .env`` OK; valores clave
       confirmados: ``DB_MARIADB_NAME=ivr_legacy``,
       ``DB_MARIADB_USER=django_user``,
       ``MARIADB_HOST=127.0.0.1``,
       ``MARIADB_PORT=3306``.
   * - T-003
     - IACT-db
     - Crear BD + usuario + grants (setup.sh)
     - Completada
     - setup.sh 5/5 pasos OK: BD ``ivr_legacy``
       (utf8mb4/utf8mb4_unicode_ci) creada;
       ``django_user@%`` y ``django_user@localhost``
       creados; GRANT SELECT en ``ivr_legacy.*`` + GRANT
       CREATE/DROP en ``test_ivr_legacy.*``; conexion
       TCP y socket Unix OK; CNST-003 verificado
       (read-only).
   * - T-004
     - IACT-db
     - Aplicar funciones_utilidad.sql
     - Completada
     - 7 funciones en ``information_schema.routines``:
       ``fn_did_segmento``, ``fn_duracion_seg``,
       ``fn_normalizar_centro``, ``fn_normalizar_menu``,
       ``ivr_agregar_dias_semana``,
       ``ivr_contar_dias_semana``, ``ivr_es_dia_semana``.
       Pruebas de smoke ejecutadas en el propio script
       (sample outputs visibles en stdout).
   * - T-005
     - IACT-db
     - Aplicar schema_base_ivr.sql
     - Completada
     - 5 tablas creadas: ``base_ivr_clientes``,
       ``base_ivr_detalle``, ``etl_runs``,
       ``job_config`` (2 filas seed), ``job_execution_log``.
       Bonus: vista ``vw_monitor_dias_semana`` tambien
       definida por el script.
   * - T-006
     - IACT-db
     - Sembrar tbl_temp_prueba_ivr
     - Completada
     - 3000 registros insertados por lotes de 500;
       verificacion: COUNT=3000, todos con
       ``CHAR_LENGTH(numero)=10``. Muestra de 5 filas
       listada en el log de schema_seed.sh.
   * - T-007
     - IACT-db
     - Verificar conexion TCP django_user
     - Completada
     - ``mysql -h 127.0.0.1 -u django_user -pdjango_pass
       ivr_legacy -e "SELECT COUNT(*) FROM
       tbl_temp_prueba_ivr;"`` retorna ``3000``.
       ``information_schema.TABLES`` reporta las 6
       relaciones esperadas (5 tablas + 1 vista) + la
       tabla seed.

Conteo
=======

* Total: 7 tareas.
* Completadas: 7/7.
* En progreso: 0.
* Pendientes: 0.
* Bloqueadas: 0.

Inicio: 2026-05-19T18:31:19

Cierre: 2026-05-19T18:35:48

Historial
==========

.. list-table::
   :header-rows: 1
   :widths: 18 22 60

   * - Version
     - Fecha
     - Cambio
   * - 1.0.0
     - 2026-05-19T18:31:19
     - Creacion de la estructura de la iniciativa: index,
       alcance, analisis, tareas y progreso. Build dummy
       limpio en estructura.
   * - 1.1.0
     - 2026-05-19T18:35:48
     - Cierre: 7/7 tareas completadas (T-001..T-007).
       ivr_legacy operativa con esquema base + seed
       de pruebas. Conexion TCP django_user verificada.
       Decisiones documentadas en
       ``decisiones-preparar-entorno-mariadb-ivr-legacy``.
