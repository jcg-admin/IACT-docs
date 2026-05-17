.. _uc-pip-02-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

Actores
-------

- **PipelineAdmin** — usuario con permiso
  ``view_pipeline_errors`` (AGR-009 ``pipeline_admin_group``).
  Inicia el caso de uso consultando el detalle de ejecuciones
  fallidas del Servicio ETL.

  .. note::

     ``PipelineAdmin`` es un rol IT/ops, distinto del actor
     ``Supervisor`` de call center (AGR-003 / AGR-012, fuera de
     scope). Ver UC_PIP_01 para la nota completa.
- **Registro de Ejecuciones** — sistema secundario que
  provee los registros con ``estado = 'fallido'``.

Precondiciones
--------------

- El usuario esta autenticado (JWT valido).
- El usuario tiene el permiso ``view_pipeline_errors`` (RBAC).
- El Registro de Ejecuciones esta accesible.

Postcondiciones
---------------

- El sistema retorna la lista de ejecuciones fallidas con el
  mensaje de error capturado para cada una.

Endpoint de referencia:

::

   GET /api/v1/etl/errores/?period=last_7d&trimestre=Q3_25

Respuesta esperada:

::

   {
     "total": 2,
     "ejecuciones": [
       {
         "id": 42,
         "source_table": "tbl_historico_t3_2025",
         "trimestre": "Q3_25",
         "started_at": "<timestamp>",
         "finished_at": "<timestamp>",
         "error_message": "...",
         "executed_by": "scheduler"
       }
     ]
   }
