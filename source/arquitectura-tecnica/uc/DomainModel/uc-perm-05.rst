.. meta::
 :artefacto: AT_UC_PERM_05_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_05_domain:

===========================================================
UC_PERM_05 — Crear Grupo de Permisos: Domain Model
===========================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/permissions/uc-perm-05/index`.

.. uml::
 :caption: UC_PERM_05 — Domain Model

 @startuml

 left to right direction

 class AccessGroup
 class Function
 class AuditEvent

 AccessGroup --> Function
 Function --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-05/index`
