.. meta::
   :artefacto: TAREAS-Y-PROGRESO-HABILITAR-PYTEST-IACT-API
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/habilitar-pytest-iact-api
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:48:05
   :ultimo_cambio: 2026-05-19T18:48:05
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-habilitar-pytest-iact-api:

==============================================================
Tareas y Progreso: Habilitar pytest en IACT-api
==============================================================

Iniciativa runtime; las tareas modifican estado del contenedor
y archivos gitignored, no archivos versionados. Trazabilidad
por evidencia textual de cada paso.

Lista de tareas
================

.. list-table::
   :header-rows: 1
   :widths: 6 4 30 60

   * - ID
     - Repo
     - Descripcion
     - Resultado / Evidencia
   * - T-001
     - IACT-api
     - Instalar paquetes apt para compilar
       extensiones nativas:
       ``default-libmysqlclient-dev``,
       ``libpq-dev``,
       ``build-essential``, ``pkg-config``.
     - Completada. ``apt-get install`` reporta
       "Setting up libpq-dev",
       "libmysqlclient-dev",
       "default-libmysqlclient-dev". Sin errores.
   * - T-002
     - IACT-api
     - Crear venv Python 3.11 e instalar
       ``requirements/development.txt`` (cubre
       base + testing + django-extensions).
     - Completada. Venv en ``IACT-api/.venv``;
       ``pip list`` muestra ``Django 5.0.1``,
       ``pytest 7.4.4``, ``mysqlclient 2.2.1``,
       ``psycopg2-binary 2.9.9``,
       ``django-extensions 3.2.3``.
   * - T-003
     - IACT-api
     - Generar ``.env`` con credenciales hacia
       PostgreSQL y MariaDB del contenedor.
       Copia tambien en ``callcentersite/`` por
       D2 (decouple cwd).
     - Completada. ``decouple.config('DB_HOST')``
       retorna ``127.0.0.1`` desde cwd
       ``callcentersite/``. Variables:
       ``DB_NAME=iact_analytics``,
       ``IVR_DB_NAME=ivr_legacy``,
       socket Unix mariadb declarado.
   * - T-004
     - IACT-api
     - Crear directorio ``logs/`` requerido por
       handler ``RotatingFileHandler`` en
       ``base.py``.
     - Completada. ``mkdir -p logs/`` en raiz
       del repo. ``manage.py check`` ya no falla
       por handler.
   * - T-005
     - IACT-api
     - Ejecutar
       ``manage.py check`` con settings
       ``testing_local``.
     - Completada. Salida: "System check
       identified no issues (0 silenced)".
       Schedulers reportan "NOT started
       (management command)" — esperado.
   * - T-006
     - IACT-api
     - ``manage.py migrate`` sobre
       PostgreSQL ``iact_analytics``.
     - Completada. Migraciones de todas las apps
       aplicadas. Ultimas registradas:
       ``reports.0006_fase5_savedfilter_savedview_canonical``,
       ``users.0005_sync_state_field``,
       ``sessions.0001_initial``.
   * - T-007
     - IACT-api
     - ``pytest --collect-only`` para inventariar.
     - Completada. "1397 tests collected in
       2.08s". Sin errores de colection.
   * - T-008
     - IACT-api
     - ``pytest -m unit`` como smoke test.
     - Completada. "223 passed, 1174
       deselected in 35.68s". 0 failures,
       0 errors.

Conteo
=======

* Total: 8 tareas.
* Completadas: 8/8.
* Pendientes: 0.
* Bloqueadas: 0.

Inicio: 2026-05-19T18:48:05

Cierre: 2026-05-19T18:48:05

Historial
==========

.. list-table::
   :header-rows: 1
   :widths: 18 22 60

   * - Version
     - Fecha
     - Cambio
   * - 1.0.0
     - 2026-05-19T18:48:05
     - Apertura y cierre simultaneos. Ejecucion
       lineal exitosa con un solo bloqueo
       intermedio resuelto (T-001 prerequisito
       de T-002).
