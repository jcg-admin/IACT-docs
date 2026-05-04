.. meta::
 :artefacto: AT_DM_CLASS_EXCEPTIONAL_PERMISSION
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

.. _dm_class_exceptional_permission:

=====================
ExceptionalPermission
=====================

Permiso temporal otorgado a un usuario para una funcion especifica
fuera de su ``AccessGroup`` habitual. Requiere justificacion y tiene
rango temporal obligatorio (CNST-031: ``granted_at .. expires_at``).

.. uml::
 :caption: Clase ExceptionalPermission — permiso temporal con justificacion.

 @startuml

 class ExceptionalPermission {
   + permission_id : UUID
   + user_id : UUID
   + function_id : String
   + granted_by : UUID
   + granted_at : DateTime
   + expires_at : DateTime
   + justification : String
   + state : PermissionState
   --
   + grant()           <<grant_exceptional_permission>>
   + revoke()          <<revoke_exceptional_permission>>
 }

 enum PermissionState {
   ACTIVE
   EXPIRED
   REVOKED
 }

 class Function {
   + name : String
   + module : Module
 }

 ExceptionalPermission -- PermissionState
 ExceptionalPermission "*" -- "1" Function

 note right of ExceptionalPermission
   CNST-031: rango temporal obligatorio
   (granted_at .. expires_at).
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/function`
