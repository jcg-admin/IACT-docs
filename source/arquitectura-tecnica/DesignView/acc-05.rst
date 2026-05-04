.. meta::
 :artefacto: AT_UC_ACC_05_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_05_design:

======================================================
UC_ACC_05 — Gestionar Reglas SoD: Design View
======================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ACC_05 tecnicamente.

.. uml::
 :caption: UC_ACC_05 — Design View (secuencia)

 @startuml

 actor "view_separation_rules" as view_separation_rules
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 view_separation_rules -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_separation_rules : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/access/uc-acc-05/diagramas-uml`
