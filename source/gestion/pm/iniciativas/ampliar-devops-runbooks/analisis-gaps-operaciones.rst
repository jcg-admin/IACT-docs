.. meta::
   :artefacto: ANALISIS-GAPS-OPERACIONES
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/ampliar-devops-runbooks
   :estado: Aprobado
   :version: 1.0.0

.. _analisis-gaps-operaciones:

=========================================
Analisis: Gaps Operaciones temp-holding
=========================================

Clasificacion de los 13 archivos en temp-holding/operaciones
=============================================================

.. list-table::
   :widths: 35 15 15 35
   :header-rows: 1

   * - Archivo
     - Tipo
     - Decision
     - Destino
   * - ``verificar_servicios.md``
     - Runbook
     - Ya migrado
     - ``source/devops/runbooks/runbook-verificar-servicios.rst``
   * - ``reprocesar_etl_fallido.md``
     - Runbook
     - Ya migrado
     - ``source/devops/runbooks/runbook-reprocesar-etl-fallido.rst``
   * - ``TASK-013-cron_jobs_maintenance.md``
     - Runbook operativo
     - Migrar T-001
     - ``source/devops/runbooks/runbook-cron-jobs-mantenimiento.rst``
   * - ``TASK-019-log_retention_policies.md``
     - Politica operativa
     - Migrar T-002
     - ``source/devops/runbooks/runbook-log-retention-policies.rst``
   * - ``TASK-036-disaster_recovery.md``
     - Runbook operativo
     - Migrar T-003
     - ``source/devops/runbooks/runbook-disaster-recovery.rst``
   * - ``TASK-038-production_readiness.md``
     - Checklist
     - Migrar T-004
     - ``source/gestion/pm/checklists/checklist-production-readiness.rst``
   * - ``FLUJO_SYNC_DEVELOP_ANTES_MERGE.md``
     - Git historico
     - No migrar
     - Merge especifico de 2025-11-13, sin valor canonico
   * - ``MERGE_STRATEGY_NO_COMMON_ANCESTOR.md``
     - Git historico
     - No migrar
     - Estrategia de merge puntual, sin valor canonico
   * - ``procedimiento_merge_analyze_scripts.md``
     - Git historico
     - No migrar
     - Merge de rama temporal, sin valor canonico
   * - ``merge_y_limpieza_ramas.md``
     - Git operativo
     - No migrar
     - Cubierto por ``source/gestion/git-workflow``
   * - ``claude_code.md``
     - Herramienta
     - No migrar
     - Documentacion de herramienta externa, no del proyecto
   * - ``github_copilot_codespaces.md``
     - Herramienta draft
     - No migrar
     - Estado draft, tecnologia futura no implementada
   * - ``post_create.md``
     - Setup Vagrant
     - No migrar
     - Cubierto por onboarding existente en ``source/onboarding/``

Prioridad MoSCoW
================

- **Must:** T-001 (cron jobs — scripts activos en produccion),
  T-003 (disaster recovery — RTO/RPO criticos)
- **Should:** T-004 (production readiness — checklist de go-live)
- **Could:** T-002 (log retention — politicas breves, baja urgencia)
