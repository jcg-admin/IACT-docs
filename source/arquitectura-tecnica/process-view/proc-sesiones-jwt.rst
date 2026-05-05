.. meta::
 :artefacto: AT_PROC_SESIONES_JWT
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_proc_sesiones_jwt:

======================================================
Process View — Concurrencia de Sesiones y JWT
======================================================

Patron de concurrencia para sincronizacion de ``Session`` con JWT:
creacion del token, refresh antes de expiracion y revocacion
con invalidacion en cache (CNST-002, CNST-003).

.. uml::
 :caption: Process View — sincronizacion de sesiones JWT: creacion, refresh e invalidacion.

 @startuml

 actor AGR_OPERADOR

 participant ServicioAuth    <<api>>
 participant CacheSession    <<redis>>
 database    AlmacenDatos    <<postgresql>>

 == Creacion de sesion ==

 AGR_OPERADOR -> ServicioAuth : POST /auth/login\n{username, password}
 activate ServicioAuth

 ServicioAuth -> AlmacenDatos : SELECT User WHERE username=X
 AlmacenDatos --> ServicioAuth : User{state:ACTIVE}

 ServicioAuth -> AlmacenDatos : INSERT sessions\n{state:ACTIVE, expires_at:+8h}
 AlmacenDatos --> ServicioAuth : Session creada

 ServicioAuth -> CacheSession : SET session:{token}\n{user_id, expires_at}\nTTL=8h <<CNST-002>>
 CacheSession --> ServicioAuth : OK

 ServicioAuth --> AGR_OPERADOR : 200 OK {jwt_token}
 deactivate ServicioAuth

 == Refresh antes de expiracion ==

 AGR_OPERADOR -> ServicioAuth : POST /auth/refresh\n{jwt_token}
 activate ServicioAuth

 ServicioAuth -> CacheSession : GET session:{token} <<CNST-003>>
 CacheSession --> ServicioAuth : session activa

 ServicioAuth -> CacheSession : SET session:{new_token}\nDEL session:{old_token}
 ServicioAuth -> AlmacenDatos : UPDATE sessions\n{token=new, expires_at nuevo}
 AlmacenDatos --> ServicioAuth : OK

 ServicioAuth --> AGR_OPERADOR : 200 OK {new_jwt_token}
 deactivate ServicioAuth

 == Cierre de sesion (invalidacion) ==

 AGR_OPERADOR -> ServicioAuth : POST /auth/logout\n{jwt_token}
 activate ServicioAuth

 ServicioAuth -> CacheSession : DEL session:{token}
 CacheSession --> ServicioAuth : OK

 ServicioAuth -> AlmacenDatos : UPDATE sessions\n{state:INACTIVE}
 ServicioAuth -> AlmacenDatos : INSERT audit_events\n{event_type:LOGOUT}
 AlmacenDatos --> ServicioAuth : OK

 ServicioAuth --> AGR_OPERADOR : 200 OK
 deactivate ServicioAuth

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/session`
 :doc:`/arquitectura-tecnica/domain-model/user`
 :doc:`/arquitectura-tecnica/deploy-view/deploy-auth-cache`
