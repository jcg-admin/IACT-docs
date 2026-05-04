.. meta::
 :artefacto: AT_UC_LOG_07_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_07_deploy:

============================================================
UC_LOG_07 — Ver Metricas Tecnicas: Deployment View
============================================================

Distribucion fisica de nodos y artefactos para UC_LOG_07.

.. uml::
 :caption: UC_LOG_07 — Ver Metricas Tecnicas — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Apache + mod_wsgi" as WebServer {
   artifact "Django App" as App
 }
 database "MariaDB" as DB

 Client --> WebServer : HTTPS
 WebServer --> DB : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-07/requisitos-no-funcionales`
