.. meta::
 :artefacto: AT_DM_CLASS_PERMISSION_SERVICE
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

.. _dm_class_permission_service:

=================
PermissionService
=================

Servicio deterministico de verificacion de permisos RBAC.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase PermissionService — stub pendiente de desarrollo.

 @startuml

 class PermissionService {
  + check(user_id, function_code, ctx)
  + check_bulk(user_id, codes, ctx)
 }

 @enduml
