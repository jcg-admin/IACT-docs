.. meta::
 :artefacto: AT_UC_MOD_USERS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_users:

==============================================
MOD_Users — Gestion de Usuarios: UC por Modulo
==============================================

MOD_Users — Gestion de Usuarios
==================================

Altas, consultas, modificaciones y bajas logicas de usuarios IACT.
Solo usuarios con ``create_users`` o ``update_users`` pueden modificar.

.. uml::
 :caption: Figura 17 — MOD_Users: casos de uso

 @startuml
 left to right direction

 actor "create_users" as create_users
 actor "update_users" as update_users
 actor "deactivate_users" as deactivate_users
 actor "list_users" as list_users

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as U01
   usecase "UC_USR_02\nConsultar Usuarios" as U02
   usecase "UC_USR_03\nModificar Usuario" as U03
   usecase "UC_USR_04\nEliminar Usuario\n(baja logica)" as U04
 }

 create_users --> U01
 list_users --> U02
 update_users --> U02
 update_users --> U03
 deactivate_users --> U04
 deactivate_users --> U02

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
