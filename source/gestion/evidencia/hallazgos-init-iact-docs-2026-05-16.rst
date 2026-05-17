.. meta::
   :artefacto: HALLAZGOS-INIT-IACT-DOCS-2026-05-16
   :tipo: Evidencia
   :dominio: gestion/evidencia
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-16
   :ultimo_cambio: 2026-05-16
   :autor: NestorMonroy
   :clasificacion: Interno

.. _hallazgos-init-iact-docs-2026-05-16:

==========================================================
Hallazgos: Inicializacion git IACT-docs — 2026-05-16
==========================================================

Documento de hallazgos generado al inicializar el repositorio
git de IACT-docs e identificar deuda tecnica activa en el
build de Sphinx.

----

Contexto
========

Al completar las 5 fases de IACT-api, se realizo una auditoria
del estado de los repositorios del proyecto. IACT-docs no tenia
``.git`` y sus archivos ``pyproject.toml`` y ``uv.lock``
contenian **conflictos de merge sin resolver** de la rama
``dependabot/pip/sphinx-autodoc-typehints-3.6.1``.

Los conflictos hacian ``pyproject.toml`` TOML invalido,
bloqueando ``uv sync`` y el build de Sphinx.

----

Resumen de commits
==================

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Commit
     - Descripcion
   * - ``22971a4``
     - fix(deps): resolver conflictos de merge dependabot
   * - ``f11b301``
     - feat(docs): base documental completa — 1485 archivos RST

----

Hallazgo H-DOCS-001 — Conflictos de merge sin resolver
=======================================================

**Severidad:** Bloqueante (build imposible)

**Archivos afectados:**

- ``pyproject.toml``: 3 bloques de conflicto
- ``uv.lock``: 7 bloques de conflicto

**Descripcion:**

La rama ``dependabot/pip/sphinx-autodoc-typehints-3.6.1``
propuso actualizar dependencias pero no fue mergeada ni
abortada. Los marcadores de conflicto quedaron incrustados
en ambos archivos, haciendo ``pyproject.toml`` invalido como
TOML.

**Conflictos en pyproject.toml:**

.. list-table::
   :widths: 10 40 40
   :header-rows: 1

   * - Bloque
     - dependabot propuso
     - develop mantiene
   * - 1
     - ``Sphinx>=9,<10``
     - ``Sphinx>=8.2.3,<9.0`` (pinned por autodocsumm)
   * - 2
     - ``myst-parser==5.0.0`` (Markdown)
     - Sin myst-parser (RST-only, F-NEW-5)
   * - 3
     - ``markdown-it-py``, ``mdit-py-plugins``, ``mdurl``
     - Eliminados (deps transitivas de myst-parser)

**Decision:** develop gana en todos los conflictos.

**Correccion aplicada:**

Resolucion manual de los 3 bloques en ``pyproject.toml``.
El ``uv.lock`` fue regenerado completamente con ``uv lock``
en lugar de resolver los 7 bloques manualmente (ver
H-DOCS-002).

----

Hallazgo H-DOCS-002 — uv.lock no puede resolverse manualmente
==============================================================

**Severidad:** Tecnica (metodologia)

**Descripcion:**

Intentar resolver los 7 bloques de conflicto en ``uv.lock``
manualmente y ejecutar ``uv sync`` produjo el error::

   Failed to parse uv.lock
   Dependency `sphinx` has missing `source` field but has
   more than one matching package

El lockfile contenia entradas duplicadas de Sphinx de ambas
ramas. La estrategia correcta es eliminar el lockfile
conflictuado y regenerarlo con ``uv lock`` tras resolver
``pyproject.toml``. El lockfile es un artefacto generado;
no contiene decisiones de arquitectura.

**Correccion aplicada:**

``rm uv.lock && uv lock``

Resultado: 94 paquetes resueltos, lockfile valido.

----

Hallazgo H-DOCS-003 — Incompatibilidad sphinx-autodoc-typehints
================================================================

**Severidad:** Bloqueante (``uv lock`` fallaba)

**Descripcion:**

El ``pyproject.toml`` ya contenia una inconsistencia preexistente
al conflicto de Dependabot. El comentario en el propio archivo
lo documentaba::

   "sphinx-autodoc-typehints==3.6.0",
   # Type hints support (Sphinx>=9.0.4, Python>=3.11)

La version 3.6.0 requiere ``Sphinx>=9.0.4``, pero el proyecto
pineaba ``Sphinx>=8.2.3,<9.0``. Esta combinacion hace
``uv lock`` insatisfiable.

**Version afectada:** ``sphinx-autodoc-typehints==3.6.0``

**Correccion aplicada:**

Bajada a ``sphinx-autodoc-typehints==2.5.0`` — ultima version
de la serie 2.x, compatible con Sphinx 8.x.

**Nota:** Esta inconsistencia habria bloqueado ``uv lock``
incluso sin los conflictos de Dependabot.

----

Hallazgo H-DOCS-004 — Warnings RST Title underline too short
=============================================================

**Severidad:** Warning de Sphinx (degradacion del build)

**Descripcion:**

Al hacer el primer build completo con cache frio (``-E``),
aparecieron 14 warnings ``Title underline too short`` en
8 archivos del subdominio ``access``. El build parcial
anterior usaba cache y los omitia.

**Archivos corregidos:**

.. list-table::
   :widths: 60 20 20
   :header-rows: 1

   * - Archivo
     - Linea
     - Subrayado (chars)
   * - access/uc-acc-01/actores-precondiciones.rst
     - 91
     - 37 -> 48
   * - access/uc-acc-01/testing.rst
     - 36
     - 37 -> 48
   * - access/uc-acc-01/testing.rst
     - 49
     - 47 -> 58
   * - access/uc-acc-03/datos-involucrados.rst
     - 117
     - 47 -> 54
   * - access/uc-acc-03/testing.rst
     - 81
     - 38 -> 49
   * - access/uc-acc-05/datos-involucrados.rst
     - 130
     - 13 -> 20
   * - access/uc-acc-05/datos-involucrados.rst
     - 197
     - 32 -> 39
   * - access/uc-acc-05/diagramas-uml.rst
     - 156
     - 33 -> 40

**Causa raiz:** El titulo contiene caracteres Unicode (``—``,
parentesis, espacios) que en Python tienen ``len()`` == 1
pero el subrayado fue calculado manualmente con conteo incorrecto.

**Correccion aplicada:**

Subrayado extendido al ``len(titulo)`` exacto usando
``char * len(titulo)`` en Python para cada caso.

----

Hallazgo H-DOCS-005 — Warnings RST Unexpected indentation
==========================================================

**Severidad:** Warning de Sphinx (degradacion del build)

**Descripcion:**

2 warnings ``ERROR: Unexpected indentation`` en archivos
del subdominio ``operator``.

**Archivos afectados:**

- ``operator/uc-opr-03/patrones-diseno.rst:11``
- ``operator/uc-opr-07/patrones-diseno.rst:11``

**Causa raiz:**

Una lista con bullet ``-`` iniciaba inmediatamente despues
de un parrafo sin linea en blanco separadora. RST interpreta
la lista como parte del parrafo anterior, y la continuacion
indentada del bullet como indentacion inesperada.

Patron incorrecto::

   P-84 (nuevo): Allowlist-bound dialing
   - destination NO sale de allowlist
     (politica anti-fraude + compliance).

Patron correcto::

   P-84 (nuevo): Allowlist-bound dialing

   - destination NO sale de allowlist
     (politica anti-fraude + compliance).

**Correccion aplicada:**

Linea en blanco anadida entre el parrafo y la lista en
ambos archivos.

----

Estado final del build
======================

.. code-block:: text

   uv run sphinx-build -b dummy source /tmp/iact-docs-final
   build succeeded.
   0 warnings, 0 errors

**Deuda tecnica residual: CERO.**

----

Commits del repositorio
=======================

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Commit
     - Rama
     - Descripcion
   * - ``22971a4``
     - develop
     - fix(deps): conflictos Dependabot + sphinx-autodoc-typehints
   * - ``f11b301``
     - develop
     - feat(docs): base documental 1485 RST + 10 correcciones RST

*Generado: 2026-05-16T22:10:18 | Sphinx 8.2.3 | uv 94 packages*
