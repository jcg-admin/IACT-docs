.. meta::
 :artefacto: AT_UC_LOG_07_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_07_design:

=======================================================
UC_LOG_07 — Ver Metricas Tecnicas: Design View
=======================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_LOG_07 tecnicamente.

.. uml::
 :caption: UC_LOG_07 — Design View (secuencia)

 @startuml

 actor "view_technical_metrics" as view_technical_metrics
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB / Sistema" as BaseDatos <<sql>>

 view_technical_metrics -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_technical_metrics : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-07/diagramas-uml`
