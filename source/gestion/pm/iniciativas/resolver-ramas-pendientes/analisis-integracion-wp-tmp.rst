.. meta::
   :artefacto: ANALISIS-INTEGRACION-WP-TMP
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-ramas-pendientes
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T21:37:24
   :ultimo_cambio: 2026-05-18T21:37:24
   :autor: NestorMonroy
   :clasificacion: Interno

.. _analisis-integracion-wp-tmp:

============================================================
Analisis: Integracion del contenido de wp-tmp/ a source/
============================================================

Proposito
=========

``wp-tmp/`` preservo 94 archivos rescatados de R1, R2 y R3. Este
documento analiza **como** integrarlos a su ubicacion final en
``source/`` sin reintroducir deuda (nomenclatura obsoleta,
toctrees rotos, contenido inferior). NO ejecuta la integracion:
la clasifica y define la estrategia por grupo.

Inventario
==========

.. list-table::
   :header-rows: 1
   :widths: 10 14 76

   * - Origen
     - Archivos
     - Naturaleza
   * - R1
     - 1
     - ``architecture-constraints.md`` (analisis de las 711
       warnings; Markdown, ingles, borrador abril).
   * - R2
     - 12
     - Spec UC-SUP-01: 11 contenidos + ``diagramas-uml.rst``.
   * - R3
     - 80
     - 8 nuevos + 68 que difieren + 3 no-source +
       PROCEDENCIA.

Grupo R2 — integracion de bajo riesgo (recomendado primero)
============================================================

Destino: ``source/requisitos/casos-uso/supervision/uc-sup-01/``.
Comparacion verificada develop vs wp-tmp:

.. list-table::
   :header-rows: 1
   :widths: 40 18 18 24

   * - Archivo
     - develop
     - wp-tmp
     - Accion
   * - ``actores-precondiciones.rst``
     - 18
     - 90
     - Reemplazar (stub -> completo)
   * - ``criterios-aceptacion.rst``
     - 14
     - 211
     - Reemplazar
   * - ``datos-involucrados.rst``
     - 10
     - 214
     - Reemplazar
   * - ``diagramas-uml.rst``
     - (ausente)
     - 154
     - Anadir (nuevo)
   * - ``excepciones.rst``
     - 12
     - 285
     - Reemplazar
   * - ``flujo-principal.rst``
     - 18
     - 193
     - Reemplazar
   * - ``flujos-alternos.rst``
     - 14
     - 208
     - Reemplazar
   * - ``implementacion-tecnica.rst``
     - 9
     - 222
     - Reemplazar
   * - ``informacion-general.rst``
     - 19
     - 132
     - Reemplazar
   * - ``patrones-diseno.rst``
     - 12
     - 125
     - Reemplazar
   * - ``requisitos-no-funcionales.rst``
     - 11
     - 146
     - Reemplazar
   * - ``testing.rst``
     - 14
     - 358
     - Reemplazar

Riesgo R2: BAJO. develop tiene stubs; wp-tmp tiene la spec
completa. La ruta de destino existe y es la misma (nomenclatura
``uc-sup-01/`` ya correcta). Verificacion previa a integrar:
(a) que los toctrees de ``uc-sup-01/index`` en develop
referencien estos 12 archivos; (b) que ``diagramas-uml.rst``
(nuevo) este enlazado o se enlace en el index correspondiente,
para no crear documento huerfano (warning).

Grupo R3 — integracion de riesgo MEDIO-ALTO
============================================

* **8 nuevos** (ausentes en develop), incluido
  ``modelo-rbac-iact.rst`` (2897 lineas, ``:version: 5.4.0``
  M2M verificado vigente), ``cnst-030-sod.rst``, 6
  ``diagramas-uml.rst`` de casos de uso. Riesgo de
  integracion: cada nuevo necesita estar enlazado en el
  toctree de su seccion o genera warning de huerfano.
* **68 que difieren**: R3 mas reciente por fecha, pero NO
  verificado contenido sustantivo vs trivial archivo por
  archivo. Integrarlos en bloque es el mayor riesgo: 68
  archivos que sobrescriben develop sin saber si la diferencia
  es mejora real o ruido. Requiere el mismo metodo que el
  Grupo B de R2 (diff de magnitud por archivo) antes de
  decidir cuales reemplazan.
* **3 no-source** (``.gitignore``, ``pyproject.toml``,
  ``uv.lock``): NO integrar. develop ya los tiene correctos
  y mas recientes (PR #23). Marcados en PROCEDENCIA.

Grupo R1 — requiere transformacion, no copia
=============================================

``architecture-constraints.md``: valioso como evidencia
historica, pero es Markdown + ingles + borrador con datos
obsoletos (711 warnings, estado pre-D-01). Integrarlo tal cual
a ``source/`` contradice la politica RST-only del proyecto y
presentaria datos superados como vigentes. Opciones: (a)
conservar solo en ``wp-tmp/`` como evidencia (no integrar a
source/); (b) reescribir como RST historico en espanol. No es
copia directa; decision pendiente del usuario.

Estrategia de integracion recomendada (orden por riesgo)
=========================================================

1. **R2 primero** (riesgo bajo): los 12 archivos, con
   verificacion de toctree de ``uc-sup-01/index`` antes de
   reemplazar. Cada reemplazo verificado por build 0 warnings.
2. **R3 nuevos** (riesgo medio): los 8, cada uno enlazado en
   su toctree correspondiente para no crear huerfanos.
   Verificar ``modelo-rbac-iact.rst`` no colisione con
   contenido RBAC vigente de develop.
3. **R3 que difieren** (riesgo alto): analisis de sustancia
   por archivo (diff de magnitud) ANTES de decidir cuales
   integrar. No en bloque.
4. **R1**: decision del usuario (conservar como evidencia vs
   reescribir RST).

Cada paso es una tarea T-NNN futura con su verificacion de
build. Este analisis NO ejecuta integracion; la habilita de
forma trazable y sin deuda.

Restriccion critica
===================

Toda integracion a ``source/`` debe pasar build
``sphinx-build -W -j 2`` con 0 warnings antes de commitear
(PROC-GOB-013 Fase 3 paso 5). Anadir un archivo sin enlazarlo
en un toctree genera warning de documento huerfano: ese es el
modo de fallo mas probable y el que el analisis previene al
exigir verificacion de toctree por cada archivo.
