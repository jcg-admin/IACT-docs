.. meta::
 :artefacto: AT_DESIGN_ACT_JWT_AUTH
 :tipo: Diagrama Arquitectonico — Design View — Activity
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :flujo: jwt-auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_design_act_jwt_auth:

============================================================
Design View — Flujo: JWT Auth + Refresh + Blacklist
============================================================

Flujo completo de autenticacion con JWT: login emite Session,
cada request valida el JWT, refresh extiende TTL, logout
agrega el token a BlacklistedToken.

Cubre los UCs UC_AUTH_01 (login), UC_AUTH_05 (gestionar
sesiones) y la verificacion runtime de cada operacion del
sistema.

.. uml::
 :caption: Flujo JWT lifecycle — login -> request -> refresh -> logout.

 @startuml

 start
 :Cliente envia login(email, password);

 :User.verify_credentials();
 if (credenciales validas?) then (no)
   :Retornar 401;
   :Emitir AuditEvent(type=login_failed);
   stop
 else (si)
 endif

 :IdempotencyPolicy.check(request_id);
 if (request duplicado?) then (si)
   :Retornar Session existente;
   stop
 else (no)
 endif

 :ExpirationPolicy.compute_ttl();
 :Session.create(user_id, ttl);
 :Emitir JWT firmado;
 :Emitir AuditEvent(type=login_success);

 partition "Loop runtime — cada request" {
   while (request entrante?) is (si)
     :AuthorizationGuard.verify(jwt);
     if (jwt en BlacklistedToken?) then (si)
       :Retornar 401 token_revoked;
     else (no)
       :ExpirationPolicy.check(jwt.exp);
       if (expirado?) then (si)
         :Retornar 401 token_expired;
       else (no)
         :Procesar request;
       endif
     endif
   endwhile (no)
 }

 partition Refresh {
   :Cliente solicita refresh(refresh_token);
   :Session.refresh();
   :Emitir nuevo JWT;
 }

 partition Logout {
   :Cliente solicita logout(jwt);
   :BlacklistedToken.add(jwt, exp);
   :Emitir AuditEvent(type=logout);
 }

 stop

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/auth/sequence`
 - :doc:`/arquitectura-tecnica/design-view/auth/state`
 - :doc:`/arquitectura-tecnica/use-case-view/auth/index`
 - :doc:`/arquitectura-tecnica/domain-model/session`
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token`
 - :doc:`/arquitectura-tecnica/domain-model/idempotency-policy`
 - :doc:`/arquitectura-tecnica/domain-model/expiration-policy`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
