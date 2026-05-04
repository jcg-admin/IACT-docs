.. meta::
 :artefacto: AT_UC_PIP_01_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_01_deploy:

=====================================================
UC_PIP_01 — Supervisar ETL: Deployment View
=====================================================

Distribucion fisica de nodos y artefactos para UC_PIP_01.

.. uml::
 :caption: UC_PIP_01 — Supervisar ETL — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Apache + mod_wsgi" as WebServer {
   artifact "DisparadorETL" as App
 }
 database "Almacen de datos" as Almacen de Datos

 Client --> WebServer : HTTPS
 WebServer --> Almacen de Datos : SP call / TCP

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/requisitos-no-funcionales`
