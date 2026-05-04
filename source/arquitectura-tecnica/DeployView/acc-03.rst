.. meta::
 :artefacto: AT_UC_ACC_03_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_03_deploy:

===================================================================
UC_ACC_03 — Consultar Permisos Efectivos: Deployment View
===================================================================

Distribucion fisica de nodos y artefactos para UC_ACC_03.

.. uml::
 :caption: UC_ACC_03 — Consultar Permisos Efectivos — Deployment View

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

 :doc:`/requisitos/casos-uso/access/uc-acc-03/requisitos-no-funcionales`
