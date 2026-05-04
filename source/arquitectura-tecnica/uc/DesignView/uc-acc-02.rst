.. meta::
 :artefacto: AT_UC_ACC_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_02_design:

===================================================
UC_ACC_02 — Revocar Funciones: Design View
===================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ACC_02 tecnicamente.

.. uml::
 :caption: UC_ACC_02 — Design View (secuencia)

 @startuml

 actor "revoke_functions" as revoke_functions
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 revoke_functions -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> revoke_functions : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/access/uc-acc-02/diagramas-uml`
