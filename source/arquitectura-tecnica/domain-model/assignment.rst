.. meta::
 :artefacto: AT_DM_CLASS_ASSIGNMENT
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.2.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_assignment:

==========
Assignment
==========

Registro de asignacion de un ``FunctionGroup`` o ``AccessGroup`` a
un usuario. Tiene fecha de expiracion y estado propio (BR-009:
revocar, no eliminar). Un ``Assignment`` puede estar ACTIVE, EXPIRED
o REVOKED.

.. uml::
 :caption: Clase Assignment — asignacion de grupo a usuario.

 @startuml

 class Assignment {
   + assignment_id : UUID
   + user_id : UUID
   + group_ref : String       <<FunctionGroup o AccessGroup>>
   + assigned_by : UUID
   + assigned_at : DateTime
   + expires_at : DateTime
   + state : AssignmentState
   --
   + create()
   + revoke()
 }

 enum AssignmentState {
   ACTIVE
   EXPIRED
   REVOKED
 }



 Assignment -- AssignmentState
 Assignment "*" -- "1" FunctionGroup : (cuando group_ref = grupo)
 Assignment "*" -- "1" AccessGroup   : (cuando group_ref = AGR)

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/function-group`
 :doc:`/arquitectura-tecnica/domain-model/access-group`
