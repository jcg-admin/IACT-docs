.. meta::
 :artefacto: AT_DM_CLASS_NAV_DOMAIN
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

.. _dm_class_nav_domain:

======
Domain
======

Agrupador de nivel superior en la jerarquia de navegacion del menu (Menu > Domain > Section > Action).

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase Domain — stub pendiente de desarrollo.

 @startuml

 class Domain {
  + code : String
  + label : String
  + order : Integer
 }

 @enduml
