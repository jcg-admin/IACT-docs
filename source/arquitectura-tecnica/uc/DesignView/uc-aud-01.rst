.. meta::
 :artefacto: AT_UC_AUD_01_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_01_design:

=============================================================
UC_AUD_01 — Consultar Auditoria General: Design View
=============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUD_01 tecnicamente.

.. uml::
 :caption: UC_AUD_01 — Design View (secuencia)

 @startuml

 actor "view_audit_log" as view_audit_log
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (audit_log)" as BaseDatos <<sql>>

 view_audit_log -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_audit_log : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/audit/uc-aud-01/diagramas-uml`
