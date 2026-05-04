.. meta::
 :artefacto: AT_UC_OPR_10_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
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
 :caption: UC_OPR_10 — Deployment View

 @startuml

 node "Softphone WebRTC" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB (tbl_historico_*)" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-10/requisitos-no-funcionales`
