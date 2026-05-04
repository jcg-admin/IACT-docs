.. meta::
 :artefacto: AT_UC_OPR_04_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_04_design:

=====================================================
UC_OPR_04 — Hold Unhold Llamada: Design View
=====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_OPR_04 tecnicamente.

.. uml::
 :caption: UC_OPR_04 — Design View (secuencia)

 @startuml

 actor "hold_calls" as hold_calls
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 hold_calls -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> hold_calls : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-04/diagramas-uml`
