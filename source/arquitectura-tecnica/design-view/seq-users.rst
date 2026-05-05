.. meta::
 :artefacto: AT_DESIGN_MOD_USER_IDENTITY
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_user_identity:

=================================================
Design View — MOD_Users: Gestion de Identidad
=================================================

Patron de interaccion del modulo de gestion de usuarios. Muestra el
flujo de creacion de ``User`` con validacion de unicidad, asignacion
de ``primary_access_group_id`` y registro de ``AuditEvent``.

.. uml::
 :caption: Design View MOD_Users — creacion y gestion de identidad de usuarios.

 @startuml

 actor AGR_ADMIN

 participant InterfazAdmin    <<frontend>>
 participant ServicioUsuarios <<api>>
 participant RepositorioUser  <<repository>>
 database    AlmacenDatos     <<postgresql>>

 AGR_ADMIN -> InterfazAdmin : POST /users\n{username, email, full_name,\n primary_access_group_id}
 activate InterfazAdmin

 InterfazAdmin -> ServicioUsuarios : crearUsuario(datos)
 activate ServicioUsuarios

 ServicioUsuarios -> RepositorioUser : existeUsername(username)
 activate RepositorioUser
 RepositorioUser -> AlmacenDatos : SELECT users WHERE username=?
 AlmacenDatos --> RepositorioUser : resultado
 RepositorioUser --> ServicioUsuarios : boolean
 deactivate RepositorioUser

 alt username ya existe
   ServicioUsuarios --> InterfazAdmin : 409 Conflict
 else username libre
   ServicioUsuarios -> RepositorioUser : crear(User{\n  user_id:UUID,\n  username,\n  email,\n  state:UserState.ACTIVE,\n  created_at\n})
   activate RepositorioUser
   RepositorioUser -> AlmacenDatos : INSERT users
   AlmacenDatos --> RepositorioUser : OK
   RepositorioUser --> ServicioUsuarios : User
   deactivate RepositorioUser

   ServicioUsuarios -> AlmacenDatos : INSERT audit_events\n{event_type:ACCESS_CHANGE,\n actor_user_id:AGR_ADMIN}
   AlmacenDatos --> ServicioUsuarios : AuditEvent registrado

   ServicioUsuarios --> InterfazAdmin : 201 Created {user_id}
 end

 deactivate ServicioUsuarios
 InterfazAdmin --> AGR_ADMIN : confirmacion
 deactivate InterfazAdmin

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/user`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
