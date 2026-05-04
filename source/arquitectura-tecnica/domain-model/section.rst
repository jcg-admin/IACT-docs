.. meta::
 :artefacto: AT_DM_CLASS_SECTION
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

.. _dm_class_section:

=======
Section
=======

Seccion de navegacion del menu. Contiene Actions. Hijo de Domain.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase Section — stub pendiente de desarrollo.

 @startuml

 class Section {
  + code : String
  + label : String
  + icon : String
  + order : Integer
 }

 @enduml
