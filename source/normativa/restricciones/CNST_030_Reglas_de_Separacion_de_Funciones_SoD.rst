.. meta::
   :artefacto: CNST_030
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-030:

===============================================
CNST-030: Reglas de Separacion de Funciones SoD
===============================================

Enunciado
---------

Las reglas de SoD (Separation of Duties) DEBEN declararse atomicamente
y enforzarse en tiempo de asignacion. La asignacion de un grupo que
crea conflicto SoD con otro grupo del usuario DEBE rechazarse con
error explicito.

Justificacion
-------------

SoD previene fraude y errores por concentracion de poder. Las reglas
SoD textuales (no atomicas) son ineficaces porque dependen del
revisor humano.

Especificacion
--------------

- Modelo ``SoDRule`` con campos ``group_a``, ``group_b``, ``rationale``.
- Validacion en signal ``pre_save`` de ``UserGroup``: rechaza si la
  asignacion crea un par prohibido.
- Reporte periodico de violaciones existentes (sanity check).

Verificacion
------------

.. code-block:: python

   # signal handler
   def on_user_group_save(sender, instance, **kwargs):
       conflicting = SoDRule.find_conflict(instance.user, instance.group)
       if conflicting:
           raise ValidationError(f"SoD: conflict with {conflicting}")

Referencias cruzadas
--------------------

- :doc:`CNST_029_RBAC_Modelo_Plano`
- :doc:`CNST_031_Permisos_Temporales_Maximo_6_Meses`
