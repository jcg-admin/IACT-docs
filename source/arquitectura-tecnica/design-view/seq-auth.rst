.. meta::
 :artefacto: AT_DESIGN_MOD_AUTH
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_auth:

==========================================
Design View — MOD_Auth: Autenticacion
==========================================

Patron de interaccion del modulo de autenticacion. Muestra el flujo
de login: validacion de credenciales, creacion de ``Session``, emision
de token JWT y registro de ``AuditEvent(LOGIN)``.

.. uml::
 :caption: Design View MOD_Auth — secuencia de autenticacion y gestion de sesion.

 @startuml

 actor AGR_OPERADOR

 participant InterfazWeb      <<frontend>>
 participant ServicioAuth     <<api>>
 participant RepositorioUser  <<repository>>
 participant RepositorioSession <<repository>>
 database    AlmacenDatos     <<postgresql>>

 AGR_OPERADOR -> InterfazWeb : POST /auth/login\n{username, password}
 activate InterfazWeb

 InterfazWeb -> ServicioAuth : autenticar(username, password)
 activate ServicioAuth

 ServicioAuth -> RepositorioUser : buscar(username)
 activate RepositorioUser
 RepositorioUser -> AlmacenDatos : SELECT users WHERE username=?
 AlmacenDatos --> RepositorioUser : User{user_id, state:UserState}
 RepositorioUser --> ServicioAuth : User
 deactivate RepositorioUser

 alt User.state != ACTIVE
   ServicioAuth --> InterfazWeb : 401 Unauthorized
 else credenciales validas
   ServicioAuth -> RepositorioSession : crear(Session{\n  session_id:UUID,\n  user_id,\n  state:ACTIVE,\n  expires_at\n})
   activate RepositorioSession
   RepositorioSession -> AlmacenDatos : INSERT sessions
   AlmacenDatos --> RepositorioSession : OK
   RepositorioSession --> ServicioAuth : Session
   deactivate RepositorioSession

   ServicioAuth -> AlmacenDatos : INSERT audit_events\n{event_type:LOGIN, actor_user_id}
   AlmacenDatos --> ServicioAuth : AuditEvent registrado

   ServicioAuth --> InterfazWeb : 200 {jwt_token, session_id}
 end

 deactivate ServicioAuth
 InterfazWeb --> AGR_OPERADOR : dashboard
 deactivate InterfazWeb

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/session`
 :doc:`/arquitectura-tecnica/domain-model/user`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
