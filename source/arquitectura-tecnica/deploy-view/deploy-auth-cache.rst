.. meta::
 :artefacto: AT_DEPLOY_AUTH_CACHE
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_deploy_auth_cache:

=========================================
Deploy View — Variante Auth con Cache
=========================================

Topologia de despliegue para modulos de autenticacion y sesiones.
Anade un nodo de cache (CacheSession) al servidor de aplicacion para
optimizar la validacion de tokens JWT y reducir consultas repetitivas
a la base de datos (CNST-002, CNST-003).

.. uml::
 :caption: Deploy View IACT — variante auth con cache de sesiones.

 @startuml

 node "ClienteWeb" as ClienteWeb {
   artifact "Navegador" as Navegador
 }

 node "ServidorApp" as ServidorApp {
   artifact "BackendIACT" as BackendIACT
 }

 node "CacheSession" as CacheSession {
   artifact "SessionStore" as SessionStore
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 ClienteWeb  --> ServidorApp   : HTTPS / REST
 ServidorApp --> AlmacenDatos  : TCP / SQL
 ServidorApp --> CacheSession  : TCP / cache

 note right of CacheSession
   CNST-002: timeout de sesion.
   CNST-003: sesion unica activa.
   Valida Session.state == ACTIVE
   sin consultar DB en cada request.
 end note

 @enduml

Cubre el modulo MOD_Auth: UC_AUTH_01 (login), UC_AUTH_02 (logout),
UC_AUTH_03 (recuperar contrasena), UC_AUTH_04 (cambiar contrasena),
UC_AUTH_05 (gestionar sesiones).

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/deploy-view/deploy-estandar`
 :doc:`/arquitectura-tecnica/domain-model/session`
