.. meta::
   :artefacto: CNST_009
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-009:

=======================================
CNST-009: Autenticacion DRF Obligatoria
=======================================

Enunciado
---------

Toda vista DRF (``APIView``, ``ViewSet``, ``GenericAPIView``) DEBE
requerir autenticacion del cliente. La unica excepcion permitida es
el endpoint de login.

Justificacion
-------------

El sistema IACT maneja datos PII y operaciones sensibles. Endpoints
sin autenticacion son superficie de ataque inaceptable.

Especificacion
--------------

- ``DEFAULT_AUTHENTICATION_CLASSES`` incluye ``SessionAuthentication``
  y ``TokenAuthentication``.
- Vistas con ``authentication_classes = []`` requieren ADR explicito
  con justificacion documentada.

Verificacion
------------

.. code-block:: python

   for view in get_all_drf_views():
       if view.__name__ != "LoginView":
           assert view.authentication_classes

Referencias cruzadas
--------------------

- :doc:`CNST_010_Permission_Class_Explicita_en_Vistas_DRF`
