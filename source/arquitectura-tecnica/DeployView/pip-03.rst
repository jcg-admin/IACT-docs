.. meta::
 :artefacto: AT_UC_PIP_03_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_03_deploy:

========================================================================
UC_PIP_03 — Consultar Disponibilidad de Datos: Deployment View
========================================================================

Distribucion fisica de nodos y artefactos para UC_PIP_03.

.. uml::
 :caption: UC_PIP_03 — Consultar Disponibilidad de Datos — Deployment View

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

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/requisitos-no-funcionales`
