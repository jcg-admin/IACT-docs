.. meta::
 :artefacto: AT_UC_ALR_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_02_design:

=====================================================
UC_ALR_02 — Ver Alertas Activas: Design View
=====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ALR_02 tecnicamente.

.. uml::
 :caption: UC_ALR_02 — Design View (secuencia)

 @startuml

 actor "view_alerts" as view_alerts
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 view_alerts -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_alerts : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml`
