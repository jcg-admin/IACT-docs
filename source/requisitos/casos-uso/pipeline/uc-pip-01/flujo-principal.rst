.. _uc-pip-01-parte-03:

==========================
Parte 3 — Flujo principal
==========================

PASO 1 — El Supervisor de Operaciones envia GET a
          ``/api/v1/etl/supervision/``.

PASO 2 — El sistema valida el JWT y verifica que el usuario
          tiene el permiso ``view_pipeline_status`` (RBAC).

PASO 3 — El sistema consulta el Registro de Ejecuciones:
          ultimas 20 ejecuciones ordenadas por ``started_at``
          descendente.

PASO 4 — El sistema construye el ResumenSalud:

  - Identifica la ultima ejecucion con ``estado = 'exitoso'``.
  - Identifica si hay una ejecucion con ``estado = 'en_ejecucion'``.
  - Identifica la ultima ejecucion con ``estado = 'fallido'``.
  - Calcula ``estado_general`` segun la antiguedad de la ultima
    ejecucion exitosa (ok / degradado / critico).

PASO 5 — El sistema retorna 200 con el ResumenSalud serializado.

Nota: el frontend puede auto-refrescar cada 30 segundos para
mantener el estado actualizado durante la ventana ETL.
