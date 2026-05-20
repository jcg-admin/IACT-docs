.. meta::
   :artefacto: INICIATIVA-EVOLUCIONAR-PROC-GOB-013-MULTIREPO
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.1.0
   :fecha_creacion: 2026-05-19T18:18:39
   :ultimo_cambio: 2026-05-19T18:26:25
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-evolucionar-proc-gob-013-multirepo:

==========================================================
Iniciativa: Evolucionar PROC-GOB-013 a Multi-Repo
==========================================================

Resuelve la deuda tecnica DEBT-012 y DEBT-013 registradas en
:doc:`/risks-technical-debt/deuda-proc-gob-013-multirepo`,
diferidas por decision explicita (D5) de la iniciativa
``sanear-deuda-ci-y-normativa``.

PROC-GOB-013 (1.0.1) esta redactado de facto como exclusivo de
IACT-docs y carece de un campo formal para declarar el
repositorio objetivo de una iniciativa. Esta evolucion
formaliza ``:repo_objetivo:`` en el meta-modelo, generaliza
las rutas y skills por tipo de repositorio, y referencia
explicitamente a PROC-GOB-014 (gestion por submodulo) como
complemento natural. El cambio es estructural y dispara un
bump mayor 1.0.1 -> 2.0.0.

Esta iniciativa es la primera del sistema con
``:repo_objetivo: multiple`` y toca dos repos del orquestador:
IACT-docs (normativa) y IACT (bootstrap del .claude/).

.. toctree::
   :maxdepth: 1

   alcance-evolucionar-proc-gob-013-multirepo
   analisis-evolucionar-proc-gob-013-multirepo
   tareas-evolucionar-proc-gob-013-multirepo
   progreso-evolucionar-proc-gob-013-multirepo
   decisiones-evolucionar-proc-gob-013-multirepo
