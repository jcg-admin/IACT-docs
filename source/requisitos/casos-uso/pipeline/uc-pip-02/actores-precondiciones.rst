.. _uc-pip-02-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

Actores
-------

- **Supervisor de Operaciones** — usuario con permiso
  ``ver_errores_etl``. Inicia el caso de uso consultando el
  detalle de ejecuciones fallidas del Servicio ETL.
- **Registro de Ejecuciones** — sistema secundario que
  provee los registros con ``estado = 'fallido'``.

Precondiciones
--------------

- El usuario esta autenticado (JWT valido).
- El usuario tiene el permiso ``ver_errores_etl`` (RBAC).
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
         "tabla_origen": "tbl_historico_t3_2025",
         "trimestre": "Q3_25",
         "iniciado_en": "<timestamp>",
         "finalizado_en": "<timestamp>",
         "mensaje_error": "...",
         "ejecutado_por": "scheduler"
       }
     ]
   }
