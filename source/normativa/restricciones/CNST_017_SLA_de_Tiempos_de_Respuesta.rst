.. meta::
   :artefacto: CNST_017
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-017:

=====================================
CNST-017: SLA de Tiempos de Respuesta
=====================================

Enunciado
---------

Los endpoints del sistema IACT DEBEN cumplir SLAs de tiempo de
respuesta segun su tipo. Endpoints que no cumplen el SLA requieren
optimizacion o reclasificacion (mover a procesamiento asincrono).

Justificacion
-------------

Tiempos de respuesta predecibles son requisito para la usabilidad y la confianza del usuario. Endpoints sin SLA definido tienden a degradarse silenciosamente con el crecimiento del dataset y se detectan solo cuando el incidente ya ocurrio.

Parametros
----------

.. list-table::
   :header-rows: 1
   :widths: 50 25 25

   * - Tipo de endpoint
     - SLA p95
     - SLA p99
   * - Lectura simple (detalle)
     - 200 ms
     - 500 ms
   * - Lectura paginada
     - 500 ms
     - 1 s
   * - Escritura (CRUD)
     - 800 ms
     - 2 s
   * - Reporte sincrono
     - 5 s
     - 10 s
   * - Login
     - 1 s
     - 2 s

Verificacion
------------

- APM en produccion (Sentry o Prometheus) con alertas por endpoint
  que exceda el p95 sostenido.

Referencias cruzadas
--------------------

- :doc:`CNST_018_Rango_Maximo_de_Consulta_de_2_Anos`
- :doc:`CNST_019_Exportaciones_Asincronas_Sobre_10k_Registros`
