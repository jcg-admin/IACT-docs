.. meta::
 :artefacto: AT_UC_AUTH_05_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_05_design:

=====================================================
UC_AUTH_05 — Gestionar Sesiones: Design View
=====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUTH_05 tecnicamente.

.. uml::
 :caption: UC_AUTH_05 — Design View (secuencia)

 @startuml

 actor "view_own_sessions" as view_own_sessions
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 view_own_sessions -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_own_sessions : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-05/diagramas-uml`
