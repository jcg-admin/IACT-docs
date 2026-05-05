.. _uc-pip-04-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades escritas
======================

- **ETLEjecucion** — nuevo registro creado por el Disparador ETL
  al iniciar el reintento. Campos adicionales respecto al flujo
  normal:

::

   ETLEjecucion (nuevo registro de reintento):
     estado           : en_ejecucion  (al inicio)
     ejecutado_por    : 'manual'
     tabla_origen     : nombre de la tabla fuente del trimestre
     trimestre        : trimestre que se esta reprocesando

- **RegistroAuditoria** — evento de auditoria generado por el
  sistema al ejecutar el reintento. Registra quien solicito
  el reprocesamiento y en que condiciones.

7.2 Restricciones de escritura
================================

- Solo puede existir una ETLEjecucion con ``estado = 'en_ejecucion'``
  a la vez. El Disparador ETL rechaza el reintento si detecta
  una ejecucion activa.
- El campo ``ejecutado_por = 'manual'`` distingue los reintentos
  manuales de las ejecuciones programadas por el scheduler.
