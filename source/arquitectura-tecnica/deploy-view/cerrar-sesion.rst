.. meta::
 :artefacto: AT_UC_AUTH_02_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_02_deploy:

=====================================================
UC_AUTH_02 — Cerrar Sesion: Deployment View
=====================================================

Distribucion fisica de nodos y artefactos para UC_AUTH_02.

.. uml::
 :caption: UC_AUTH_02 — Cerrar Sesion — Deployment View

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

 :doc:`/requisitos/casos-uso/auth/uc-auth-02/requisitos-no-funcionales`
