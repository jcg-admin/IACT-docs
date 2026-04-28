.. meta::
   :artefacto: CNST_013
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-013:

=================================================
CNST-013: Manejo Estandarizado de Excepciones DRF
=================================================

Enunciado
---------

Las excepciones DRF DEBEN manejarse mediante un ``EXCEPTION_HANDLER``
custom que retorne respuestas estructuradas. Las excepciones NO
PUEDEN exponer trazas, paths internos o nombres de clases del backend.

Justificacion
-------------

La filtracion de detalles internos en respuestas de error es vector
clasico de reconnaissance para atacantes.

Especificacion
--------------

- ``REST_FRAMEWORK['EXCEPTION_HANDLER']`` apunta a handler custom en
  ``api/common/exceptions.py``.
- Estructura de respuesta: ``{"error": {"code": str, "message": str,
  "details": dict}}``.
- En produccion: ``DEBUG = False``, sin tracebacks en respuesta.
- Excepciones inesperadas se logean pero no se exponen.

Verificacion
------------

.. code-block:: python

   resp = client.post("/api/broken/", data={})
   assert "Traceback" not in resp.content.decode()
   assert "django." not in resp.content.decode()

Referencias cruzadas
--------------------

- :doc:`CNST_024_Logs_Estructurados_en_Formato_JSON`
