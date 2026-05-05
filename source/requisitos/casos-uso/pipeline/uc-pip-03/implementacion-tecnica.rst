.. _uc-pip-03-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componentes: ``DisponibilidadDatosView`` (DRF APIView),
``AuthorizationGuard``, ``PipelineExecutionRepo``,
``DisponibilidadBuilder``.

Contrato del servicio:

::

   contract DisponibilidadDatosService:
     get(trimestre, invoker, ctx)
       returns: DisponibilidadDatos

Pseudocodigo:

::

   procedure get(trimestre, invoker, ctx):
       require AuthorizationGuard.has(invoker, 'view_data_availability')
       ultima = PipelineExecutionRepo.get_ultima_exitosa(trimestre)
       if ultima is null:
           return DisponibilidadDatos(
               trimestre=trimestre,
               estado_frescura='vencido',
               registros_disponibles=0
           )
       return DisponibilidadBuilder.build(ultima)

Implementacion de PipelineExecutionRepo.get_ultima_exitosa:

::

   PipelineExecutionRepo.get_ultima_exitosa(trimestre):
       # Consulta directa sobre pipeline_runs en Almacen de Datos
       # via connections['ivr'].cursor()
       SELECT trimestre, finished_at,
              base_records
       FROM pipeline_runs
       WHERE estado = 'exitoso'
         AND trimestre = :trimestre
       ORDER BY finished_at DESC
       LIMIT 1

DisponibilidadBuilder.build(ejecucion) calcula ``minutos_desde_etl``
como la diferencia entre ``now()`` y ``ejecucion.finished_at``,
y asigna ``estado_frescura`` segun los umbrales configurados.
