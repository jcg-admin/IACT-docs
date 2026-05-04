.. meta::
 :artefacto: AT_DM_CLASS_ACTION
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

.. _dm_class_action:

======
Action
======

Item accionable del menu de navegacion. Referencia a un function_code de Function.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase Action — stub pendiente de desarrollo.

 @startuml

 class Action {
  + code : String
  + label : String
  + function_code : String
  + order : Integer
 }

 @enduml
