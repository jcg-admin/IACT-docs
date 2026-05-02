.. _uc-pip-03-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

Actores
-------

- **Analista de Datos** — usuario con permiso
  ``ver_disponibilidad_datos``. Consulta la frescura de
  los datos en la Base Analitica IVR.
- **Registro de Ejecuciones** — sistema secundario que
  provee el timestamp de la ultima actualizacion exitosa.

Precondiciones
--------------

- El usuario esta autenticado (JWT valido).
- El usuario tiene el permiso ``ver_disponibilidad_datos`` (RBAC).
- El Registro de Ejecuciones esta accesible.

Postcondiciones
---------------

- El sistema retorna el estado de frescura de los datos IVR
  del trimestre consultado.

Endpoint de referencia:

::

   GET /api/v1/datos/disponibilidad/?trimestre=Q3_25

Respuesta esperada:

::

   {
     "trimestre": "Q3_25",
     "ultima_actualizacion": "<timestamp>",
     "registros_disponibles": 1234567,
     "minutos_desde_etl": 480,
     "estado_frescura": "fresco | degradado | vencido"
   }
