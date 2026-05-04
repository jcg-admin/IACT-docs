.. meta::
 :artefacto: AT_UC_OPR_03_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_03_deploy:

================================================================
UC_OPR_03 — Realizar Llamada Saliente: Deployment View
================================================================

Distribucion fisica de nodos y artefactos para UC_OPR_03.

.. uml::
 :caption: UC_OPR_03 — Realizar Llamada Saliente — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Servidor Web" as WebServer {
   artifact "Aplicacion Backend" as App
 }
 database "Almacen de datos" as Almacen de Datos

 Client --> WebServer : HTTPS
 WebServer --> Almacen de Datos : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-03/requisitos-no-funcionales`
