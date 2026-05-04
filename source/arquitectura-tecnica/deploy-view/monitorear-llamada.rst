.. meta::
 :artefacto: AT_UC_SUP_01_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_01_deploy:

=========================================================
UC_SUP_01 — Monitorear Llamada: Deployment View
=========================================================

Distribucion fisica de nodos y artefactos para UC_SUP_01.

.. uml::
 :caption: UC_SUP_01 — Monitorear Llamada — Deployment View

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

 :doc:`/requisitos/casos-uso/supervision/uc-sup-01/requisitos-no-funcionales`
