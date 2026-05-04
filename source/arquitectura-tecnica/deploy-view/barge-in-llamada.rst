.. meta::
 :artefacto: AT_UC_SUP_02_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_02_deploy:

==========================================================
UC_SUP_02 — Barge-in en Llamada: Deployment View
==========================================================

Distribucion fisica de nodos y artefactos para UC_SUP_02.

.. uml::
 :caption: UC_SUP_02 — Barge-in en Llamada — Deployment View

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

 :doc:`/requisitos/casos-uso/supervision/uc-sup-02/requisitos-no-funcionales`
