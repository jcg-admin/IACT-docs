.. meta::
 :artefacto: AT_UC_AUD_01_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_01_deploy:

==================================================================
UC_AUD_01 — Consultar Auditoria General: Deployment View
==================================================================

Distribucion fisica de nodos y artefactos para UC_AUD_01.

.. uml::
 :caption: UC_AUD_01 — Consultar Auditoria General — Deployment View

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

 :doc:`/requisitos/casos-uso/audit/uc-aud-01/requisitos-no-funcionales`
