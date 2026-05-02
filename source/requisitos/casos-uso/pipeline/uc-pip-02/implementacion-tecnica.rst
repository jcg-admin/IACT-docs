.. _uc-pip-02-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componentes: ``ErroresETLView`` (DRF APIView),
``AuthorizationGuard``, ``ETLEjecucionRepo``.

Contrato del servicio:

::

   contract ErroresETLService:
     get(filters, period, page, invoker, ctx)
       returns: ListaErroresETL

Pseudocodigo:

::

   procedure get(filters, period, page, invoker, ctx):
       require AuthorizationGuard.has(invoker, 'view_etl_errors')
       ejecuciones = ETLEjecucionRepo.get_fallidas(
           period=period,
           trimestre=filters.trimestre,
           page=page
       )
       return ListaErroresETL(ejecuciones)

Implementacion de ETLEjecucionRepo.get_fallidas:

::

   ETLEjecucionRepo.get_fallidas(period, trimestre, page):
       # Consulta directa sobre etl_runs en MariaDB
       # via connections['ivr'].cursor()
       SELECT id, tabla_origen, trimestre,
              iniciado_en, finalizado_en,
              mensaje_error, ejecutado_por
       FROM etl_runs
       WHERE estado = 'fallido'
         AND iniciado_en >= :period_start
         AND (:trimestre IS NULL OR trimestre = :trimestre)
       ORDER BY iniciado_en DESC
       LIMIT :page_size OFFSET :offset

El campo ``mensaje_error`` se retorna tal como fue almacenado
por el Disparador ETL. No se aplica sanitizacion adicional en
la capa de presentacion dado que el mensaje es generado por el
sistema interno (no por input de usuario).
