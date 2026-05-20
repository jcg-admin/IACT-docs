.. meta::
   :artefacto: DECISIONES-HABILITAR-PYTEST-IACT-API
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/habilitar-pytest-iact-api
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:48:05
   :ultimo_cambio: 2026-05-19T18:48:05
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-habilitar-pytest-iact-api:

==============================================================
Decisiones: Habilitar pytest en IACT-api
==============================================================

Decisiones de diseno
=====================

D1 — development.txt en lugar de testing.txt
----------------------------------------------

``settings/development.py`` importa ``django_extensions``
en ``INSTALLED_APPS``. ``testing.txt`` no lo incluye (solo
``base + pytest + factory-boy``). Considerado: usar
``testing.txt`` y ajustar settings para excluir
``django_extensions`` cuando no esta presente.

Decision tomada: instalar ``development.txt`` que
incluye django-extensions. Costo extra (debug-toolbar,
ipython, black, flake8) es bajo y elimina divergencias entre
"setup local de desarrollo" y "setup de pruebas". El gate
real de los tests es ``DJANGO_SETTINGS_MODULE=testing_local``
en la invocacion.

D2 — Dos copias de .env (raiz y callcentersite/)
--------------------------------------------------

``python-decouple`` busca ``.env`` con ``AutoConfig`` desde
``os.getcwd()`` recursivamente hacia arriba. Las
invocaciones de ``manage.py`` desde
``IACT-api/callcentersite/`` no encontraban el ``.env`` de
``IACT-api/``: ``config('DB_HOST')`` retornaba ``NOTSET``,
psycopg2 caia a socket Unix por default y fallaba con "Peer
authentication failed".

Considerado: usar ``decouple.Config('/path/.env')`` explicito.
Se descarto: requiere modificar ``base.py``, codigo
versionado, para un problema de entorno local.

Decision tomada: dejar ``.env`` en dos rutas (``IACT-api/``
y ``IACT-api/callcentersite/``). Ambos son gitignored. Es un
duplicado tolerable de un archivo de 20 lineas; la fuente
de verdad sigue siendo el primero y el segundo se copia con
``cp`` al final del setup. Si en una sesion siguiente se
actualiza, debe replicarse a las dos rutas.

Documentar este patron como deuda menor: el codigo de
IACT-api podria usar un repositorio explicito para
``.env`` y dejar de depender del cwd.

D3 — DJANGO_SETTINGS_MODULE explicito en cada comando
-------------------------------------------------------

``manage.py`` por defecto usa
``config.settings.development`` (DEBUG=True). El gate de
tests usa ``testing_local`` por ``pytest.ini``. Pero
``manage.py migrate`` se ejecuta fuera de pytest y usaria
``development`` por default — settings cuyo throttle y
caches no son los de tests.

Considerado: cambiar el default de ``manage.py`` a
``testing_local``. Se descarto: rompe el flujo de desarrollo
local.

Decision tomada: invocar siempre con
``DJANGO_SETTINGS_MODULE=config.settings.testing_local``
explicito durante esta iniciativa. Para sesiones donde el
desarrollador quiera DEBUG, el default no cambia.

D4 — Smoke test = solo subset ``unit``
----------------------------------------

La suite completa son 1397 tests. Ejecutar todo en este
contexto agrega 5-20 minutos sin garantia de que el subset
``integration`` o ``api`` no requiera fixtures externos
(p.ej. seed historico, datos especificos en
``ivr_legacy``).

Decision tomada: el criterio de completitud incluye solo
``-m unit`` (223 tests). Suficiente para validar que la
infraestructura runtime esta operativa. La ejecucion de la
suite completa con su deuda de fixtures se difiere a
iniciativas dedicadas (al menos una por marker:
``integration``, ``api``).

Hallazgos durante la ejecucion
================================

H-E1 — testing.txt incompleto vs development.py
-------------------------------------------------

``requirements/testing.txt`` declara
``-r base.txt`` + pytest stack + factory-boy + faker +
coverage. No declara ``django-extensions``. Pero
``settings/development.py`` (que ``manage.py`` carga por
default) tiene ``INSTALLED_APPS += ['django_extensions']``.

Resultado: con solo ``testing.txt`` y ``manage.py check``
falla con ``ModuleNotFoundError: django_extensions``. La
contradicion sugiere que ``testing.txt`` se diseno para
trabajar con ``settings.testing`` (no ``development``), pero
``manage.py`` no defaultea a esa settings.

Hallazgo registrado pero no corregido en esta iniciativa:
afecta a la arquitectura de requirements/settings de IACT-api,
fuera de scope (solucion habitual: dependencia opcional o
limpieza del default de manage.py).

H-E2 — config/settings/development.py no es buen default para manage.py
-------------------------------------------------------------------------

``manage.py`` declara
``os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'config.settings.development')``. Para un setup de tests
puros este default crea fricciones (H-E1, requiere DEBUG=False
override en ``.env``, etc).

Considerado durante la ejecucion: cambiar el default a
``testing_local``. No se ejecuto: cambio de codigo
versionado fuera del scope de esta iniciativa runtime. Se
documenta como observacion: una iniciativa futura de
saneamiento de settings podria evaluarlo.

H-E3 — handler 'file' requiere logs/ existente
-------------------------------------------------

``settings/base.py`` declara
``RotatingFileHandler`` apuntando a ``PROJECT_ROOT / 'logs'
/ 'django.log'``. Si ``logs/`` no existe, ``manage.py
check`` ya falla con ``ValueError: Unable to configure
handler 'file'``. No es un "warning" — es un error duro.

Mitigacion aplicada: ``mkdir -p logs/`` antes de
cualquier comando Django. Hallazgo registrado: el handler
podria usar ``mode='a'`` con ``delay=True`` o el codigo
podria crear el directorio al iniciar para evitar el error
duro. Fuera de scope.

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 38 12 50

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - Paquetes apt instalados
     - PASA
     - ``apt-get install`` salida: "Setting up
       libpq-dev", "libmysqlclient-dev",
       "default-libmysqlclient-dev".
   * - Venv con development.txt
     - PASA
     - ``pip list`` muestra Django 5.0.1,
       pytest 7.4.4, mysqlclient 2.2.1,
       psycopg2-binary 2.9.9,
       django-extensions 3.2.3.
   * - .env presente en ambas rutas
     - PASA
     - ``ls -la /home/user/IACT-api/.env`` +
       ``ls -la /home/user/IACT-api/callcentersite/.env``
       (ambos existen).
   * - logs/ creado
     - PASA
     - ``mkdir -p logs/`` aplicado.
   * - manage.py check sin issues
     - PASA
     - "System check identified no issues
       (0 silenced)".
   * - Migraciones aplicadas
     - PASA
     - "Applying ... OK" para todas las apps
       (auth, contenttypes, alerts, audit,
       reports, sessions, users, etc.).
   * - Tests colectados
     - PASA
     - "1397 tests collected in 2.08s".
   * - Tests unit pasan sin fallas
     - PASA
     - "223 passed, 1174 deselected in 35.68s".

Deuda nueva registrada
========================

* **H-E1 / H-E2:** revisar la coherencia entre
  ``requirements/testing.txt`` y
  ``settings/development.py`` (django-extensions). Tambien
  reconsiderar el default de ``manage.py``. Candidato a
  iniciativa de saneamiento.
* **H-E3:** ``logs/`` debe crearse antes del primer
  comando Django. Candidato a fix en ``apps.py`` o
  ``manage.py`` para crearlo automaticamente.
* **Suite completa:** 1174 tests no ejecutados aun
  (markers ``integration``, ``api``, otros). Cada marker
  debe probarse con su fixture set. Iniciativas futuras:
  ``habilitar-pytest-iact-api-integration``,
  ``habilitar-pytest-iact-api-api``.
* **Coverage:** no se midio. Pendiente de iniciativa
  dedicada.
* **manage.py default = development:** invita a
  divergencias. Candidato a fix.
* **IACT-ui pytest/jest:** eslabon ``ui`` de la cadena
  ``db -> api -> ui`` queda como siguiente iniciativa
  natural.

Conclusion
==========

El eslabon ``api`` de la cadena esta operativo. IACT-api
arranca con ambas bases conectadas (PostgreSQL
``iact_analytics`` para Django default, MariaDB
``ivr_legacy`` para el ORM ``ivr``). pytest colecta los 1397
tests y el subset ``unit`` (223 tests) pasa al 100% sin
modificaciones de codigo. La infraestructura de pruebas
funciona: cambios futuros en api/ui pueden validarse contra
esta base.
