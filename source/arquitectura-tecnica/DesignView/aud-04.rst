.. meta::
 :artefacto: AT_UC_AUD_04_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_04_design:

===============================================================
UC_AUD_04 — Generar Reporte de Compliance: Design View
===============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUD_04 tecnicamente.

.. uml::
 :caption: UC_AUD_04 — Design View (secuencia)

 @startuml

 actor "generate_compliance_report" as generate_compliance_report
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (audit_log)" as BaseDatos <<sql>>

 generate_compliance_report -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> generate_compliance_report : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/audit/uc-aud-04/diagramas-uml`
