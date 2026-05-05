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

 actor TargetUser
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
 CREAR_USUARIO --> TargetUser
 MODIFICAR_USUARIO --> TargetUser
 ELIMINAR_USUARIO --> TargetUser


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

Casos de uso del módulo
=========================

Cada UC tiene su especificación textual completa y su diagrama
individual (con `<<include>>` y `<<extend>>` per uml-07) en
``source/requisitos/casos-uso/``:

.. list-table::
 :header-rows: 1
 :widths: 20 50 30

 * - UC
   - Nombre
   - Diagrama
 * - :doc:`UC_USR_01 </requisitos/casos-uso/users/uc-usr-01/index>`
   - Crear Usuario
   - :doc:`Diagrama </requisitos/casos-uso/users/uc-usr-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_USR_02 </requisitos/casos-uso/users/uc-usr-02/index>`
   - Consultar Usuarios
   - :doc:`Diagrama </requisitos/casos-uso/users/uc-usr-02/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_USR_03 </requisitos/casos-uso/users/uc-usr-03/index>`
   - Modificar Usuario
   - :doc:`Diagrama </requisitos/casos-uso/users/uc-usr-03/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_USR_04 </requisitos/casos-uso/users/uc-usr-04/index>`
   - Eliminar Usuario
   - :doc:`Diagrama </requisitos/casos-uso/users/uc-usr-04/diagramas-uml/diagrama-de-caso-de-uso>`

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
