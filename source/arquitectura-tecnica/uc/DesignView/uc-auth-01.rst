.. meta::
 :artefacto: AT_UC_AUTH_01_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_01_design:

=================================================
UC_AUTH_01 — Iniciar Sesion: Design View
=================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUTH_01 tecnicamente.

.. uml::
 :caption: UC_AUTH_01 — Design View (secuencia)

 @startuml

 actor "Usuario" as Usuario
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 Usuario -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> Usuario : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-01/diagramas-uml`
