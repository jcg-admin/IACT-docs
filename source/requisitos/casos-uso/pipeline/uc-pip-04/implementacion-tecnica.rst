.. _uc-pip-04-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componentes: ``ReintentarETLView`` (DRF APIView),
``AuthorizationGuard``, ``ETLEjecucionRepo``,
``DisparadorETL``, ``AuditService``.

Contrato del servicio:

::

   contract ReintentarETLService:
     retry(trimestre, motivo, invoker, ctx)
       returns: ETLEjecucionRef

Pseudocodigo:

::

   procedure retry(trimestre, motivo, invoker, ctx):
       require AuthorizationGuard.has(invoker, 'request_pipeline_retry')
       if len(motivo) < 20:
           raise ValidationError('motivo_muy_corto')
       ejecucion_activa = ETLEjecucionRepo.get_activa()
       if ejecucion_activa is not null:
           raise ConflictoEjecucion(ejecucion_activa.id)
       nueva = ETLEjecucionRepo.crear_manual(
           trimestre=trimestre,
           ejecutado_por='manual'
       )
       DisparadorETL.ejecutar_historico(
           trimestre=trimestre,
           etl_run_id=nueva.id
       )
       AuditService.emit(
           'ETL_REINTENTO_SOLICITADO',
           actor_id=invoker.id,
           payload={trimestre, motivo, etl_run_id: nueva.id}
       )
       return ETLEjecucionRef(id=nueva.id)

Implementacion de DisparadorETL.ejecutar_historico:

::

   DisparadorETL.ejecutar_historico(trimestre, etl_run_id):
       # Parsea trimestre: Q3_25 -> year=2025, quarter=3
       year, quarter = parse_trimestre(trimestre)
       # Llama sp_etl_historico via management command asincronico
       # o directamente via cursor si es sincrono:
       CALL sp_etl_historico(:year, :quarter_num)
       # Al finalizar actualiza etl_runs con estado y registros_base

El reintento usa ``sp_etl_historico(year, quarter_num)`` que
reprocesa el trimestre completo via TRUNCATE + INSERT desde
``tbl_historico_*``. Garantiza idempotencia: ejecutar dos veces
produce el mismo resultado que ejecutar una vez.
