.. meta::
 :artefacto: AT_UC_CLI_04_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_04_deploy:

=========================================================
UC_CLI_04 — Solicitar Callback: Deployment View
=========================================================

Distribucion fisica de nodos y artefactos para UC_CLI_04.

.. uml::
 :caption: UC_CLI_04 — Solicitar Callback — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Apache + mod_wsgi" as WebServer {
   artifact "Django App" as App
 }
 database "MariaDB" as MariaDB

 Client --> WebServer : HTTPS
 WebServer --> MariaDB : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/caller/uc-cli-04/requisitos-no-funcionales`
