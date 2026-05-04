.. meta::
 :artefacto: AT_UC_ACC_05_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_05_domain:

=======================================================
UC_ACC_05 — Gestionar Reglas SoD: Domain Model
=======================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/access/uc-acc-05/index`.

.. uml::
 :caption: UC_ACC_05 — Domain Model

 @startuml

 left to right direction

 class SodRule
 class Function
 class AuditEvent

 SodRule --> Function
 Function --> AuditEvent

 @enduml


.. uml::
 :caption: UC_ACC_05 — Gestionar Reglas SoD — Estado de FuncionAsignada

 @startuml
 hide empty description

 [*] --> Pendiente : solicitar asignacion
 Pendiente --> Asignada : aprobar asignacion
 Asignada --> Activa : activar
 Activa --> Revocada : revocar funcion
 Pendiente --> [*] : rechazar solicitud
 Revocada --> [*] : eliminar registro

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/access/uc-acc-05/index`
