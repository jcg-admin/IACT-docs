.. meta::
 :artefacto: AT_UC_ALR_03_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_03_design:

==================================================
UC_ALR_03 — Reconocer Alerta: Design View
==================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ALR_03 tecnicamente.

.. uml::
 :caption: UC_ALR_03 — Design View (secuencia)

 @startuml

 actor "acknowledge_alert" as acknowledge_alert
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 acknowledge_alert -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> acknowledge_alert : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml`
