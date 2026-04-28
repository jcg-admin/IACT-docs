.. meta::
   :artefacto: CNST_012
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-012:

============================================
CNST-012: Validacion de Input via Serializer
============================================

Enunciado
---------

Todo input al sistema DEBE validarse mediante ``Serializer`` o
``ModelSerializer`` de DRF. Esta prohibido leer ``request.data``
directamente y procesarlo sin pasar por un serializer.

Justificacion
-------------

Centraliza la validacion, previene inyeccion y garantiza consistencia
de tipos. Saltarse el serializer es vector tipico de bugs de
seguridad.

Especificacion
--------------

- Cada vista que recibe payload define un serializer dedicado.
- Validaciones cruzadas usan ``validate()`` a nivel serializer.
- ``raise_exception=True`` obligatorio en ``is_valid()``.

Verificacion
------------

.. code-block:: python

   serializer = MySerializer(data=request.data)
   serializer.is_valid(raise_exception=True)

Referencias cruzadas
--------------------

- :doc:`CNST_013_Manejo_Estandarizado_de_Excepciones_DRF`
