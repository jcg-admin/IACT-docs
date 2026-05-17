:orphan:

.. meta::
 :artefacto: NORM_GUIA_DIFERENCIA_PROCESOS_PROCEDIMIENTOS
 :tipo: Guia Normativa
 :dominio: normativa
 :subdominio: guias
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Importante

.. _norm_guia_diferencia_procesos_procedimientos:

============================================================
Guia — Diferencia entre Procesos y Procedimientos
============================================================

Esta guia define que es un **proceso** vs. un **procedimiento**
en el corpus IACT-docs y como se nombran/almacenan ambos.

Tabla comparativa
==================

.. list-table::
 :widths: 20 40 40
 :header-rows: 1

 * - Aspecto
   - Proceso (``proc-*``)
   - Procedimiento (``proced-*``)
 * - Pregunta que responde
   - ¿Que se hace y para que?
   - ¿Como se hace, paso a paso?
 * - Granularidad
   - Alta (que actividades secuenciales)
   - Baja (instrucciones ejecutables)
 * - Audiencia
   - Stakeholders, gestion, auditoria
   - Operadores, devs, ejecutantes
 * - Estabilidad
   - Cambia poco (anos)
   - Cambia mas (meses)
 * - Ejemplos en el corpus
   - ``proc-dev-001-pipeline-trabajo-iact``,
     ``proc-doc-001-generacion-std``,
     ``proc-gob-001-mapeo-procesos-templates``
   - ``proced-dev-001-crear-pull-request``,
     ``proced-gob-002-actualizar-documentacion``,
     ``proced-devops-001-deploy-staging``

Naming
=======

- **Procesos:** ``proc-{dominio}-{NNN}-{nombre-descriptivo}.rst``
  donde ``dominio`` ∈ ``dev | devops | doc | gob | ops | qa``.
- **Procedimientos:** ``proced-{dominio}-{NNN}-{nombre-descriptivo}.rst``.
- Ambos viven en ``source/normativa/procedimientos/``.
- ``NNN`` es secuencial dentro del dominio (no global).

Relacion proceso ↔ procedimiento
==================================

Un proceso puede invocar **N** procedimientos. Un
procedimiento sirve a **uno o mas** procesos. La relacion
no es 1:1.

Ejemplo:

- **Proceso** ``proc-dev-001-pipeline-trabajo-iact`` (el
  flujo end-to-end de trabajo del equipo de desarrollo)
  invoca:

  - ``proced-dev-001-crear-pull-request``
  - ``proced-dev-002-code-review``
  - ``proced-dev-003-resolver-conflictos-merge``

----

.. seealso::

 - :doc:`/normativa/procedimientos/proc-dev-001-pipeline-trabajo-iact`
 - :doc:`/normativa/procedimientos/proced-dev-001-crear-pull-request`
 - :doc:`/normativa/gobernanza/adr-gob-001-organizacion-proyecto-por-dominio`
