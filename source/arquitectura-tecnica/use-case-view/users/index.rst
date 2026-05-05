.. meta::
 :artefacto: AT_UC_MOD_USERS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_users:

==============================================
MOD_Users — Gestion de Usuarios: UC por Modulo
==============================================

Altas, consultas, modificaciones y bajas lógicas de usuarios
IACT. Solo el rol ``UserAdmin`` (AGR-006) modifica el catálogo
de usuarios.

.. uml::
 :caption: MOD_Users — UserAdmin gestiona el catálogo;
           cualquier rol autenticado consulta.

 @startuml
 left to right direction

 actor User
 actor UserAdmin

 User <|-- UserAdmin

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as CREAR_USUARIO
   usecase "UC_USR_02\nConsultar Usuarios" as CONSULTAR_USUARIOS
   usecase "UC_USR_03\nModificar Usuario" as MODIFICAR_USUARIO
   usecase "UC_USR_04\nEliminar Usuario\n(baja logica)" as ELIMINAR_USUARIO
 }

 User      --> CONSULTAR_USUARIOS
 UserAdmin --> CREAR_USUARIO
 UserAdmin --> MODIFICAR_USUARIO
 UserAdmin --> ELIMINAR_USUARIO

 note right of MOD_Users
   Codenames RBAC:
     User (autenticado) → list_users, view_users,
                           search_users
     UserAdmin (AGR-006) →
       create_users, update_users, delete_users,
       block_users, unblock_users, reactivate_users
   BR-009: bajas LOGICAS — UC_USR_04
   marca user.state=DELETED, no DELETE SQL.
 end note

 @enduml

Lectura del diagrama
====================

- Cualquier ``User`` autenticado consulta el catálogo
  (``UC_USR_02``).
- ``UserAdmin`` (AGR-006) hereda esa capacidad y agrega
  CRUD completo del catálogo de usuarios.
- ``UC_USR_04 Eliminar Usuario`` es una **baja lógica**
  (BR-009): marca ``state=DELETED``, nunca borra el
  registro.

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/user` — User entity (CRUD CNST + BR-009 baja lógica).

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
