.. _uc-pip-02-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades
=============

- **ETLEjecucion** — registro de una ejecucion del Servicio ETL.
  Solo los registros con ``estado = 'fallido'`` son relevantes
  para este UC.

7.2 Modelo ETLEjecucion (subset relevante)
==========================================

::

   ETLEjecucion:
     id               : identificador unico de la ejecucion
     tabla_origen     : nombre de la tabla fuente procesada
     trimestre        : codigo del trimestre (ej: Q3_25)
     iniciado_en      : timestamp de inicio de la ejecucion
     finalizado_en    : timestamp de finalizacion
     estado           : fallido  (filtro de este UC)
     mensaje_error    : descripcion del error capturado
     ejecutado_por    : 'scheduler' | 'manual'

7.3 Indices de consulta
=======================

- ``ETLEjecucion(estado, iniciado_en DESC)`` — para listar
  ejecuciones fallidas ordenadas por fecha descendente.
- ``ETLEjecucion(trimestre)`` — para filtrar por trimestre.

7.4 Notas de contenido
=======================

El campo ``mensaje_error`` contiene el mensaje de excepcion o
el codigo de error retornado por el Servicio ETL. No contiene
stack traces del sistema interno ni datos de clientes.
