.. meta::
 :artefacto: AT_UC_OPR_06_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_06_design:

======================================================
UC_OPR_06 — Ingresar Disposition: Design View
======================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_OPR_06 tecnicamente.

.. uml::
 :caption: UC_OPR_06 — Design View (secuencia)

 @startuml

 actor "enter_call_disposition" as enter_call_disposition
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 enter_call_disposition -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> enter_call_disposition : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-06/diagramas-uml`
