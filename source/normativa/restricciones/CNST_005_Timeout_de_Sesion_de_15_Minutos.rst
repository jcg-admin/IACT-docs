.. meta::
   :artefacto: CNST_005
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-005:

=========================================
CNST-005: Timeout de Sesion de 15 Minutos
=========================================

Enunciado
---------

La sesion de usuario DEBE expirar tras 15 minutos de inactividad. La
sesion expirada no puede reutilizarse: requiere re-autenticacion
completa.

Justificacion
-------------

Limita la ventana de exposicion de sesiones abandonadas en estaciones
compartidas. Alineado con politicas tipicas de sistemas con datos PII.

Parametros
----------

- ``SESSION_COOKIE_AGE = 900`` (15 minutos en segundos).
- ``SESSION_SAVE_EVERY_REQUEST = True`` (renueva timeout en cada
  request autenticado).
- ``SESSION_EXPIRE_AT_BROWSER_CLOSE = False`` (la BD es la fuente de
  verdad, no el navegador).

Verificacion
------------

.. code-block:: python

   from django.conf import settings
   assert settings.SESSION_COOKIE_AGE == 900
   assert settings.SESSION_SAVE_EVERY_REQUEST is True

Referencias cruzadas
--------------------

- :doc:`CNST_003_Sesiones_Persistidas_en_Base_de_Datos`
- :doc:`CNST_004_Sesion_Unica_por_Usuario`
