.. _uc-pip-04-parte-03:

==========================
Parte 3 — Flujo principal
==========================

PASO 1 — El Administrador de Pipeline envia POST a
          ``/api/v1/etl/reintento/`` con ``trimestre`` y
          ``motivo``.

PASO 2 — El sistema valida el JWT y verifica que el usuario
          tiene el permiso ``request_pipeline_retry`` (RBAC).

PASO 3 — El sistema valida los parametros:

  - ``trimestre`` en formato valido (ej: Q3_25).
  - ``motivo`` con minimo 20 caracteres.

PASO 4 — El sistema verifica que no hay ejecucion en curso:

  - Consulta el Registro de Ejecuciones buscando registros
    con ``estado = 'IN_PROGRESS'``.
  - Si existe una ejecucion activa: retorna 409 Conflict.

PASO 5 — El sistema registra el reintento en el Registro de
          Ejecuciones con ``estado = 'IN_PROGRESS'`` y
          ``executed_by = 'manual'``.

PASO 6 — El sistema invoca el Disparador ETL para el trimestre
          indicado. El Disparador ETL llama al Servicio ETL
          con el modo de reprocesamiento completo (equivalente
          a un backfill del trimestre).

PASO 7 — El sistema emite el evento de auditoria
          ``ETL_REINTENTO_SOLICITADO`` con actor, motivo y
          el identificador de la nueva ejecucion.

PASO 8 — El sistema retorna 202 Accepted con el identificador
          de la nueva ejecucion en curso.

3.1 Resumen
===========

.. list-table::
 :widths: 8 50 22 20

 * - Paso
   - Accion
   - Componente
   - CNST
 * - 1-3
   - POST + JWT + RBAC + validar
   - Endpoint / Guard / Validator
   - 009
 * - 4
   - Verificar no hay ejecucion activa
   - PipelineExecutionRepo
   - —
 * - 5
   - Registrar nuevo reintento
   - PipelineExecutionRepo
   - —
 * - 6
   - Invocar Disparador ETL (reproceso completo)
   - DisparadorETL
   - 008
 * - 7
   - Auditoria
   - AuditService
   - 025
 * - 8
   - 202 Accepted
   - View
   - —
