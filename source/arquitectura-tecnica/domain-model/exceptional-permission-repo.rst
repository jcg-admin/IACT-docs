.. meta::
 :artefacto: AT_DM_CLASS_EXCEPTIONAL_PERMISSION_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_exceptional_permission_repo:

=========================
ExceptionalPermissionRepo
=========================

Repositorio de ExceptionalPermission activos por usuario y funcion.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase ExceptionalPermissionRepo — stub pendiente de desarrollo.

 @startuml

 class ExceptionalPermissionRepo {
  + find_active_revoke(user, fn)
  + find_active_grant(user, fn)
 }

 @enduml
