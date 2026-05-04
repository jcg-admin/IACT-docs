.. meta::
 :artefacto: AT_UC_LOG_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_02_design:

========================================================
UC_LOG_02 — Consultar Logs del ETL: Design View
========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_LOG_02 tecnicamente.

.. uml::
 :caption: UC_LOG_02 — Design View (secuencia)

 @startuml

 actor "view_etl_logs" as view_etl_logs
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB / Sistema" as BaseDatos <<sql>>

 view_etl_logs -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_etl_logs : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-02/diagramas-uml`
