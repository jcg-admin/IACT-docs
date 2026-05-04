.. meta::
 :artefacto: AT_UC_ALR_01_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_01_deploy:

=====================================================================
UC_ALR_01 — Configurar Umbrales de Alertas: Deployment View
=====================================================================

Distribucion fisica de nodos y artefactos para UC_ALR_01.

.. uml::
 :caption: UC_ALR_01 — Configurar Umbrales de Alertas — Deployment View

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

 :doc:`/requisitos/casos-uso/alerts/uc-alr-01/requisitos-no-funcionales`
