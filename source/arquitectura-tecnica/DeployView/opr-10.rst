.. meta::
 :artefacto: AT_UC_OPR_10_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_10_deploy:

======================================================================
UC_OPR_10 — Recibir Notificacion Supervisor: Deployment View
======================================================================

Distribucion fisica de nodos y artefactos para UC_OPR_10.

.. uml::
 :caption: UC_OPR_10 — Recibir Notificacion Supervisor — Deployment View

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

 :doc:`/requisitos/casos-uso/operator/uc-opr-10/requisitos-no-funcionales`
