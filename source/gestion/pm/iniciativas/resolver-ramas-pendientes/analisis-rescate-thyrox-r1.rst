.. meta::
   :artefacto: ANALISIS-RESCATE-THYROX-R1
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-ramas-pendientes
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:46:00
   :ultimo_cambio: 2026-05-18T18:46:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _analisis-rescate-thyrox-r1:

============================================================
Analisis: Rescate de .thyrox/ de la rama R1
============================================================

Contexto
========

La rama R1 (``claude/review-project-config-V8Fg5``) reporta 9
archivos ``.thyrox/`` "unicos" segun ``git diff --name-only
origin/develop...R1``. Se evaluo si rescatarlos antes de
resolver la rama.

Correccion de caracterizacion previa
=====================================

El documento ``analisis-estado-ramas-pendientes`` describio
``.thyrox/`` como "scratch de trabajo, no contenido del
producto". **Esa caracterizacion es incorrecta** y se corrige
aqui con evidencia:

* ``.thyrox/`` esta versionado en ``origin/develop``: 3548
  archivos.
* ``.thyrox/`` no figura en ``.gitignore`` de develop.
* El proyecto trackea ``.thyrox/`` deliberadamente; contiene
  ADRs, registros de work packages y analisis de proceso con
  valor (no es scratch desechable).

Verificacion por hash (evidencia)
==================================

El conteo de ``git diff`` bidireccional infla el resultado: R1
esta ``behind`` 1420 respecto a develop, por lo que reporta como
"unicos" archivos que develop ya tiene en otra version. Se
comparo el hash de objeto git (SHA-1 de contenido) de cada
archivo entre R1 y develop:

.. list-table::
   :header-rows: 1
   :widths: 16 18 18 48

   * - Estado
     - Hash R1
     - Hash develop
     - Archivo
   * - IDENTICO
     - ``628f68165565``
     - ``628f68165565``
     - ``adr-decouple-myst-parser.md``
   * - IDENTICO
     - ``6aaeb4bc4d2e``
     - ``6aaeb4bc4d2e``
     - ``adr-hierarchical-toctree-structure.md``
   * - IDENTICO
     - ``0a9241d65e2e``
     - ``0a9241d65e2e``
     - ``adr-semantic-cross-references.md``
   * - DIFIERE
     - ``9cc4bf53b332``
     - ``5b6decf23d6c``
     - ``now.md`` (develop mas reciente)
   * - NUEVO en R1
     - ``685ef34fe21b``
     - (ausente)
     - ``architecture-constraints.md``
   * - IDENTICO
     - ``f04e8ab5aadc``
     - ``f04e8ab5aadc``
     - ``DOCUMENTATION-INDEX.md``
   * - IDENTICO
     - ``b6add88d50de``
     - ``b6add88d50de``
     - ``config-review-iact-docs-changelog.md``
   * - IDENTICO
     - ``192ed20d6fa6``
     - ``192ed20d6fa6``
     - ``config-review-iact-docs-lessons-learned.md``
   * - IDENTICO
     - ``9459a4b45959``
     - ``9459a4b45959``
     - ``warning-root-cause-analysis.md``

Interpretacion: hash de objeto git identico implica contenido
binariamente identico, sin ambiguedad. 7 de 9 ya estan en
develop sin diferencia alguna.

Conclusiones
============

* **7 archivos IDENTICOS**: ya estan en develop byte por byte.
  No se rescatan (copiarlos seria duplicar lo identico = deuda).
* **1 archivo (``now.md``)**: develop tiene version mas
  reciente. Ademas es un archivo incremental de estado; moverlo
  o retrocederlo no tiene sentido. Se ignora (decision del
  usuario).
* **1 archivo (``architecture-constraints.md``)**: unico real,
  ausente en develop, 261 lineas, ``status: Borrador``. Documenta
  el analisis de las 711 warnings de Sphinx y el desacople
  arquitectonico toctree vs implementacion (mismo problema raiz
  que el diferido D-01). Es contenido con valor, no scratch.

Recomendacion
=============

R1 NO aporta los 9 archivos que el ``git diff`` sugiere: aporta
efectivamente **uno** (``architecture-constraints.md``). El resto
ya esta en develop o se ignora por incremental.

Decision pendiente del usuario: rescatar
``architecture-constraints.md`` (unico contenido con valor que se
perderia al borrar R1) a un repositorio de paso, o dejarlo fuera
de alcance. No se copio ningun archivo a ``wp-tmp/`` en este
analisis: 8 de 9 no proceden, y el noveno espera decision
explicita.

Implicacion para R1: una vez resuelto el destino de
``architecture-constraints.md``, el resto del valor ``.thyrox/``
de R1 ya esta en develop. El ``source/`` de R1 sigue descartado
(nomenclatura antigua, ver ``analisis-estado-ramas-pendientes``).
R1 queda como candidata a borrado tras esa unica decision.

Leccion de proceso
===================

Tercer caso en la sesion del mismo patron: ``git diff
--name-only A...B`` sobre una rama ``behind`` infla el conteo de
"unicos". La verificacion correcta es comparar hash de objeto
git por archivo, no asumir por el listado de ``git diff``.
