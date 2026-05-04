.. meta::
 :artefacto: AT_UC_PERM_08_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_08_domain:

=========================================================
UC_PERM_08 — Generar Menu Dinamico: Domain Model
=========================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`.

.. uml::
 :caption: UC_PERM_08 — Domain Model

 @startuml

 left to right direction

 class MenuItem
 class UserFunction
 class User

 MenuItem --> UserFunction
 UserFunction --> User

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`
