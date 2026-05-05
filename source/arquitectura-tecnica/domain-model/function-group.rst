.. meta::
 :artefacto: AT_DM_CLASS_FUNCTION_GROUP
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_function_group:

=============
FunctionGroup
=============

Agrupacion logica de funciones RBAC atomicas. Un ``FunctionGroup``
se asigna a un usuario via ``Assignment`` o como parte de un
``AccessGroup``. Permite gestionar permisos en bloque sin otorgarlos
individualmente.

.. uml::
 :caption: Clase FunctionGroup — agrupacion de funciones RBAC.

 @startuml

 class FunctionGroup {
   + group_id : UUID
   + name : String
   + description : String
   --
   + create_function_group()       <<create_function_group>>
   + assign_functions_to_group()   <<assign_functions_to_group>>
   + revoke_function_group()       <<revoke_function_group>>
 }


 FunctionGroup "*" -- "*" Function : contiene

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/function`
 :doc:`/arquitectura-tecnica/domain-model/access-group`
 :doc:`/arquitectura-tecnica/domain-model/assignment`
