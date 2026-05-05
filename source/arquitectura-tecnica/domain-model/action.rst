.. meta::
 :artefacto: AT_DM_CLASS_ACTION
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

.. _dm_class_action:

======
Action
======

Item accionable del menú de navegación dinámico. Hoja de la
jerarquía ``Menu > Domain > Section > Action``. Cada
``Action`` referencia a una ``Function`` del catálogo RBAC
mediante ``function_code``: si el usuario tiene la función
en su ``effective_set``, la acción se renderiza; si no, el
``MenuBuilder`` la oculta.

Es entidad de configuración (catalog-driven): los códigos y
labels se editan en almacén de configuración, no en código.

.. uml::
 :caption: Clase Action — item de navegación con
           referencia a Function vía function_code.

 @startuml

 class Action {
   + code : String
   + label : String
   + function_code : String
   + order : Integer
   + icon : String
   + url_template : String
   --
   + is_visible_for(user_function_codes : Set<String>) : Boolean
   + render_url(context : NavContext) : String
 }

 class Section
 class Function

 Action "*" -- "1" Section : belongs_to
 Action ..> Function : references via function_code

 note right of Action
   function_code apunta a Function.code,
   no a un FK rigido — desacoplado para
   permitir migracion de codigos.
 end note

 @enduml

Operaciones principales
=======================

- ``is_visible_for(user_function_codes)`` — devuelve true
  si ``function_code`` ∈ ``user_function_codes``. Usado
  por ``MenuBuilder`` al filtrar.
- ``render_url(context)`` — substituye placeholders del
  ``url_template`` (e.g. ``/users/{user_id}/edit``) con
  valores de ``NavContext``.

Restricciones aplicables
========================

- ``function_code`` debe existir en ``Function.code``;
  consistencia validada en config-time, no en runtime
  (evitar costo de check en cada render del menú).

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`
  — generación de menú dinámico (consume ``Action``).

Relaciones
==========

- Pertenece a una ``Section`` (asociación M:1).
- Referencia ``Function`` por código (no FK estricto;
  acoplamiento por convención).
