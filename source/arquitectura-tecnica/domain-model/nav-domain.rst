.. meta::
 :artefacto: AT_DM_CLASS_NAV_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_nav_domain:

======
Domain
======

Agrupador de nivel superior en la jerarquía de navegación
del menú: ``Menu > Domain > Section > Action``. Representa
áreas funcionales mayores (e.g. "Operación", "Reportes",
"Administración").

El nombre de archivo es ``nav-domain.rst`` para
desambiguar del concepto ``bounded_context`` (también
llamado *domain* en DDD); la clase en sí se llama
``Domain``.

.. uml::
 :caption: Clase Domain (nav) — raíz de la jerarquía de
           navegación del menú.

 @startuml

 class Domain {
   + code : String
   + label : String
   + order : Integer
   --
   + visible_sections(user_function_codes : Set<String>) : List<Section>
   + has_visible_sections(user_function_codes : Set<String>) : Boolean
 }

 class Menu
 class Section

 Domain "*" -- "1" Menu : belongs_to
 Domain "1" *-- "*" Section : composes

 note right of Domain
   "Domain" en navegacion ≠ bounded_context
   en DDD. Archivo nav-domain.rst para
   desambiguar en el filesystem.
 end note

 @enduml

Operaciones principales
=======================

- ``visible_sections(user_function_codes)`` — devuelve
  ``Section`` que tienen al menos una ``Action`` visible
  para el usuario.
- ``has_visible_sections(user_function_codes)`` — short
  circuit para decidir si renderizar el dominio.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`
  — generación de menú dinámico.

Relaciones
==========

- Pertenece a un ``Menu`` (asociación M:1, jerárquica).
- Compone ``Section`` (composición fuerte ``*--``).
