.. _uc-pip-02-parte-03:

==========================
Parte 3 — Flujo principal
==========================

PASO 1 — El Supervisor de Operaciones envia GET a
          ``/api/v1/etl/errores/`` con filtros opcionales
          (period, trimestre, pagina).

PASO 2 — El sistema valida el JWT y verifica que el usuario
          tiene el permiso ``view_pipeline_errors`` (RBAC).

PASO 3 — El sistema valida los filtros recibidos (period
          dentro de rango permitido por CNST_018, trimestre
          en formato valido si se indica).

PASO 4 — El sistema consulta el Registro de Ejecuciones
          filtrando por ``estado = 'fallido'``, period y
          trimestre, con paginacion.

PASO 5 — El sistema retorna 200 con la lista de ejecuciones
          fallidas, incluyendo ``mensaje_error`` de cada una.
