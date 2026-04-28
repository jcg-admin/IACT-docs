.. meta::
   :artefacto: CNST_020
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-020:

=================================================
CNST-020: Throttling de Exportaciones por Formato
=================================================

Enunciado
---------

Las exportaciones DEBEN respetar limites cuantitativos por formato:
maximo de registros, cantidad maxima diaria por usuario y timeout de
procesamiento.

Parametros
----------

.. list-table::
   :header-rows: 1
   :widths: 15 25 25 20 15

   * - Formato
     - Max registros
     - Max/dia/usuario
     - Timeout
     - Tamano aprox
   * - CSV
     - 100 000
     - 10
     - 60 s
     - 15-20 MB
   * - Excel
     - 50 000
     - 5
     - 90 s
     - 10-15 MB
   * - PDF
     - 10 000
     - 3
     - 120 s
     - 5-10 MB

Justificacion
-------------

Previene scraping, controla uso de recursos y mantiene UX usable
(archivos mas grandes son inmanejables del lado cliente).

Verificacion
------------

.. code-block:: python

   limits = {"csv": 100_000, "xlsx": 50_000, "pdf": 10_000}
   assert export.records <= limits[export.format]

Referencias cruzadas
--------------------

- :doc:`CNST_019_Exportaciones_Asincronas_Sobre_10k_Registros`
- :doc:`CNST_011_Throttling_Obligatorio_en_Endpoints_Publicos`
