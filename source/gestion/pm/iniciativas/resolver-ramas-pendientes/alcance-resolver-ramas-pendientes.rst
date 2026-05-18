.. meta::
   :artefacto: ALCANCE-RESOLVER-RAMAS-PENDIENTES
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-ramas-pendientes
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:46:00
   :ultimo_cambio: 2026-05-18T21:37:24
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-resolver-ramas-pendientes:

==================================================
Alcance: Resolver Ramas Pendientes
==================================================

Por que existe
==============

Tras integrar los PR #22, #23, #24 y crear la iniciativa
``sanear-deuda-ci-y-normativa``, el remoto conserva 5 ramas
reales sin resolver. Cada una requiere una accion distinta
(borrar, rescatar contenido, o esperar dependencia). Dejarlas
sin resolver es deuda: ramas huerfanas que esconden trabajo no
integrado o duplican lo ya integrado.

Las refs ``pr/N/*`` son refs internas de GitHub (no ramas
reales) y quedan fuera de alcance.

Criterio de completitud verificable
=====================================

* Cada una de las 5 ramas (R1..R5) tiene una resolucion
  documentada con evidencia: rescatada a ``wp-tmp/``,
  marcada para borrado, o con dependencia explicita.
* El contenido con valor no integrado de R1, R2 y R3 esta
  preservado en ``wp-tmp/`` (verificado por hash), de modo que
  las ramas puedan borrarse sin perdida.
* La estructura PROC-GOB-013 de la iniciativa esta completa
  (5 documentos + index) y enlazada en
  ``pm/iniciativas/index.rst``.

In-scope
========

* Analisis por rama (R1..R5) con verificacion por hash y por
  contenido.
* Rescate a ``wp-tmp/`` (repositorio de paso) del contenido
  con valor no integrado de R1, R2, R3.
* Identificacion de ramas a borrar (R4 sin aporte, R5
  redundante tras integrar otra iniciativa).
* Documentacion completa de la iniciativa.

Out-of-scope
============

* **Integracion real** del contenido de ``wp-tmp/`` a su
  ubicacion final en ``source/``: es una fase posterior con su
  propio analisis de sustancia (sustantivo vs trivial por
  archivo, compatibilidad de nomenclatura/modelo). ``wp-tmp/``
  solo preserva; no decide la integracion.
* Borrado fisico de las ramas remotas: lo ejecuta el usuario
  en GitHub; esta iniciativa solo identifica cuales y cuando.
* El ``source/`` de R1 (nomenclatura antigua ``UC_ACC_01``,
  ``casos_uso/``): descartado, reintroduciria deuda.

Decisiones de contenido tomadas durante la lectura
====================================================

* ``wp-tmp/`` es pasajero: queda en git log y en los
  documentos de la iniciativa, no se integra a develop ni al
  build (no requiere ``exclude_patterns`` porque la rama de
  iniciativa no llega a develop hasta decision consciente).
* La iniciativa se clasifica **documental**: operacion git
  sobre IACT-docs, sin presupuesto ni PMBOK.
* El conteo de ``git diff --name-only A...B`` sobre ramas
  ``behind`` infla el resultado; la verificacion valida es por
  hash de objeto git por archivo (lecion aplicada en R1, R2,
  R3).
