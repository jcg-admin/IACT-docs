.. meta::
 :artefacto: AT_UC_ALR_04_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_04_design:

==========================================================
UC_ALR_04 — Ver Historial de Alertas: Design View
==========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ALR_04 tecnicamente.

.. uml::
 :caption: UC_ALR_04 — Design View (secuencia)

 @startuml

 actor "view_alert_history" as view_alert_history
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 view_alert_history -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_alert_history : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml`
