.. meta::
 :artefacto: AT_UC_CLI_02_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_02_deploy:

==================================================
UC_CLI_02 — Navegar IVR: Deployment View
==================================================

Distribucion fisica de nodos y artefactos para UC_CLI_02.

.. uml::
 :caption: UC_CLI_02 — Deployment View

 @startuml

 node "PBX Telefonia" as NodoFront
 node "IVR Asterisk" as NodoAPI
 database "MariaDB (tbl_historico_*)" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/caller/uc-cli-02/requisitos-no-funcionales`
