.. meta::
   :artefacto: TAREAS-AMPLIAR-DEVOPS-RUNBOOKS
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/ampliar-devops-runbooks
   :estado: En ejecucion
   :version: 1.0.0

.. _tareas-ampliar-devops-runbooks:

=========================================
Tareas: Ampliar DevOps Runbooks
=========================================

.. list-table::
   :widths: 10 55 20 15
   :header-rows: 1

   * - ID
     - Tarea
     - Archivo destino
     - Estado
   * - T-001
     - Crear runbook cron jobs mantenimiento (TASK-013)
     - ``devops/runbooks/runbook-cron-jobs-mantenimiento.rst``
     - Pendiente
   * - T-002
     - Crear runbook log retention policies (TASK-019)
     - ``devops/runbooks/runbook-log-retention-policies.rst``
     - Pendiente
   * - T-003
     - Crear runbook disaster recovery (TASK-036)
     - ``devops/runbooks/runbook-disaster-recovery.rst``
     - Pendiente
   * - T-004
     - Crear checklist production readiness (TASK-038)
     - ``gestion/pm/checklists/checklist-production-readiness.rst``
     - Pendiente
   * - T-005
     - Actualizar index de runbooks
     - ``devops/runbooks/index.rst``
     - Pendiente (depende T-001, T-002, T-003)
   * - T-006
     - Actualizar index de checklists
     - ``gestion/pm/checklists/index.rst``
     - Pendiente (depende T-004)
   * - T-007
     - Crear documento de decisiones
     - ``iniciativas/ampliar-devops-runbooks/decisiones-ampliar-devops-runbooks.rst``
     - Pendiente (cierre)

DAG de dependencias
===================

.. code-block:: text

   T-001 ─┐
   T-002 ─┼─► T-005 ─┐
   T-003 ─┘          ├─► T-007 (cierre)
   T-004 ──► T-006 ──┘
