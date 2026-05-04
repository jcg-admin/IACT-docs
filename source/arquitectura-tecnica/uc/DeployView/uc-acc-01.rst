.. meta::
 :artefacto: AT_UC_ACC_01_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_01_deploy:

========================================================
UC_ACC_01 — Asignar Funciones: Deployment View
========================================================

Distribucion fisica de nodos y artefactos para UC_ACC_01.

.. uml::
 :caption: UC_ACC_01 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/access/uc-acc-01/requisitos-no-funcionales`
