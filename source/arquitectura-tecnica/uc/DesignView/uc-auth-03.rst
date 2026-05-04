.. meta::
 :artefacto: AT_UC_AUTH_03_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_03_design:

=======================================================
UC_AUTH_03 — Recuperar Contrasena: Design View
=======================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUTH_03 tecnicamente.

.. uml::
 :caption: UC_AUTH_03 — Design View (secuencia)

 @startuml

 actor "reset_password" as reset_password
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 reset_password -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> reset_password : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-03/diagramas-uml`
