.. _uc-pip-01-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades
=============

- **ETLEjecucion** — registro de una ejecucion del Servicio ETL.
- **ResumenSalud** — proyeccion de lectura construida a partir de
  los ultimos registros de ETLEjecucion.

7.2 Modelo ETLEjecucion
=======================

::

   ETLEjecucion:
     id               : identificador unico de la ejecucion
     tabla_origen     : nombre de la tabla fuente procesada
     trimestre        : codigo del trimestre (ej: Q3_25)
     iniciado_en      : timestamp de inicio de la ejecucion
     finalizado_en    : timestamp de finalizacion (nulo si aun corre)
     estado           : en_ejecucion | exitoso | fallido
     registros_base   : filas en Base Analitica IVR tras el ETL
     mensaje_error    : descripcion del error (nulo si exitoso)
     ejecutado_por    : 'scheduler' | 'manual'

7.3 Indices de consulta
=======================

- ``ETLEjecucion(estado, iniciado_en DESC)`` — para obtener
  las ultimas ejecuciones por estado.
- ``ETLEjecucion(trimestre)`` — para filtrar por trimestre.

7.4 Proyeccion ResumenSalud
============================

El ResumenSalud no es una entidad persistida. Es una proyeccion
de lectura calculada en tiempo de consulta a partir de los
registros de ETLEjecucion:

::

   ResumenSalud:
     ultima_ejecucion_exitosa : ETLEjecucion o nulo
     ejecucion_en_curso       : ETLEjecucion o nulo
     ultima_ejecucion_fallida : ETLEjecucion o nulo
     total_exitosas_24h       : entero
     total_fallidas_24h       : entero
     estado_general           : ok | degradado | critico
