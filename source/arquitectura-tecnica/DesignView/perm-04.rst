.. meta::
 :artefacto: AT_UC_PERM_04_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_04_design:

==============================================================
UC_PERM_04 — Revocar Permiso Excepcional: Design View
==============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PERM_04 tecnicamente.

.. uml::
 :caption: UC_PERM_04 — Design View (secuencia)

 @startuml

 actor "revoke_exceptional_permission" as revoke_exceptional_permission
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 revoke_exceptional_permission -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> revoke_exceptional_permission : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-04/diagramas-uml`
