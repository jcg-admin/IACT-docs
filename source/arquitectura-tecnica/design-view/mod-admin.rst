.. meta::
 :artefacto: AT_DESIGN_MOD_ADMIN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_admin:

=========================================
Design View — MOD_Admin: Administracion
=========================================

Patron de interaccion del modulo de administracion. Muestra la
desactivacion de ``User`` (BR-009: state → INACTIVE, no eliminar)
con revocacion de todos sus ``Assignment`` activos y registro de
``AuditEvent``.

.. uml::
 :caption: Design View MOD_Admin — desactivacion de usuario con revocacion de asignaciones.

 @startuml

 actor AGR_ADMIN

 participant InterfazAdmin        <<frontend>>
 participant ServicioAdmin        <<api>>
 participant RepositorioUser      <<repository>>
 participant RepositorioAssignment <<repository>>
 database    AlmacenDatos         <<postgresql>>

 AGR_ADMIN -> InterfazAdmin : DELETE /users/{user_id}
 activate InterfazAdmin

 InterfazAdmin -> ServicioAdmin : desactivarUsuario(user_id)
 activate ServicioAdmin

 ServicioAdmin -> RepositorioUser : buscar(user_id)
 activate RepositorioUser
 RepositorioUser -> AlmacenDatos : SELECT users WHERE user_id=?
 AlmacenDatos --> RepositorioUser : User
 RepositorioUser --> ServicioAdmin : User
 deactivate RepositorioUser

 note right of ServicioAdmin
   BR-009 v2.0.0: desactivar, no eliminar.
   User.state → INACTIVE
 end note

 ServicioAdmin -> RepositorioAssignment : revocarTodos(user_id)
 activate RepositorioAssignment
 RepositorioAssignment -> AlmacenDatos : UPDATE assignments\nSET state=REVOKED\nWHERE user_id=? AND state=ACTIVE
 AlmacenDatos --> RepositorioAssignment : N filas actualizadas
 RepositorioAssignment --> ServicioAdmin : OK
 deactivate RepositorioAssignment

 ServicioAdmin -> RepositorioUser : actualizar(User{state:UserState.INACTIVE})
 activate RepositorioUser
 RepositorioUser -> AlmacenDatos : UPDATE users SET state=INACTIVE
 AlmacenDatos --> RepositorioUser : OK
 RepositorioUser --> ServicioAdmin : User actualizado
 deactivate RepositorioUser

 ServicioAdmin -> AlmacenDatos : INSERT audit_events\n{event_type:ACCESS_CHANGE,\n details:{user_id, accion:DEACTIVATE}}
 AlmacenDatos --> ServicioAdmin : AuditEvent registrado

 ServicioAdmin --> InterfazAdmin : 200 OK
 deactivate ServicioAdmin
 InterfazAdmin --> AGR_ADMIN : confirmacion
 deactivate InterfazAdmin

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/user`
 :doc:`/arquitectura-tecnica/domain-model/assignment`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
