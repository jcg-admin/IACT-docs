.. meta::
 :artefacto: AT_DM_CLASS_IMPACT_REPORT
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_impact_report:

============
ImpactReport
============

DTO inmutable que describe el impacto previsto de una
modificacion a un ``AccessGroup`` (AGR). Calcula que
``Function`` cambiarian de status efectivo y que ``User``
verian sus capabilities alteradas si el cambio se aplicara.

Es generado por ``EvaluatorReloader.preview_effective_set()``
y consumido por la UI de ``uc-adm-03`` para mostrar al
admin el efecto del cambio **antes** de confirmarlo. NO
persiste — vive el tiempo de un request.

.. uml::
 :caption: ImpactReport — preview de impacto de cambio
           a AccessGroup.

 @startuml

 class ImpactReport {
   + access_group_id : UUID
   + change_type : ChangeType
   + functions_added : List<Function>
   + functions_removed : List<Function>
   + affected_users : List<UUID>
   + affected_users_count : Integer
   + sod_violations : List<SodViolation>
 }

 enum ChangeType {
   ADD_FUNCTION
   REMOVE_FUNCTION
   REPLACE
 }

 class SodViolation {
   + user_id : UUID
   + rule_id : UUID
 }

 ImpactReport ..> ChangeType
 ImpactReport ..> SodViolation

 @enduml

Atributos
=========

- ``access_group_id`` — AGR objetivo del cambio.
- ``change_type`` — naturaleza del cambio simulado.
- ``functions_added/removed`` — diff frente al estado actual.
- ``affected_users`` — ids de usuarios cuya capability set
  cambia con el preview.
- ``affected_users_count`` — cardinalidad para UI sin
  expandir lista.
- ``sod_violations`` — lista no-vacia bloquea la operacion
  real (CNST-030).

Restricciones aplicables
========================

- **CNST-030** — si ``sod_violations`` no esta vacia, el UC
  no permite confirmar el cambio.
- **BR-009** — el preview no realiza cambios persistentes;
  los cambios reales requieren UC distinto.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/admin/uc-adm-03/index` —
  preview de impacto antes de modificar AGR.

Relaciones
==========

- Producido por ``EvaluatorReloader.preview_effective_set``.
- Consumido por la UI; serializado al response del
  ``Servicio de Aplicacion``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/access-group`
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`
 - :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod`
