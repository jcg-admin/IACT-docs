.. meta::
   :artefacto: CNST_011
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-011:

======================================================
CNST-011: Throttling Obligatorio en Endpoints Publicos
======================================================

Enunciado
---------

Todo endpoint publico (login, recuperacion de password, exportaciones)
DEBE tener throttling activo. Las clases de throttling son
obligatorias y configuradas con limites especificos por tipo de
endpoint.

Justificacion
-------------

Previene ataques de fuerza bruta, scraping y abuso de recursos.

Parametros
----------

.. list-table::
   :header-rows: 1
   :widths: 50 25 25

   * - Endpoint
     - Limite
     - Scope
   * - Login
     - 5/min/IP
     - ``login``
   * - Recuperacion de password
     - 3/hora/IP
     - ``recovery``
   * - Exportacion de reportes
     - segun :doc:`CNST_020_Throttling_de_Exportaciones_por_Formato`
     - ``exports``
   * - API general autenticada
     - 100/min/usuario
     - ``user``

Verificacion
------------

.. code-block:: python

   from rest_framework.settings import api_settings
   assert "DEFAULT_THROTTLE_CLASSES" in api_settings.user_settings

Referencias cruzadas
--------------------

- :doc:`CNST_020_Throttling_de_Exportaciones_por_Formato`
