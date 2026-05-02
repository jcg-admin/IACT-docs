.. _uc-pip-01-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componentes: ``SupervisionETLView`` (DRF APIView),
``AuthorizationGuard``, ``ETLEjecucionRepo``,
``ResumenSaludBuilder``.

Contrato del servicio:

::

   contract SupervisionETLService:
     get(invoker, ctx)
       returns: ResumenSalud

Pseudocodigo:

::

   procedure get(invoker, ctx):
       require AuthorizationGuard.has(invoker, 'ver_estado_etl')
       runs = ETLEjecucionRepo.get_recientes(limit=20)
       return ResumenSaludBuilder.build(runs)

Implementacion de ETLEjecucionRepo:

::

   ETLEjecucionRepo.get_recientes(limit):
       # Consulta directa sobre etl_runs en MariaDB
       # via connections['ivr'].cursor()
       SELECT id, tabla_origen, trimestre,
              iniciado_en, finalizado_en,
              estado, registros_base,
              mensaje_error, ejecutado_por
       FROM etl_runs
       ORDER BY iniciado_en DESC
       LIMIT :limit

ResumenSaludBuilder.build(runs) calcula el estado general:

- ``ok`` si la ultima ejecucion es ``exitoso`` y
  ``finalizado_en`` esta dentro de las ultimas 14 horas.
- ``degradado`` si la ultima ejecucion exitosa tiene mas de
  14 horas pero menos de 24 horas.
- ``critico`` si no hay ninguna ejecucion exitosa en las
  ultimas 24 horas o la ultima ejecucion es ``fallido``.
