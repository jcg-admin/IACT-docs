.. meta::
 :artefacto: AT_DM_CLASS_ACCESS_GROUP
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_access_group:

===========
AccessGroup
===========

Perfil de acceso predefinido del sistema IACT. Los AGR identifican
el rol funcional de un usuario (AGR-001..012). Un usuario puede
tener un ``AccessGroup`` primario y asignaciones adicionales via
``Assignment``.

.. uml::
 :caption: Clase AccessGroup — perfil de acceso AGR del sistema IACT.

 @startuml

 class AccessGroup {
   + id : UUID                  <<technical PK>>
   + agr_id : String          <<AGR-001..012>>
   + name : String            <<p.ej. quality_supervisor_group>>
   + profile_description : String
   + is_system : Boolean      <<true para AGR-001..012, false para custom>>
   + state : AccessGroupState
   --
   + assign_to_user()        <<assign_function_groups>>
   + revoke_from_user()
 }

 enum AccessGroupState {
   ACTIVE
   INACTIVE
 }

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/assignment`
 :doc:`/arquitectura-tecnica/domain-model/function-group`
