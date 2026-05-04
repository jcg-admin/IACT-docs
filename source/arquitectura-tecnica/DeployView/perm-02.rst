.. meta::
 :artefacto: AT_UC_PERM_02_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_02_deploy:

===============================================================
UC_PERM_02 — Revocar Grupo a Usuario: Deployment View
===============================================================

Distribucion fisica de nodos y artefactos para UC_PERM_02.

.. uml::
 :caption: UC_PERM_02 — Revocar Grupo a Usuario — Deployment View

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

 :doc:`/requisitos/casos-uso/permissions/uc-perm-02/requisitos-no-funcionales`
