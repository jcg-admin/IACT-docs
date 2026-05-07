.. _uc-acc-04-parte-08-diagrama-agr-como-agregacion:

8.4 Diagrama de AGR como agregacion
====================================

.. uml::
 :caption: AGR contiene Functions via FunctionGroupMembership;
           UC_ACC_04 crea el UserAccessGroupAssignment.

 @startuml

 class User {
   + id : UUID
   + username : String
   + segment_id : Integer (BR-012)
 }

 class UserAccessGroupAssignment {
   + id : UUID
   + user : User
   + group : AccessGroup
   + state : AssignmentState
   + granted_at : DateTime
   + granted_by : User
   + expires_at : DateTime
 }

 class AccessGroup {
   + id : UUID
   + agr_code : String
   + name : String
   + is_system : Boolean
   + state : AccessGroupState
 }

 class FunctionGroupMembership {
   + id : UUID
   + group : AccessGroup
   + function : Function
   + added_at : DateTime
 }

 class Function {
   + id : UUID
   + codename : String
   + module : Module
   + is_active : Boolean
   + is_critical : Boolean
 }

 User "1" --> "*" UserAccessGroupAssignment : has
 UserAccessGroupAssignment "*" --> "1" AccessGroup : grants
 AccessGroup "1" o-- "*" FunctionGroupMembership : composes
 FunctionGroupMembership "*" --> "1" Function : binds

 note right of UserAccessGroupAssignment
   UC_ACC_04 crea ESTE registro:
     state='ACTIVE',
     granted_by=invoker,
     expires_at opcional.
 end note

 note right of FunctionGroupMembership
   UC_PERM_06 manipula esta tabla
   (composicion del AGR — quien
   tiene que Function dentro del AGR).
 end note

 note bottom of Function
   v5.6.x: campo is_critical=True
   fuerza bypass de cache (AP-2b).
   Ver ADR-BACK-010.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user`.
 - :doc:`/arquitectura-tecnica/domain-model/assignment` —
   UserAccessGroupAssignment.
 - :doc:`/arquitectura-tecnica/domain-model/access-group`.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function`
   — FunctionGroupMembership.
 - :doc:`/arquitectura-tecnica/domain-model/function`.
 - :doc:`/backend/adr-back-010-function-is-critical-governance`
   (campo is_critical).
