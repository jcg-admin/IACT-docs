.. meta::
 :artefacto: AT_UC_PERM_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_02_design:

==========================================================
UC_PERM_02 — Revocar Grupo a Usuario: Design View
==========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PERM_02 tecnicamente.

.. uml::
 :caption: UC_PERM_02 — Design View (secuencia)

 @startuml

 actor "revoke_function_group" as revoke_function_group
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 revoke_function_group -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> revoke_function_group : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-02/diagramas-uml`
