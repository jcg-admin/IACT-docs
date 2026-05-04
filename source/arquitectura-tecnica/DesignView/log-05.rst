.. meta::
 :artefacto: AT_UC_LOG_05_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_05_design:

=============================================================
UC_LOG_05 — Ver Logs de Infraestructura: Design View
=============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_LOG_05 tecnicamente.

.. uml::
 :caption: UC_LOG_05 — Design View (secuencia)

 @startuml

 actor "view_infrastructure_logs" as view_infrastructure_logs
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB / Sistema" as BaseDatos <<sql>>

 view_infrastructure_logs -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_infrastructure_logs : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-05/diagramas-uml`
