.. _uc-pip-03-parte-03:

==========================
Parte 3 — Flujo principal
==========================

PASO 1 — El Analista de Datos envia GET a
          ``/api/v1/datos/disponibilidad/`` con el parametro
          ``trimestre`` (opcional; sin parametro retorna el
          trimestre activo).

PASO 2 — El sistema valida el JWT y verifica que el usuario
          tiene el permiso ``view_data_availability`` (RBAC).

PASO 3 — El sistema consulta el Registro de Ejecuciones:
          ultima ejecucion con ``estado = 'exitoso'`` para el
          trimestre indicado.

PASO 4 — El sistema calcula DisponibilidadDatos:

  - ``minutos_desde_etl``: diferencia entre ``now()`` y
    ``finalizado_en`` de la ultima ejecucion exitosa.
  - ``estado_frescura``: fresco (<720 min) / degradado
    (720-1440 min) / vencido (>=1440 min).

PASO 5 — El sistema retorna 200 con el estado de
          disponibilidad de los datos IVR.

Flujo alternativo: si no existe ninguna ejecucion exitosa para
el trimestre, el sistema retorna ``estado_frescura = 'vencido'``
con ``registros_disponibles = 0`` y ``ultima_actualizacion = null``.
