.. meta::
 :artefacto: AT_UC_PIP_04_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_04_deploy:

======================================================================
UC_PIP_04 — Solicitar Reintento de Pipeline: Deployment View
======================================================================

Distribucion fisica de nodos y artefactos para UC_PIP_04.

.. uml::
 :caption: UC_PIP_04 — Solicitar Reintento de Pipeline — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Apache + mod_wsgi" as WebServer {
   artifact "DisparadorETL" as App
 }
 database "MariaDB" as DB

 Client --> WebServer : HTTPS
 WebServer --> DB : SP call / TCP

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/requisitos-no-funcionales`
