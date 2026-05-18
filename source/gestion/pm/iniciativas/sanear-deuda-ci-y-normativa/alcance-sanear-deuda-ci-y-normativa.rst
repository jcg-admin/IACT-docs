.. meta::
   :artefacto: ALCANCE-SANEAR-DEUDA-CI-Y-NORMATIVA
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/sanear-deuda-ci-y-normativa
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:21:29
   :ultimo_cambio: 2026-05-18T18:21:29
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-sanear-deuda-ci-y-normativa:

==============================================
Alcance: Sanear Deuda de CI y Normativa
==============================================

Por que existe
==============

Durante la verificacion del diferido D-01 (resolver tres warnings
de ``sphinx-build -W`` heredados del port-delta) se descubrio una
cadena de deuda tecnica y normativa que excede el alcance original
de D-01:

1. ``-j auto`` en ``validate.yml`` provoca agotamiento de memoria
   (OOM-killer del kernel confirmado) al renderizar el volumen de
   diagramas PlantUML del proyecto.

2. El build de CI ejecuta ``make clean`` antes de ``sphinx-build``,
   forzando un rebuild completo de ~3000 documentos en cada
   ejecucion. Inviable en cuenta gratuita de GitHub Actions y en
   flujo agil.

3. La extension ``source/_ext/plantuml_cached.py`` presenta seis
   hallazgos de auditoria (A-01..A-06), incluido uno critico
   (``parallel_write_safe: True`` declarado falsamente, causa raiz
   adicional del OOM).

4. El procedimiento normativo aprobado
   ``proc-gob-013-nueva-iniciativa-gestion`` contiene una
   discrepancia de ruta respecto a la realidad de facto y a su
   propio ``iniciativas/index.rst``.

Criterio de completitud verificable
=====================================

* ``validate.yml`` ejecuta build incremental (sin ``make clean``,
  con cache de doctrees) y produce ``build succeeded`` con cero
  warnings bajo ``-W``.
* Los triggers de ``validate.yml`` no disparan el build completo en
  cada push de rama de trabajo, conservando la validacion en PR y
  push hacia ``develop`` y ``main``.
* El job de build completo limpio se ejecuta de forma controlada y
  con guard de visibilidad publica del repositorio para no consumir
  cupo de Actions en repositorio privado.
* Los hallazgos A-01..A-06 de ``plantuml_cached.py`` estan
  resueltos o registrados con decision explicita de diferimiento.
* ``proc-gob-013-nueva-iniciativa-gestion`` refleja la ruta real
  ``source/gestion/pm/iniciativas/{nombre-iniciativa}/``.
* Todos los documentos RST de la iniciativa existen, estan
  enlazados en sus ``index.rst`` y el build produce 0 warnings.

In-scope
========

* Rediseno de ``validate.yml``: triggers, cache de doctrees,
  eliminacion de ``make clean``, ``-j`` acotado, job de build
  completo con guard de visibilidad publica.
* Auditoria y remediacion de ``source/_ext/plantuml_cached.py``
  (A-01..A-06) y coordinacion con ``scripts/prerender-plantuml.py``.
* Correccion puntual de la ruta en
  ``proc-gob-013-nueva-iniciativa-gestion`` (hallazgo H-N1).
* Cierre formal del diferido D-01 (los tres warnings de contenido).

Out-of-scope
============

* Soporte multi-repositorio en
  ``proc-gob-013-nueva-iniciativa-gestion`` (hallazgos H-N2 y
  H-N3): el procedimiento asume IACT-docs implicitamente y carece
  de mecanismo para declarar el repositorio objetivo de una
  iniciativa. Es un cambio normativo estructural que afecta a todas
  las iniciativas futuras del sistema IACT y se difiere a una
  iniciativa dedicada. Esta iniciativa solo declara su propio
  ``:repo_objetivo: IACT-docs`` en el meta como medida local.
* Cambio de la ruta de salida de diagramas de
  ``source/_generated_diagrams/`` a ``source/_static/img/``:
  contradice la decision documentada D-03 ("la ruta sobrevive a
  make clean") y requiere analisis propio; pendiente de
  justificacion antes de incorporarse.
* Migracion a runners de pago de GitHub Actions: el proyecto es
  corporativo pero no migrara a premium por decision explicita.

Decisiones de contenido tomadas durante la lectura
====================================================

* La iniciativa se clasifica como **documental** (flujo
  ``workflow-*``): aunque toca CI y scripts, no tiene presupuesto,
  sponsor ni Project Charter, y su alcance es exclusivamente
  IACT-docs. El criterio "afecta multiples repositorios" de
  PROC-GOB-013 no se cumple.
* La correccion de PROC-GOB-013 se ejecuta como tarea interna de
  esta iniciativa (no como parche previo) para mantener
  trazabilidad y respetar el propio procedimiento de gestion de
  cambios normativos.
