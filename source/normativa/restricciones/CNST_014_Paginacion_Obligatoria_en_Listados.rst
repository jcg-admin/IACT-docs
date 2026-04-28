.. meta::
   :artefacto: CNST_014
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-014:

============================================
CNST-014: Paginacion Obligatoria en Listados
============================================

Enunciado
---------

Todo endpoint DRF que retorne una lista DEBE paginar la respuesta.
Esta prohibido retornar ``QuerySet.all()`` sin paginar para evitar
cargas no acotadas.

Justificacion
-------------

Garantiza tiempo de respuesta predecible, controla uso de memoria y
previene exfiltracion masiva por endpoints de lectura.

Parametros
----------

- ``DEFAULT_PAGINATION_CLASS = "rest_framework.pagination.PageNumberPagination"``.
- ``PAGE_SIZE = 50``.
- Maximo override por request: ``page_size`` <= 200.

Verificacion
------------

.. code-block:: python

   resp = client.get("/api/clientes/")
   data = resp.json()
   assert "results" in data and "count" in data
   assert len(data["results"]) <= 50

Referencias cruzadas
--------------------

- :doc:`CNST_017_SLA_de_Tiempos_de_Respuesta`
