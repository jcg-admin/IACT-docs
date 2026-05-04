.. meta::
 :artefacto: AT_UC_SUP_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_02_design:

=====================================================
UC_SUP_02 — Barge-in en Llamada: Design View
=====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_SUP_02 tecnicamente.

.. uml::
 :caption: UC_SUP_02 — Design View (secuencia)

 @startuml

 actor "barge_in_calls" as barge_in_calls
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 barge_in_calls -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> barge_in_calls : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/supervision/uc-sup-02/diagramas-uml`
