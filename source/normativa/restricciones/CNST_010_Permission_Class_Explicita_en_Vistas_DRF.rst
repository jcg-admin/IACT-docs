.. meta::
   :artefacto: CNST_010
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-010:

==================================================
CNST-010: Permission Class Explicita en Vistas DRF
==================================================

Enunciado
---------

Toda vista DRF DEBE declarar ``permission_classes`` explicitamente.
Esta prohibido depender de ``DEFAULT_PERMISSION_CLASSES`` global para
endpoints que tocan datos sensibles.

Justificacion
-------------

Una permission class explicita hace auditable la autorizacion de
cada endpoint. Una permission heredada del default es opaca al
revisor.

Especificacion
--------------

- ``DEFAULT_PERMISSION_CLASSES = [IsAuthenticated]`` como fallback.
- Toda vista que opera sobre PII o catalogo RBAC declara una
  permission class especifica (``HasFunctionPermission``,
  ``IsAdminUser``).
- Esta prohibido ``permission_classes = [AllowAny]`` excepto en login.

Verificacion
------------

.. code-block:: python

   for view in get_all_drf_views():
       assert hasattr(view, "permission_classes")

Referencias cruzadas
--------------------

- :doc:`CNST_009_Autenticacion_DRF_Obligatoria`
- :doc:`CNST_029_RBAC_Modelo_Plano`
