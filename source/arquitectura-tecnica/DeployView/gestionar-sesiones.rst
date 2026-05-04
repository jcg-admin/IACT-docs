.. meta::
 :artefacto: AT_UC_AUTH_05_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_05_deploy:

==========================================================
UC_AUTH_05 — Gestionar Sesiones: Deployment View
==========================================================

Distribucion fisica de nodos y artefactos para UC_AUTH_05.

.. uml::
 :caption: UC_AUTH_05 — Gestionar Sesiones — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Servidor Web" as WebServer {
   artifact "Aplicacion Backend" as App
 }
 database "Almacen de datos" as Almacen de Datos
 node "cache" as Cache

 Client --> WebServer : HTTPS
 WebServer --> Almacen de Datos : TCP / SQL
 WebServer --> Cache : TCP / cache

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-05/requisitos-no-funcionales`
