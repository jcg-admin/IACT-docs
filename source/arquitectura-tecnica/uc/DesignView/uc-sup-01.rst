.. meta::
 :artefacto: AT_UC_SUP_01_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_01_design:

====================================================
UC_SUP_01 — Monitorear Llamada: Design View
====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_SUP_01 tecnicamente.

.. uml::
 :caption: UC_SUP_01 — Design View (secuencia)

 @startuml

 actor "monitor_live_calls" as monitor_live_calls
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 monitor_live_calls -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> monitor_live_calls : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/supervision/uc-sup-01/diagramas-uml`
