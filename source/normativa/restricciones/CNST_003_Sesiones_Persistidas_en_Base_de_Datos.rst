.. meta::
   :artefacto: CNST_003
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-003:

===============================================
CNST-003: Sesiones Persistidas en Base de Datos
===============================================

Enunciado
---------

Las sesiones de usuario DEBEN almacenarse en la base de datos
relacional. Esta prohibido el uso de cookies firmadas, cache externo
(Redis, Memcached) o cualquier mecanismo distinto a la BD para
persistencia de sesion.

Justificacion
-------------

Permite auditoria centralizada, revocacion inmediata y elimina
dependencias de servicios externos para una funcion critica de
seguridad.

Especificacion
--------------

- Engine obligatorio: ``django.contrib.sessions.backends.db``.
- Tabla principal: ``django_session`` (Django default).
- Tabla auxiliar de auditoria: ``UserSession`` con campos ``user``,
  ``ip``, ``user_agent``, ``last_activity``, ``is_active``.

Verificacion
------------

.. code-block:: python

   from django.conf import settings
   assert settings.SESSION_ENGINE == "django.contrib.sessions.backends.db"

Referencias cruzadas
--------------------

- :doc:`CNST_004_Sesion_Unica_por_Usuario`
- :doc:`CNST_005_Timeout_de_Sesion_de_15_Minutos`
