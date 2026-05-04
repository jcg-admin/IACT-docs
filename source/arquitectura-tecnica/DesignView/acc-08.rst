.. meta::
 :artefacto: AT_UC_ACC_08_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_08_design:

==================================================
UC_ACC_08 — Permiso Temporal: Design View
==================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ACC_08 tecnicamente.

.. uml::
 :caption: UC_ACC_08 — Design View (secuencia)

 @startuml

 actor "grant_exceptional_permission" as grant_exceptional_permission
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 grant_exceptional_permission -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> grant_exceptional_permission : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/access/uc-acc-08/diagramas-uml`
