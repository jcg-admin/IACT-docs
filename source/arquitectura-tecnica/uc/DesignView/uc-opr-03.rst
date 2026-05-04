.. meta::
 :artefacto: AT_UC_OPR_03_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_03_design:

===========================================================
UC_OPR_03 — Realizar Llamada Saliente: Design View
===========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_OPR_03 tecnicamente.

.. uml::
 :caption: UC_OPR_03 — Design View (secuencia)

 @startuml

 actor "make_outbound_calls" as make_outbound_calls
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 make_outbound_calls -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> make_outbound_calls : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-03/diagramas-uml`
