.. _uc-pip-01-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componentes: ``SupervisionETLView`` (DRF APIView),
``AuthorizationGuard``, ``PipelineExecutionRepo``,
``ResumenSaludBuilder``.

Contrato del servicio:

::

   contract SupervisionETLService:
     get(invoker, ctx)
       returns: ResumenSalud

Pseudocodigo:

::

   procedure get(invoker, ctx):
       require AuthorizationGuard.has(invoker, 'view_pipeline_status')
       runs = PipelineExecutionRepo.get_recientes(limit=20)
       return ResumenSaludBuilder.build(runs)

Implementacion de PipelineExecutionRepo:

::

   PipelineExecutionRepo.get_recientes(limit):
       # Consulta directa sobre pipeline_runs en Almacen de Datos
       # via connections['ivr'].cursor()
       SELECT id, source_table, trimestre,
              started_at, finished_at,
              estado, base_records,
              error_message, executed_by
       FROM pipeline_runs
       ORDER BY started_at DESC
       LIMIT :limit

ResumenSaludBuilder.build(runs) calcula el estado general:

- ``ok`` si la ultima ejecucion es ``exitoso`` y
  ``finished_at`` esta dentro de las ultimas 14 horas.
- ``degradado`` si la ultima ejecucion exitosa tiene mas de
  14 horas pero menos de 24 horas.
- ``critico`` si no hay ninguna ejecucion exitosa en las
  ultimas 24 horas o la ultima ejecucion es ``fallido``.
