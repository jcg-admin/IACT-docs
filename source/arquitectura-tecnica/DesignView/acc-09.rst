.. meta::
 :artefacto: AT_UC_ACC_09_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_09_design:

===========================================================
UC_ACC_09 — Auditar Cambios de Acceso: Design View
===========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ACC_09 tecnicamente.

.. uml::
 :caption: UC_ACC_09 — Design View (secuencia)

 @startuml

 actor "view_audit_log" as view_audit_log
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

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

 :doc:`/requisitos/casos-uso/access/uc-acc-09/diagramas-uml`
