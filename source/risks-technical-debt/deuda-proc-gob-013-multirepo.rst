.. meta::
   :artefacto: DEBT_003
   :tipo: Deuda Tecnica
   :dominio: risks-technical-debt
   :estado: Resuelta
   :version: 1.1.0
   :fecha_creacion: 2026-05-18T23:28:16
   :ultimo_cambio: 2026-05-19T18:26:25
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deuda-proc-gob-013-multirepo:

==================================================
Deuda Tecnica: PROC-GOB-013 sin soporte multi-repo
==================================================

Origen
======

Iniciativa ``sanear-deuda-ci-y-normativa`` (cerrada
2026-05-18). Durante la correccion del hallazgo H-N1 (ruta) se
identificaron dos hallazgos normativos adicionales en
``proc-gob-013-nueva-iniciativa-gestion``, diferidos por
decision explicita (D5 de esa iniciativa) por ser un cambio
estructural que afecta a todas las iniciativas futuras del
sistema IACT.

Catalogo
========

.. list-table::
   :widths: 12 18 50 20
   :header-rows: 1

   * - ID
     - Origen
     - Descripcion
     - Estado
   * - DEBT-012
     - sanear-deuda-ci-y-normativa
     - H-N2: el meta-modelo de iniciativa de PROC-GOB-013 no
       tiene campo para declarar el repositorio objetivo. Se
       asume IACT-docs implicitamente. Mitigacion local
       aplicada: las iniciativas declaran
       ``:repo_objetivo:`` en su meta, pero el procedimiento
       no lo formaliza ni lo exige.
     - **Resuelta** por iniciativa
       :doc:`/gestion/pm/iniciativas/evolucionar-proc-gob-013-multirepo/index`
       en PROC-GOB-013 v2.0.0 (2026-05-19): el campo
       ``:repo_objetivo:`` es obligatorio del meta-modelo
       con dominio enumerado.
   * - DEBT-013
     - sanear-deuda-ci-y-normativa
     - H-N3: PROC-GOB-013 esta redactado como exclusivo de
       documentacion IACT-docs (rutas ``source/gestion/``,
       skills ``workflow-*``). El sistema IACT es multi-repo
       (IACT-api, IACT-ui, IACT-db). Una iniciativa cuya
       ejecucion sea en otro repo no tiene encuadre en el
       procedimiento actual.
     - **Resuelta** por iniciativa
       :doc:`/gestion/pm/iniciativas/evolucionar-proc-gob-013-multirepo/index`
       en PROC-GOB-013 v2.0.0 (2026-05-19): documentacion
       siempre en IACT-docs, ejecucion en el repo objetivo
       declarado; skills enumerados por repo.

Accion propuesta
================

Iniciativa dedicada a evolucionar PROC-GOB-013 a multi-repo:
anadir campo formal de repositorio objetivo al meta-modelo,
generalizar rutas y skills por tipo de repo, y un bump de
version mayor del procedimiento (cambio estructural, no
correccion puntual como fue H-N1 -> 1.0.1).

Por que se difirio
==================

Modificar el meta-modelo de como el proyecto gestiona TODAS
sus iniciativas es un cambio estructural de envergadura.
Absorberlo en ``sanear-deuda-ci-y-normativa`` habria
desbordado su alcance (saneamiento de CI + plantuml +
correccion puntual de normativa). El procedimiento mismo
(Fase 5 Paso 4) prevee diferir y registrar hallazgos fuera de
alcance en lugar de absorberlos. Este registro cumplio ese
paso: la deuda quedo con dueno y trazable, no silenciada
dentro de una iniciativa cerrada.

Resolucion (2026-05-19)
=======================

La iniciativa
:doc:`/gestion/pm/iniciativas/evolucionar-proc-gob-013-multirepo/index`
ejecuto el cambio estructural diferido. PROC-GOB-013 paso de
v1.0.1 a v2.0.0 con: (a) seccion "Meta-modelo de la
iniciativa" con tabla de 11 campos obligatorios, incluido
``:repo_objetivo:`` (dominio enumerado IACT, IACT-api,
IACT-db, IACT-docs, IACT-ui, multiple); (b) generalizacion
del paso 1 de la Fase 3 (documentacion siempre en IACT-docs,
ejecucion en el repo objetivo); (c) trazabilidad de skills
abierta por repo objetivo; (d) cross-reference a
PROC-GOB-014; (e) entrada de historial 2.0.0.

Iniciativas previas quedan validas; el campo se introduce
con efecto prospectivo (compatibilidad documentada en la
propia seccion Meta-modelo de PROC-GOB-013 v2.0.0).
