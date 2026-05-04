.. meta::
 :artefacto: AT_UC_CLI_03_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_03_design:

=================================================
UC_CLI_03 — Esperar en Cola: Design View
=================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_CLI_03 tecnicamente.

.. uml::
 :caption: UC_CLI_03 — Design View (secuencia)

 @startuml

 actor "CallerExterno" as CallerExterno
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 CallerExterno -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> CallerExterno : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/caller/uc-cli-03/diagramas-uml`
