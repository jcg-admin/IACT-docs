.. meta::
 :artefacto: AT_UC_ACC_05_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_05_deploy:

===========================================================
UC_ACC_05 — Gestionar Reglas SoD: Deployment View
===========================================================

Distribucion fisica de nodos y artefactos para UC_ACC_05.

.. uml::
 :caption: UC_ACC_05 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/access/uc-acc-05/requisitos-no-funcionales`
