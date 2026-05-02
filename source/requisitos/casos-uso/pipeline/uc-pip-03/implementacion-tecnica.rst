.. _uc-pip-03-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componentes: ``DisponibilidadDatosView`` (DRF APIView),
``AuthorizationGuard``, ``ETLEjecucionRepo``,
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
       ultima = ETLEjecucionRepo.get_ultima_exitosa(trimestre)
       if ultima is null:
           return DisponibilidadDatos(
               trimestre=trimestre,
               estado_frescura='vencido',
               registros_disponibles=0
           )
       return DisponibilidadBuilder.build(ultima)

Implementacion de ETLEjecucionRepo.get_ultima_exitosa:

::

   ETLEjecucionRepo.get_ultima_exitosa(trimestre):
       # Consulta directa sobre etl_runs en MariaDB
       # via connections['ivr'].cursor()
       SELECT trimestre, finalizado_en,
              registros_base
       FROM etl_runs
       WHERE estado = 'exitoso'
         AND trimestre = :trimestre
       ORDER BY finalizado_en DESC
       LIMIT 1

DisponibilidadBuilder.build(ejecucion) calcula ``minutos_desde_etl``
como la diferencia entre ``now()`` y ``ejecucion.finalizado_en``,
y asigna ``estado_frescura`` segun los umbrales configurados.
