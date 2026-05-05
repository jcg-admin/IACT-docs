.. meta::
 :artefacto: AT_DM_CLASS_SECTION
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

.. _dm_class_section:

=======
Section
=======

Sección de la jerarquía de navegación. Nivel intermedio
entre ``Domain`` (raíz) y ``Action`` (hoja). Agrupa
``Action`` relacionadas funcionalmente (e.g. sección
"Reportes" agrupa actions ``view_dashboard``,
``view_realtime_metrics``, ``export_reports``).

Una ``Section`` se renderiza solo si al menos una de sus
``Action`` es visible para el usuario; si todas están
filtradas por permisos, la sección entera se oculta.

.. uml::
 :caption: Clase Section — agrupador funcional de Action
           dentro de un Domain de navegación.

 @startuml

 class Section {
   + code : String
   + label : String
   + icon : String
   + order : Integer
   --
   + visible_actions(user_function_codes : Set<String>) : List<Action>
   + has_visible_actions(user_function_codes : Set<String>) : Boolean
 }

 class Domain
 class Action

 Section "*" -- "1" Domain : belongs_to
 Section "1" *-- "*" Action : composes

 note right of Section
   Composicion fuerte con Action:
   suprimir Section elimina sus Actions
   (cleanup en cascada).
 end note

 @enduml

Operaciones principales
=======================

- ``visible_actions(user_function_codes)`` — devuelve la
  sublista de actions visibles para el usuario.
- ``has_visible_actions(user_function_codes)`` — short
  circuit booleano para decidir si renderizar la sección.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`
  — generación de menú dinámico.

Relaciones
==========

- Pertenece a un ``Domain`` (asociación M:1).
- Compone (composición fuerte ``*--``) un conjunto de
  ``Action``: la vida de las acciones está ligada a la
  sección que las contiene.
