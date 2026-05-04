.. meta::
 :artefacto: AT_UC_LOG_04_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_04_deploy:

====================================================
UC_LOG_04 — Exportar Logs: Deployment View
====================================================

Distribucion fisica de nodos y artefactos para UC_LOG_04.

.. uml::
 :caption: UC_LOG_04 — Exportar Logs — Deployment View

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

 :doc:`/requisitos/casos-uso/logs/uc-log-04/requisitos-no-funcionales`
