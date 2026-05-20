.. meta::
   :artefacto: ALCANCE-SANEAR-DEUDA-RUNTIME-MULTIREPO
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/sanear-deuda-runtime-multirepo
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:07:37
   :ultimo_cambio: 2026-05-19T19:12:52
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-sanear-deuda-runtime-multirepo:

==============================================================
Alcance: Sanear Deuda Runtime Multi-Repo
==============================================================

Por que existe
==============

Las iniciativas hermanas (``habilitar-pytest-iact-api``,
``habilitar-jest-iact-ui``, ``preparar-entorno-mariadb-ivr-legacy``,
``evolucionar-proc-gob-013-multirepo``) cerraron con la cadena
``db -> api -> ui`` operativa pero dejaron registrada en sus
documentos de decisiones varias deudas concretas:

* **H-E1 api** — ``requirements/testing.txt`` no declara
  ``django-extensions``, requerido por
  ``settings/development.py``. Cualquier setup fresco que
  use solo testing.txt falla en el primer ``manage.py``.
* **H-E3 api** — ``logs/`` debe pre-existir o
  ``manage.py check`` falla con ``ValueError("Unable to
  configure handler 'file'")``. Es un error duro sin
  workaround documentado.
* **DEBT-FUTURE-NPM-DEPS ui** — 3 warnings de deprecacion
  en transitivas (``inflight``, ``glob@7``, ``fstream``)
  al ``npm install``.
* **H-E1 mariadb cierre** — ``.gitmodules`` de IACT
  declaraba solo api/db/ui; faltaba docs/. Sin ese
  submodulo, un clone fresco de IACT no tiene acceso al
  corpus documental que define el sistema.

Adicionalmente, los 1174 tests no ejecutados por
``habilitar-pytest-iact-api`` (filtro ``-m unit`` solo
223 / 1397) son deuda implicita: se desconoce su estado.

Criterio de completitud verificable
=====================================

* ``requirements/testing.txt`` declara
  ``django-extensions==3.2.3``.
* ``settings/base.py`` ejecuta
  ``(PROJECT_ROOT / 'logs').mkdir(exist_ok=True)``
  inmediatamente despues de definir ``PROJECT_ROOT``.
* ``IACT-api/logs/`` se crea automaticamente tras
  ``rm -rf logs/`` + ``manage.py check``; el check no
  falla.
* ``IACT-ui/package.json`` declara
  ``overrides.glob: "^10.4.5"``. ``npm test`` sigue en
  250 suites / 2381 tests passed.
* ``IACT/.gitmodules`` incluye bloque
  ``[submodule "docs"]`` con URL
  ``https://github.com/jcg-admin/IACT-docs.git`` y la
  entrada ``docs`` esta indexada como submodulo
  (gitlink mode 160000).
* ``IACT/.gitignore`` ya no contiene la regla ``docs/``.
* Suite pytest completa ejecutada con ``--create-db``
  reporta una tabla resumen pass/fail/error con conteo
  real.

In-scope
========

* Modificaciones de codigo en ``IACT-api/requirements/testing.txt``
  y ``IACT-api/callcentersite/config/settings/base.py``.
* Modificacion de ``IACT-ui/package.json`` con bloque
  ``overrides`` y regeneracion controlada de
  ``package-lock.json``.
* Modificacion de ``IACT/.gitignore`` y ``IACT/.gitmodules``
  + adicion del submodulo ``docs``.
* Re-ejecucion runtime de la suite pytest completa con
  ``--create-db`` para medir la brecha real.
* Documentacion compacta de la iniciativa en IACT-docs
  (3 archivos: index, alcance, tareas-y-progreso,
  decisiones).

Out-of-scope
============

* Cualquier trabajo sobre ``uc-opr-*``, ``uc-sup-*`` y
  ``uc-cli-01..05``.
* Atacar las 67 fallas / 4 errores reales detectados con
  ``--create-db``: requieren analisis caso por caso,
  fuera del alcance "sanear lo trazable". Se difieren a
  iniciativa dedicada
  ``resolver-tests-fallidos-pytest-iact-api``.
* Reemplazar ``inflight`` y ``fstream`` con alternativas
  modernas: los reemplazos rompen APIs y requieren
  iniciativa dedicada de saneamiento de deps npm.
* Cambiar el default de ``manage.py`` de
  ``development`` a ``testing_local``: rompe el flujo
  estandar de desarrollo. Se difiere a iniciativa de
  refactor de settings.
* Coverage report y gates de cobertura: deuda
  diferida desde ``habilitar-pytest-iact-api``.
