.. meta::
 :artefacto: AT_UC_SUP_03_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_03_deploy:

==================================================================
UC_SUP_03 — Mensaje Broadcast al Equipo: Deployment View
==================================================================

Distribucion fisica de nodos y artefactos para UC_SUP_03.

.. uml::
 :caption: UC_SUP_03 — Deployment View

 @startuml

 node "Softphone WebRTC" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB (tbl_historico_*)" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/requisitos-no-funcionales`
