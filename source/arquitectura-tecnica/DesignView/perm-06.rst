.. meta::
 :artefacto: AT_UC_PERM_06_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_06_design:

============================================================
UC_PERM_06 — Asignar Funciones a Grupo: Design View
============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PERM_06 tecnicamente.

.. uml::
 :caption: UC_PERM_06 — Design View (secuencia)

 @startuml

 actor "assign_functions_to_group" as assign_functions_to_group
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 assign_functions_to_group -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> assign_functions_to_group : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-06/diagramas-uml`
