.. meta::
   :dominio: normativa
   :subdominio: gobernanza
   :tipo: Indice
   :estado: Aprobado
   :version: 1.0.0

.. _gob-05:
.. _gobernanza-index:

==============================================================================
Gobernanza Documental
==============================================================================

Este subdominio contiene las **politicas, procesos y estandares** que rigen
el sistema documental IACT, estableciendo las reglas de gobernanza que
garantizan calidad, consistencia y trazabilidad.

----

Proposito del Subdominio
------------------------

El subdominio ``gobernanza/`` define **como** se gestiona la documentacion:

- Quien puede crear, modificar y aprobar artefactos
- Que criterios de calidad deben cumplirse
- Como se versionan y controlan los cambios
- Como se audita el cumplimiento

----

Catalogo de Artefactos
----------------------

Modelo y Estructura
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 15 45 20 20

   * - ID
     - Titulo
     - Tipo
     - Estado
   * - :ref:`gob-01`
     - Modelo de Gobernanza IACT
     - Politica
     - Aprobado
   * - :ref:`gob-02`
     - Roles y Matriz RACI
     - Matriz
     - Aprobado
   * - :ref:`gob-07`
     - Gestion de Dominios
     - Politica
     - Aprobado

Control de Artefactos
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 15 45 20 20

   * - ID
     - Titulo
     - Tipo
     - Estado
   * - :ref:`gob-03`
     - Control de Calidad Documental
     - Proceso
     - Aprobado
   * - :ref:`gob-04`
     - Gestion de Cambios Documentales
     - Proceso
     - Aprobado
   * - :ref:`gob-05`
     - Control de Versiones
     - Estandar
     - Aprobado
   * - :ref:`gob-08`
     - Estados Documentales
     - Politica
     - Aprobado

Seguridad y Cumplimiento
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 15 45 20 20

   * - ID
     - Titulo
     - Tipo
     - Estado
   * - :ref:`gob-06`
     - Trazabilidad SDLC
     - Proceso
     - Aprobado
   * - :ref:`gob-09`
     - Politica de Clasificacion
     - Politica
     - Aprobado
   * - :ref:`gob-10`
     - Auditoria Documental
     - Proceso
     - Aprobado

----

Mapa de Dependencias
--------------------

.. code-block:: text

   GOB_01 (Modelo de Gobernanza)
      │
      ├──► GOB_02 (Roles y RACI)
      │       │
      │       └──► GOB_03 (Control de Calidad)
      │               │
      │               └──► GOB_10 (Auditoria)
      │
      ├──► GOB_07 (Gestion de Dominios)
      │
      ├──► GOB_04 (Gestion de Cambios)
      │       │
      │       └──► GOB_05 (Control de Versiones)
      │
      ├──► GOB_08 (Estados Documentales)
      │
      ├──► GOB_06 (Trazabilidad SDLC)
      │
      └──► GOB_09 (Politica de Clasificacion)
              │
              └──► GOB_10 (Auditoria)

----

Guia de Uso Rapido
------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Si necesitas saber...
     - Consulta
   * - ¿Quien aprueba que?
     - :ref:`gob-02` (Roles y RACI)
   * - ¿Como versionar un documento?
     - :ref:`gob-05` (Control de Versiones)
   * - ¿Como modificar un doc aprobado?
     - :ref:`gob-04` (Gestion de Cambios)
   * - ¿Que criterios debe cumplir un doc?
     - :ref:`gob-03` (Control de Calidad)
   * - ¿En que estado puede estar un doc?
     - :ref:`gob-08` (Estados Documentales)
   * - ¿Como se organiza la documentacion?
     - :ref:`gob-07` (Gestion de Dominios)
   * - ¿Quien puede ver este documento?
     - :ref:`gob-09` (Politica de Clasificacion)
   * - ¿Como se audita el cumplimiento?
     - :ref:`gob-10` (Auditoria Documental)
   * - ¿Como se relacionan BR, UC, FR?
     - :ref:`gob-06` (Trazabilidad SDLC)

----

Estadisticas del Subdominio
---------------------------

.. list-table::
   :widths: 50 25

   * - Total de artefactos
     - 10
   * - Politicas
     - 4
   * - Procesos
     - 4
   * - Estandares
     - 1
   * - Matrices
     - 1
   * - Estado
     - Congelado

----

----

**Owner:** PMO
**Clasificacion:** Interno
**Ultima actualizacion:** 2025-12-22