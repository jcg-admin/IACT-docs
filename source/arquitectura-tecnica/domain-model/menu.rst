.. meta::
 :artefacto: AT_DM_CLASS_MENU
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

.. _dm_class_menu:

====
Menu
====

Proyección del menú de navegación generada para un usuario
en un locale específico. Es el resultado de ``MenuBuilder``
recorriendo el árbol ``Domain > Section > Action`` y
filtrando por las funciones que el usuario tiene en su
``effective_set``.

El ``Menu`` no se persiste como entidad permanente: se
genera en cada login (o en cache TTL corto) y se entrega
al frontend para renderizar la barra de navegación.

.. uml::
 :caption: Clase Menu — proyección filtrada por permisos
           del árbol de navegación para un usuario.

 @startuml

 class Menu {
   + user_id : UUID
   + locale_used : String
   + generated_at : DateTime
   + cache : Boolean
   + domains : List<Domain>
   --
   + total_visible_actions() : Integer
   + has_any_visible() : Boolean
   + to_view_model() : MenuViewModel
 }

 class Domain
 class MenuViewModel

 Menu "1" *-- "1..*" Domain : composes
 Menu "1" ..> "1" MenuViewModel : <<projects>>

 note right of Menu
   Resultado de MenuBuilder.build(user, locale).
   No es entidad persistida; se genera por demanda.
   cache=true cuando viene de cache TTL corto.
 end note

 @enduml

Operaciones principales
=======================

- ``total_visible_actions()`` — agrega el conteo a través
  de domains y sections. Útil para diagnósticos: si
  devuelve 0, el usuario no ve nada en el menú (alerta
  UX).
- ``has_any_visible()`` — short circuit equivalente.
- ``to_view_model()`` — proyección serializable para el
  frontend (omite campos internos como ``cache``).

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`
  — UC principal: generar menú dinámico.

Relaciones
==========

- Compone (composición ``*--``) ``Domain``: la vida del
  menú genera y descarta sus dominios renderizados.
- Proyecta a ``MenuViewModel`` para entrega al frontend.
