.. meta::
 :artefacto: AT_UC_OPR_06_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_06_domain:

=======================================================
UC_OPR_06 — Ingresar Disposition: Domain Model
=======================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/operator/uc-opr-06/index`.

.. uml::
 :caption: UC_OPR_06 — Domain Model

 @startuml

 left to right direction

 class CallDisposition
 class Call
 class AuditEvent

 CallDisposition --> Call
 Call --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/operator/uc-opr-06/index`
