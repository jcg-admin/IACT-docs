.. meta::
 :artefacto: AT_UC_OPR_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_01_domain:

============================================================
UC_OPR_01 — Cambiar Estado del Agente: Domain Model
============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/operator/uc-opr-01/index`.

.. uml::
 :caption: UC_OPR_01 — Domain Model

 @startuml

 left to right direction

 class AgentSession
 class AgentState
 class AuditEvent

 AgentSession --> AgentState
 AgentState --> AuditEvent

 @enduml


.. uml::
 :caption: UC_OPR_01 — Cambiar Estado del Agente — Estado de AccionOperador

 @startuml
 hide empty description

 [*] --> Iniciada : operador ejecuta accion
 Iniciada --> Procesando : sistema valida RBAC
 Procesando --> Completada : accion exitosa
 Procesando --> Fallida : error / sin permiso
 Completada --> [*] : registrar en auditoria
 Fallida --> [*] : registrar error

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/operator/uc-opr-01/index`
