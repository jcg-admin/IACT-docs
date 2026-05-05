.. meta::
 :artefacto: AT_DM_CLASS_RBAC_REPO
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

.. _dm_class_rbac_repo:

========
RBACRepo
========

Repositorio de consultas RBAC: asignaciones DID y rol global admin.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase RBACRepo — stub pendiente de desarrollo.

 @startuml

 class RBACRepo {
  + get_did_assignments(user_id) : list[str]
  + is_global_admin(user_id) : bool
 }

 @enduml
