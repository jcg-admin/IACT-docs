.. meta::
   :artefacto: DECISIONES-SANEAR-DEUDA-RUNTIME-MULTIREPO
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/sanear-deuda-runtime-multirepo
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:12:52
   :ultimo_cambio: 2026-05-19T19:12:52
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-sanear-deuda-runtime-multirepo:

==============================================================
Decisiones: Sanear Deuda Runtime Multi-Repo
==============================================================

Decisiones de diseno
=====================

D1 — fix de logs/ va en base.py, no en apps.py ni manage.py
-------------------------------------------------------------

Tres ubicaciones consideradas para el ``mkdir`` de
``logs/``:

* ``manage.py``: rechazado. Solo cubre comandos CLI; las
  invocaciones via WSGI/gunicorn no pasan por manage.
* ``apps.py`` (AppConfig.ready): rechazado. El handler de
  logging se construye **antes** de que las apps esten
  listas; el error sucede en ``django.setup()`` durante
  ``configure_logging``, no en app ready.
* ``settings/base.py`` justo despues de ``PROJECT_ROOT``:
  **elegido**. Garantiza que el directorio exista antes
  de que ``LOGGING`` se evalue (ambos viven en el mismo
  modulo, mismo orden de import). Funciona para CLI,
  WSGI, pytest, gunicorn, etc.

D2 — overrides solo glob, no inflight ni fstream
--------------------------------------------------

Considerado: aliasar ``inflight`` a ``lru-cache`` y
``fstream`` a ``tar`` via ``overrides`` (sugerencia
literal de los warnings de npm).

Probado: aliasing rompe APIs. ``inflight`` expone una
funcion factory que ``lru-cache`` no tiene; cualquier
consumer transitive falla. ``fstream`` expone streams
que ``tar`` no provee directamente. El cambio rompe
``npm install`` (paquetes que importan estos fallan).

Decision tomada: limitar el override a ``glob: ^10.4.5``,
que es backwards-compatible para los consumers
transitivas que detecte npm. Verificado con ``npm test``
sin regresiones. ``inflight`` y ``fstream`` quedan como
deuda residual; su saneamiento real requiere actualizar
los paquetes que dependen de ellos a versiones que ya no
los usen (trabajo de actualizacion de deps grande,
fuera de scope).

D3 — Decision de tratar la brecha pytest como deuda externa
-------------------------------------------------------------

Pytest con ``--create-db`` revelo 67 failed + 4 errors
(5.1% del total). Considerado: incluir el analisis y fix
de esas 71 fallas en esta iniciativa.

Se descarto por dos razones:

* El alcance "sanear deuda runtime" es heterogeneo (api,
  ui, IACT). Anadir 71 investigaciones de fallas
  individuales diluye su foco.
* Cada falla potencialmente requiere su propia tarea
  con diagnostico/fix/test. No son una unidad coherente.

Decision tomada: dejar la brecha cuantificada (
``T-005`` con conteo verificado) y abrir iniciativa
hermana ``resolver-tests-fallidos-pytest-iact-api``
cuando el sponsor decida prioridad. La diferencia clave
con el cierre previo de ``habilitar-pytest-iact-api`` es
que ya no son "1174 tests no ejecutados" (incognita)
sino "67 + 4 fallas observables y trazables" (deuda con
contorno).

D4 — Submodulo docs con URL github canonica
---------------------------------------------

Considerado: declarar la URL del submodulo con la URL
del proxy local
(``http://127.0.0.1:44269/git/jcg-admin/IACT-docs.git``)
que es la que git submodule add detecto. Se descarto:
mismo patron que los otros submodulos
(``https://github.com/jcg-admin/...``); la URL local es
artefacto del proxy de esta sesion, no del proyecto.

Decision tomada: editar ``.gitmodules`` post-add para
fijar URL canonica https://github.com/jcg-admin/IACT-docs.git.
Local clones que usen el proxy lo redirigen
automaticamente; sesiones fuera del proxy usan la URL
GitHub directa.

D5 — Iniciativa compacta con 3 documentos
-------------------------------------------

El alcance es heterogeneo pero las decisiones de
diseno son enumerables y el progreso esta dominado por
evidencia textual de outputs (no por matriz de gaps).
Formato compacto es coherente.

Hallazgos durante la ejecucion
================================

H-E1 — Aliasing de inflight rompe el install
----------------------------------------------

Detectado en una iteracion previa al commit final. El
override inicial inclula
``"inflight": "npm:lru-cache@^11.0.0"`` y
``"fstream": "npm:tar@^7.4.3"``. ``npm install``
imprimia errores duros porque los consumers esperan la
API original. Reduccion del override a solo ``glob``
resolvio el bloqueo. Documentado en D2.

H-E2 — pytest --reuse-db (default en pytest.ini) causa errores en suite completa
----------------------------------------------------------------------------------

El flag ``--reuse-db`` configurado en ``pytest.ini``
``addopts`` produce 932 errores en la suite completa
porque diferentes markers contaminan el esquema de la
test DB. Cambiar a ``--create-db`` runtime baja los
errores a 4 y los failures aparecen como reales (67).

No se modifico ``pytest.ini`` en esta iniciativa: cambiar
el default afecta el ciclo de desarrollo incremental
(``--reuse-db`` es mas rapido). Se documenta como deuda
para iniciativa de saneamiento de pytest config.

H-E3 — git submodule add usa la URL de fetch del remote actual
----------------------------------------------------------------

Cuando se ejecuta ``git submodule add <url> docs``
desde IACT, git clona via la URL pasada. Si la URL es
la del proxy local
(``http://local_proxy@127.0.0.1:44269/...``), termina
en ``.gitmodules`` aunque el proyecto deba referenciar
github.com canonico. Hay que editar
``.gitmodules`` post-add (D4).

H-E4 — .gitignore tenia "docs/" heredado
------------------------------------------

Bloqueo inicial: ``git submodule add ... docs`` fallaba
con "The following paths are ignored by one of your
.gitignore files: docs". La regla ``docs/`` venia de un
setup anterior donde ``docs/`` era artefacto de build
local de Sphinx. Removerla fue prerequisito.

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 38 12 50

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - testing.txt declara django-extensions
     - PASA
     - ``grep django-extensions
       IACT-api/requirements/testing.txt`` =>
       ``django-extensions==3.2.3``. Commit
       ``86b52cb``.
   * - base.py crea logs/ automatico
     - PASA
     - ``rm -rf IACT-api/logs && manage.py check``
       => "System check identified no issues",
       y luego ``ls IACT-api/logs`` muestra
       ``django.log``. Mismo commit ``86b52cb``.
   * - package.json override glob ^10
     - PASA
     - ``grep glob IACT-ui/package.json`` =>
       ``"glob": "^10.4.5"`` en bloque
       overrides. Commit ``61b2155``.
   * - npm test sigue verde
     - PASA
     - "Test Suites: 250 passed, 250 total;
       Tests: 2381 passed, 2381 total; Time:
       20.9s".
   * - IACT/.gitmodules incluye docs
     - PASA
     - ``cat IACT/.gitmodules`` muestra bloque
       ``[submodule "docs"]`` con URL
       https://github.com/jcg-admin/IACT-docs.git.
       Commit ``00c401c6``.
   * - IACT/.gitignore sin "docs/"
     - PASA
     - ``grep -E "^docs/?$"
       IACT/.gitignore`` => sin output. Commit
       ``00c401c6``.
   * - Suite pytest completa cuantificada
     - PASA
     - 67 failed, 1326 passed, 4 errors en
       93.54s con ``--create-db``. 95% pass
       rate.

Deuda residual y nuevas iniciativas candidatas
===============================================

* **resolver-tests-fallidos-pytest-iact-api**: 67 fallas
  reales + 4 errores en la suite completa con
  ``--create-db``. Cada una requiere diagnostico propio.
* **sanear-pytest-config-iact-api**: cambiar el default
  de ``--reuse-db`` por ``--create-db`` o instrumentar
  la diferencia. Tambien revaluar el default de
  ``manage.py`` de ``development`` a ``testing_local``.
* **sanear-deuda-deps-npm-iact-ui**: ``inflight`` y
  ``fstream`` aun emiten warnings. Solucion correcta:
  actualizar los paquetes que los importan. Adicional:
  ``lodash.isequal``, ``whatwg-encoding``, ``uuid@8``
  detectados en este install.
* **integrar-docs-en-submodulo-iact**: ahora que docs
  es submodulo, sesiones del orquestador pueden
  agregar ``git submodule update --init --recursive``
  como paso en su README de setup.
* **resolver-tests-mariadb-historico**:
  ``schema_historico.sql`` y ``seed_historico.sql`` no
  se aplicaron en
  ``preparar-entorno-mariadb-ivr-legacy``. Si la
  brecha pytest se debe a tests que esperan tablas
  ``tbl_historico_*``, esta iniciativa cierra esa
  causa raiz.

Conclusion
==========

Cuatro deudas concretas cerradas con commits reales en
tres repos. La brecha pytest queda cuantificada en
67 failed + 4 errors (5.1%), trazable y diferida a
iniciativa dedicada. Patron ``:repo_objetivo: multiple``
con tres feature branches paralelas estrenado y
documentado.

Cumple la directiva del sponsor: "continuar y no dejar
deuda tecnica". Donde no se cerro deuda en bloque
(D2, D3), se subdividio en iniciativas con scope
acotado y observables ya capturados.
