.. meta::
 :artefacto: AT_UC_PIP_04_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_04_domain:

==================================================================
UC_PIP_04 — Solicitar Reintento de Pipeline: Domain Model
==================================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index`.

.. uml::
 :caption: UC_PIP_04 — Domain Model

 @startuml

 left to right direction

 class ETLEjecucion
 class DisparadorETL
 class AuditEvent

 ETLEjecucion --> DisparadorETL
 DisparadorETL --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index`
