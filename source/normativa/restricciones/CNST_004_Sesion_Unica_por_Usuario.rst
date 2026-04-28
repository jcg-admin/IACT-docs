.. meta::
   :artefacto: CNST_004
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-004:

==================================
CNST-004: Sesion Unica por Usuario
==================================

Enunciado
---------

Un usuario solo PUEDE tener una sesion activa simultanea. Al iniciar
una nueva sesion, todas las sesiones previas del mismo usuario deben
invalidarse automaticamente.

Justificacion
-------------

Reduce la superficie de ataque por credenciales comprometidas y
simplifica la auditoria al asociar cada accion con un origen unico.

Especificacion
--------------

- Al login exitoso: invalidar todas las sesiones activas del usuario
  antes de crear la nueva.
- ``UserSession.is_active = False`` para todas las sesiones previas.
- La fila correspondiente en ``django_session`` se elimina.

Verificacion
------------

.. code-block:: python

   assert UserSession.objects.filter(user=u, is_active=True).count() == 1

Referencias cruzadas
--------------------

- :doc:`CNST_003_Sesiones_Persistidas_en_Base_de_Datos`
- :doc:`CNST_005_Timeout_de_Sesion_de_15_Minutos`
