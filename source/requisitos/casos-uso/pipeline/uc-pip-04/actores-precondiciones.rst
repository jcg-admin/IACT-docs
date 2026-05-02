.. _uc-pip-04-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

Actores
-------

- **Administrador de Pipeline** — usuario con permiso
  ``retry_etl``. Solicita el reprocesamiento de un
  trimestre del Servicio ETL.
- **Disparador ETL** — sistema que ejecuta el reintento
  invocando el Servicio ETL para el trimestre indicado.
- **Registro de Ejecuciones** — sistema que persiste el
  nuevo registro de ejecucion del reintento.

Precondiciones
--------------

- El usuario esta autenticado (JWT valido).
- El usuario tiene el permiso ``retry_etl`` (RBAC).
- No hay una ejecucion del Servicio ETL en curso al momento
  de la solicitud.

Postcondiciones
---------------

- El Servicio ETL fue invocado para reprocesar el trimestre.
- Existe un nuevo registro en el Registro de Ejecuciones con
  ``ejecutado_por = 'manual'``.
- El evento de auditoria ``ETL_REINTENTO_SOLICITADO`` fue
  emitido.

Endpoint de referencia:

::

   POST /api/v1/etl/reintento/
   body: {
     "trimestre": "Q3_25",
     "motivo": string (min 20 caracteres, obligatorio)
   }

Respuesta esperada:

::

   {
     "etl_run_id": 47,
     "trimestre": "Q3_25",
     "estado": "en_ejecucion"
   }
