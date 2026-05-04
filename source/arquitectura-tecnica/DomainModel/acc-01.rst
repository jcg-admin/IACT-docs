.. meta::
 :artefacto: AT_UC_ACC_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_01_domain:

====================================================
UC_ACC_01 — Asignar Funciones: Domain Model
====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/access/uc-acc-01/index`.

.. uml::
 :caption: UC_ACC_01 — Domain Model

 @startuml

 left to right direction

 class UserFunction
 class User
 class Function

 UserFunction --> User
 User --> Function

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/access/uc-acc-01/index`
