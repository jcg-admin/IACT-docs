.. meta::
 :artefacto: AT_DM_CLASS_MENU
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

.. _dm_class_menu:

====
Menu
====

Proyeccion del menu de navegacion generada para un usuario en un locale especifico.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase Menu — stub pendiente de desarrollo.

 @startuml

 class Menu {
  + user_id : UUID
  + locale_used : String
  + generated_at : DateTime
  + cache : Boolean
 }

 @enduml
