.. meta::
   :artefacto: ALCANCE-EVOLUCIONAR-PROC-GOB-013-MULTIREPO
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/evolucionar-proc-gob-013-multirepo
   :repo_objetivo: multiple
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:18:39
   :ultimo_cambio: 2026-05-19T18:18:39
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-evolucionar-proc-gob-013-multirepo:

==========================================================
Alcance: Evolucionar PROC-GOB-013 a Multi-Repo
==========================================================

Por que existe
==============

El sistema IACT esta compuesto por cinco repositorios: IACT
(orquestador, con submodulos api/db/ui), IACT-api, IACT-db,
IACT-docs e IACT-ui. La gobernanza de iniciativas vive en
IACT-docs (este repo), pero el procedimiento rector
:doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`
v1.0.1 fue redactado asumiendo implicitamente que toda
iniciativa actua sobre IACT-docs:

1. Las rutas declaradas (``source/gestion/pm/iniciativas/``)
   solo existen en IACT-docs.
2. Los skills indicados (``workflow-*``) son los del repo
   IACT-docs; otros repos pueden requerir skills propios.
3. El meta-modelo de iniciativa no tiene campo para declarar
   el repositorio objetivo. Las iniciativas que lo declaran
   (``:repo_objetivo:``) lo hacen como medida local sin
   respaldo normativo.

Esta deuda quedo registrada como DEBT-012 (campo formal
ausente) y DEBT-013 (procedimiento redactado mono-repo) en
:doc:`/risks-technical-debt/deuda-proc-gob-013-multirepo`,
diferida desde la iniciativa ``sanear-deuda-ci-y-normativa``
(decision D5) por ser un cambio estructural que afecta a
todas las iniciativas futuras del sistema IACT.

Criterio de completitud verificable
=====================================

* PROC-GOB-013 v2.0.0 declara ``:repo_objetivo:`` como campo
  **obligatorio** del meta-modelo de iniciativa, con dominio
  enumerado (``IACT``, ``IACT-api``, ``IACT-db``,
  ``IACT-docs``, ``IACT-ui``, ``multiple``).
* PROC-GOB-013 v2.0.0 generaliza la "ruta de iniciativa" por
  repositorio objetivo: la ruta ``source/gestion/pm/iniciativas/``
  aplica cuando el objetivo incluye IACT-docs; para los demas
  repos, la ruta paralela es el ``source/gestion/pm/iniciativas/``
  del propio repo cuando existe, o se documenta en IACT-docs y
  se referencia desde el repo objetivo si no.
* PROC-GOB-013 v2.0.0 referencia explicitamente a PROC-GOB-014
  (gestion por submodulo) como procedimiento complementario que
  define la estructura vertical por submodulo.
* DEBT-012 y DEBT-013 estan marcadas como **Resuelta** en
  :doc:`/risks-technical-debt/deuda-proc-gob-013-multirepo`
  con referencia a esta iniciativa.
* El repositorio IACT contiene una copia funcional de
  ``.claude/`` proveniente de IACT-docs como bootstrap para
  trabajos del orquestador, demostrando uso real del
  ``:repo_objetivo: multiple``.
* Esta iniciativa cumple ella misma el nuevo meta-modelo:
  todos sus documentos declaran ``:repo_objetivo: multiple``.
* ``sphinx-build -b dummy`` produce ``build succeeded`` con
  cero warnings.

In-scope
========

* Reescritura estructural de
  ``source/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion.rst``
  a v2.0.0: meta-modelo formal, generalizacion de rutas y
  skills por tipo de repo, cross-ref a PROC-GOB-014, entrada
  de historial 2.0.0.
* Actualizacion de
  ``source/risks-technical-debt/deuda-proc-gob-013-multirepo.rst``
  marcando DEBT-012 y DEBT-013 como Resueltas.
* Integracion de ``.claude/`` de IACT-docs en el repositorio
  IACT (orquestador) como cambio cross-repo trazado dentro de
  esta iniciativa con ``:repo_objetivo: multiple``.
* Estructura completa de la iniciativa en
  ``source/gestion/pm/iniciativas/evolucionar-proc-gob-013-multirepo/``
  con sus cinco artefactos (index, alcance, analisis, tareas,
  progreso, decisiones al cierre).
* Enlace de la iniciativa en el toctree de
  ``source/gestion/pm/iniciativas/index.rst``.

Out-of-scope
============

* Migracion retroactiva de iniciativas cerradas para que
  declaren ``:repo_objetivo:`` formalmente. Las iniciativas
  cerradas (``ampliar-devops-runbooks``,
  ``crear-infrastructure-skeleton``,
  ``integrar-contenido-rescatado``,
  ``resolver-ramas-pendientes``,
  ``sanear-deuda-ci-y-normativa``) ya declaran el campo de
  facto; reescribirlas para validar contra el nuevo modelo es
  trabajo de auditoria, no de evolucion normativa.
* Cualquier trabajo sobre los casos de uso ``uc-opr-*``,
  ``uc-sup-*`` y ``uc-cli-01..05``: declarados
  explicitamente fuera de scope por el sponsor; no se
  realizan ni se implementan.
* Modificacion de PROC-GOB-014 (gestion por submodulo): es
  procedimiento complementario y reciente (creado el mismo
  ciclo, 2026-05-19) que no requiere ajuste para la evolucion
  de PROC-GOB-013. Cualquier necesidad detectada se registrara
  como deuda nueva.
* Implementacion de skills generalizados por tipo de repo
  (``workflow-api-*``, ``workflow-db-*``, etc.). El
  procedimiento solo enumera **que** skills aplicarian por
  repo; la creacion de los skills concretos es trabajo de
  cada iniciativa especifica.
* Configuracion de IACT-docs como submodulo del repo IACT (hoy
  ``.gitmodules`` declara api/db/ui pero no docs). Es una
  decision de arquitectura git que excede esta iniciativa
  normativa.

Decisiones de contenido tomadas durante la lectura
====================================================

* La iniciativa se clasifica como **documental** (flujo
  ``workflow-*`` segun PROC-GOB-013 Fase 2). Aunque toca dos
  repos, no tiene presupuesto, sponsor formal ni Project
  Charter — solo evoluciona el procedimiento que rige a las
  demas iniciativas. El criterio "multiples repositorios" se
  satisface estrictamente, pero la iniciativa es de
  metodologia, no de producto.
* PROC-GOB-014 (creado 2026-05-19) introduce la estructura
  vertical por submodulo, pero NO modifica el meta-modelo de
  iniciativa. Ambos procedimientos coexisten: PROC-GOB-013
  define **como nace** una iniciativa (con ``:repo_objetivo:``),
  PROC-GOB-014 define **donde vive** la gestion del submodulo
  afectado.
* La integracion de ``.claude/`` en IACT se incluye como
  tarea T-004 de esta iniciativa para estrenar
  ``:repo_objetivo: multiple`` con evidencia real de
  ejecucion cross-repo, no como iniciativa separada.
