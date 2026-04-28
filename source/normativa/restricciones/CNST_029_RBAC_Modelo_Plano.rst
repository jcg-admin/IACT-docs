.. meta::
   :artefacto: CNST_029
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-029:

===========================
CNST-029: RBAC Modelo Plano
===========================

Enunciado
---------

El control de acceso del sistema IACT DEBE implementarse como un
modelo RBAC plano: funciones atomicas asignadas a usuarios via
grupos, sin jerarquia ni herencia entre roles. Esta prohibido el uso
de modelos jerarquicos (RBAC inherit) o ABAC complejo.

Justificacion
-------------

El modelo plano es auditable, predecible y soportado nativamente por
``django-guardian`` u otros frameworks. Modelos jerarquicos derivan
en permisos efectivos opacos al revisor.

Especificacion
--------------

- Unidad atomica: funcion (action sobre un recurso, ej.
  ``alertas.crear``).
- Grupo: conjunto de funciones agrupadas por rol de negocio.
- Asignacion: usuario en N grupos, no roles directos sobre usuario.
- Sin herencia: si un grupo deriva de otro, sus funciones se copian
  explicitamente.

Verificacion
------------

.. code-block:: python

   user.groups.all()  # union de funciones, sin jerarquia

Referencias cruzadas
--------------------

- :doc:`CNST_030_Reglas_de_Separacion_de_Funciones_SoD`
- :doc:`CNST_031_Permisos_Temporales_Maximo_6_Meses`
