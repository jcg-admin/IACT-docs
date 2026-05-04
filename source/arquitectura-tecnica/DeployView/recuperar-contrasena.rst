.. meta::
 :artefacto: AT_UC_AUTH_03_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_03_deploy:

============================================================
UC_AUTH_03 — Recuperar Contrasena: Deployment View
============================================================

Distribucion fisica de nodos y artefactos para UC_AUTH_03.

.. uml::
 :caption: UC_AUTH_03 — Recuperar Contrasena — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Apache + mod_wsgi" as WebServer {
   artifact "Django App" as App
 }
 database "Almacen de datos" as Almacen de Datos
 node "cache" as Cache

 Client --> WebServer : HTTPS
 WebServer --> Almacen de Datos : TCP / SQL
 WebServer --> Cache : TCP / cache

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-03/requisitos-no-funcionales`
