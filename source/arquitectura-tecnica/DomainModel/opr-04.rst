.. meta::
 :artefacto: AT_UC_OPR_04_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_04_domain:

======================================================
UC_OPR_04 — Hold Unhold Llamada: Domain Model
======================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/operator/uc-opr-04/index`.

.. uml::
 :caption: UC_OPR_04 — Domain Model

 @startuml

 left to right direction

 class Call
 class AgentSession
 class Call

 Call --> AgentSession
 AgentSession --> Call

 @enduml


.. uml::
 :caption: UC_OPR_04 — Hold Unhold Llamada — Estado de AccionOperador

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
 :doc:`/requisitos/casos-uso/operator/uc-opr-04/index`
