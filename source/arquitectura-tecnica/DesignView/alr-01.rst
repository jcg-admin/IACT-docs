.. meta::
 :artefacto: AT_UC_ALR_01_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_01_design:

================================================================
UC_ALR_01 — Configurar Umbrales de Alertas: Design View
================================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ALR_01 tecnicamente.

.. uml::
 :caption: UC_ALR_01 — Design View (secuencia)

 @startuml

 actor "configure_alerts" as configure_alerts
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 configure_alerts -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> configure_alerts : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml`
