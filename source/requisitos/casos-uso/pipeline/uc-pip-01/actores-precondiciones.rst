.. _uc-pip-01-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

Actores
-------

- **Supervisor de Operaciones** — usuario con permiso
  ``view_pipeline_status``. Inicia el caso de uso consultando el
  estado del Servicio ETL.
- **Registro de Ejecuciones** — sistema secundario que
  provee los datos de ejecucion del Servicio ETL.

Precondiciones
--------------

- El usuario esta autenticado (JWT valido).
- El usuario tiene el permiso ``view_pipeline_status`` (RBAC).
- El Registro de Ejecuciones esta accesible.

Postcondiciones
---------------

- El sistema retorna el resumen de salud del Servicio ETL con
  la informacion de las ultimas ejecuciones.

Endpoint de referencia:

::

   GET /api/v1/etl/supervision/

Respuesta esperada:

::

   {
     "estado_general": "ok | degradado | critico",
     "ultima_ejecucion_exitosa": {
       "trimestre": "Q3_25",
       "finished_at": "<timestamp>",
       "base_records": 1234567
     },
     "ejecucion_en_curso": null,
     "total_exitosas_24h": 2,
     "total_fallidas_24h": 0
   }
