.. meta::
   :artefacto: CNST_031
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-031:

============================================
CNST-031: Permisos Temporales Maximo 6 Meses
============================================

Enunciado
---------

Los permisos temporales DEBEN tener vigencia maxima de 6 meses,
justificacion obligatoria de minimo 20 caracteres y revocacion
automatica al vencer. No existe auto-renovacion: cada renovacion
requiere nueva justificacion y nueva aprobacion.

Justificacion
-------------

Limita la acumulacion de permisos olvidados. La justificacion textual
acotada permite trazabilidad para auditoria. La revocacion automatica
elimina la responsabilidad del olvido humano.

Parametros
----------

- Vigencia maxima: 6 meses (180 dias) desde la asignacion.
- Justificacion: minimo 20 caracteres, texto libre.
- Revocacion: proceso programado diario que desasigna permisos
  vencidos.
- Auditoria: cada uso del permiso temporal genera registro en
  ``AuditLog`` (CNST_025).
- SoD: la validacion de :doc:`CNST_030_Reglas_de_Separacion_de_Funciones_SoD`
  aplica tambien a permisos temporales.

Verificacion
------------

.. code-block:: python

   assert (perm.expires_at - perm.granted_at).days <= 180
   assert len(perm.justification) >= 20

Referencias cruzadas
--------------------

- :doc:`CNST_029_RBAC_Modelo_Plano`
- :doc:`CNST_030_Reglas_de_Separacion_de_Funciones_SoD`
- :doc:`CNST_025_Auditoria_Inmutable_Append_Only`
