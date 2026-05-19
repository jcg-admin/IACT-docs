.. meta::
   :artefacto: PROC-GOB-014
   :tipo: Procedimiento
   :dominio: normativa
   :subdominio: procedimientos
   :estado: Aprobado
   :version: 1.0.0
   :fecha_creacion: 2026-05-19
   :ultimo_cambio: 2026-05-19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _proc-gob-014-gestion-por-submodulo:

================================================================
Procedimiento: Gestion por submodulo en ``source/gestion/pm/``
================================================================

.. note::

   Procedimiento obligatorio que describe **como se estructura y
   gestiona el trabajo por submodulo** del sistema IACT bajo
   ``source/gestion/pm/``.

   Complementa a
   :doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`
   (iniciativas globales) anadiendo el eje de **gestion vertical
   por submodulo** (api, db, docs, server, ui).

   Todo archivo producido en ``source/`` es exclusivamente ``.rst``.
   Los artefactos operativos generados por los skills
   (``.md`` en ``.thyrox/context/work/``) no entran en ``source/``.

----

Principio Rector
================

El sistema IACT esta compuesto por cinco submodulos con ciclos de
vida tecnicos y de release independientes:

- ``api`` — capa de servicios REST (Django + DRF).
- ``db`` — esquema, migraciones, seeds, ETL.
- ``docs`` — corpus documental (este repositorio).
- ``server`` — infraestructura, despliegue, runbooks operativos.
- ``ui`` — frontend (React).

Cada submodulo requiere su propio espacio de gestion: roadmap,
iniciativas, decisiones, riesgos e indicadores. Mezclar la gestion
de los cinco en una sola jerarquia plana esconde dependencias y
diluye la trazabilidad. Por eso ``source/gestion/pm/`` se
organiza como un arbol vertical: una rama por submodulo, con un
mismo conjunto de artefactos estandar dentro de cada rama.

Las iniciativas que cruzan dos o mas submodulos siguen viviendo en
``source/gestion/pm/iniciativas/`` (rama transversal). La gestion
por submodulo no las absorbe; las **referencia** desde el
``index.rst`` del submodulo correspondiente.

----

Estructura obligatoria
======================

A partir de la version 1.0.0 de este procedimiento, el subdominio
``source/gestion/pm/`` cumple esta estructura:

.. code-block:: text

   source/gestion/pm/
   ├── index.rst                       Indice raiz de PM
   ├── api/
   │   └── index.rst                   Indice del submodulo API
   ├── db/
   │   └── index.rst                   Indice del submodulo DB
   ├── docs/
   │   └── index.rst                   Indice del submodulo DOCS
   ├── server/
   │   └── index.rst                   Indice del submodulo SERVER
   ├── ui/
   │   └── index.rst                   Indice del submodulo UI
   ├── iniciativas/                    Iniciativas transversales
   ├── audits/                         Auditorias globales
   ├── checklists/                     Checklists operativos
   ├── lecciones-aprendidas/           Lecciones globales
   └── matrices/                       Matrices de trazabilidad

Cada directorio ``{api,db,docs,server,ui}/`` es un **submodulo de
gestion** y debe contener al menos el ``index.rst`` con las
secciones definidas en el siguiente apartado.

----

Plantilla de ``index.rst`` por submodulo
========================================

Todo ``index.rst`` de submodulo declara las siguientes secciones,
en este orden:

#. **Meta y target** — bloque ``.. meta::`` con
   ``artefacto: INDEX-PM-<MOD>`` y ``subdominio: pm-<mod>``.
#. **Proposito** — que aspecto del submodulo gestiona este indice.
#. **Alcance** — que entra y que no entra. Que iniciativas
   transversales lo afectan.
#. **Roadmap** — vista o link al roadmap del submodulo (puede ser
   embed o link a tablero externo, registrado aqui).
#. **Iniciativas activas** — lista de iniciativas (transversales o
   propias) que tocan este submodulo, con su estado.
#. **Decisiones recientes** — ADRs aprobados que afectan al
   submodulo. Link al ADR canonico en
   ``source/normativa/gobernanza/``.
#. **Riesgos abiertos** — riesgos vivos con severidad y duenio.
#. **Indicadores** — metricas que el submodulo monitorea
   (cobertura, MTTR, SLO, etc.) o ``Pendiente`` si aun no se ha
   definido.
#. **Trazabilidad** — link a este procedimiento (PROC-GOB-014),
   al naming (STD-007) y al procedimiento de iniciativas globales
   (PROC-GOB-013).

----

Naming y convenciones
=====================

- Nombres de directorio: kebab-lowercase corto, sin tildes
  (``api``, ``db``, ``docs``, ``server``, ``ui``). Ver
  :doc:`/normativa/estandares/std-007-convencion-naming`.
- Identificador en ``meta::`` del indice: ``INDEX-PM-<MOD>`` en
  mayusculas (``INDEX-PM-API``, ``INDEX-PM-DB``, etc.).
- Subdominio en ``meta::``: ``pm-<mod>`` en minusculas
  (``pm-api``, ``pm-db``, etc.).

Artefactos hijos del submodulo siguen el naming general:
``adr-<mod>-NNN-desc.rst``, ``risk-<mod>-NNN-desc.rst``,
``initiative-<mod>-NNN-desc.rst``. La numeracion ``NNN`` es por
submodulo (cada submodulo tiene su contador independiente).

----

Reglas de actualizacion
=======================

#. **Toda iniciativa transversal** registrada en
   ``source/gestion/pm/iniciativas/`` que tenga impacto en un
   submodulo debe aparecer linkada desde el ``index.rst`` de
   ese submodulo, en la seccion "Iniciativas activas".
#. **Toda decision** (ADR) que afecte exclusivamente a un
   submodulo se referencia desde la seccion "Decisiones
   recientes" del submodulo. ADRs transversales se referencian
   desde varios submodulos.
#. **El index del submodulo** se actualiza cuando cambia el
   roadmap, una iniciativa cierra o abre, un ADR nuevo aplica, o
   un riesgo se agrega o cierra. La fecha de
   ``ultimo_cambio`` en ``meta::`` refleja el ultimo update real.
#. **No se crean carpetas vacias**. Si una seccion ("Decisiones
   recientes", "Riesgos abiertos") aun no tiene contenido, se
   declara explicitamente ``Sin entradas. Pendiente.`` en el
   cuerpo, no se omite la seccion.

----

Promocion de un submodulo
=========================

La primera version del ``index.rst`` de un submodulo puede
publicarse con secciones marcadas ``Pendiente`` mientras el
trabajo se acumula. Para considerarse **maduro** debe cumplir:

- Roadmap explicito (no ``Pendiente``).
- Al menos un riesgo abierto o cerrado registrado (la ausencia
  total es sintoma de falta de analisis).
- Al menos un indicador definido con baseline.
- Trazabilidad completa (todos los links obligatorios resueltos).

Submodulos no maduros se etiquetan en el ``index.rst`` con la
admonicion ``.. warning:: Submodulo en bootstrap`` hasta cumplir
los cuatro criterios.

----

Trazabilidad
============

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Procedimiento padre**
     - :doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`
   * - **Naming**
     - :doc:`/normativa/estandares/std-007-convencion-naming`
   * - **Indice del subdominio**
     - :doc:`/gestion/pm/index`
   * - **Submodulos**
     - :doc:`/gestion/pm/api/index` ·
       :doc:`/gestion/pm/db/index` ·
       :doc:`/gestion/pm/docs/index` ·
       :doc:`/gestion/pm/server/index` ·
       :doc:`/gestion/pm/ui/index`

----

Historial
=========

- ``1.0.0`` (2026-05-19) — Version inicial. Define la estructura
  obligatoria de gestion por submodulo y la plantilla minima del
  ``index.rst`` por submodulo.
