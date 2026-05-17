.. meta::
   :artefacto: ALCANCE-AMPLIAR-DEVOPS-RUNBOOKS
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/ampliar-devops-runbooks
   :estado: Aprobado
   :version: 1.0.0

.. _alcance-ampliar-devops-runbooks:

=========================================
Alcance: Ampliar DevOps Runbooks
=========================================

Por que existe
==============

``source/devops/runbooks/`` tiene 2 runbooks migrados en el WP
``source-rebuild-operations`` (diferido). Existen 4 documentos
operativos en ``temp-holding/FASE 01/docs/operaciones/`` con
contenido real no disponible en ``source/``.

Criterio de completitud verificable
=====================================

Los 4 archivos RST existen en ``source/``, estan enlazados en
sus respectivos ``index.rst``, y el build produce 0 warnings.

In-scope
========

- ``runbook-cron-jobs-mantenimiento.rst`` (TASK-013)
- ``runbook-log-retention-policies.rst`` (TASK-019)
- ``runbook-disaster-recovery.rst`` (TASK-036)
- ``checklist-production-readiness.rst`` (TASK-038)
- Actualizacion de ``source/devops/runbooks/index.rst``
- Actualizacion de ``source/gestion/pm/checklists/index.rst``

Out-of-scope
============

- ``source/operations/`` — no se crea dominio nuevo: el
  contenido mapea a dominios existentes.
- 7 archivos de git-historico / herramientas en
  ``temp-holding/operaciones/``: no son documentacion canonica.
- ``source/infrastructure/`` (WP #10) — iniciativa separada.
- Seccion "Tecnicas de Prompt Engineering para Agente" presente
  en los TASKs: es scaffolding interno, no contenido documental.
