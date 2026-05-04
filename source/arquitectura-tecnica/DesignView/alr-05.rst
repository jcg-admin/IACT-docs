.. meta::
 :artefacto: AT_UC_ALR_05_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_05_design:

=========================================================
UC_ALR_05 — Gestionar Suscripciones: Design View
=========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ALR_05 tecnicamente.

.. uml::
 :caption: UC_ALR_05 — Design View (secuencia)

 @startuml

 actor "subscribe_to_alert" as subscribe_to_alert
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 subscribe_to_alert -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> subscribe_to_alert : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml`
