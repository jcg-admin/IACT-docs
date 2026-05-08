.. meta::
 :artefacto: AT_UC_ACC_01
 :tipo: Diagrama Arquitectonico — Caso de Uso
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_acc_01:

================================
UC_ACC_01 — Asignar Funciones
================================

Diagrama de caso de uso (uml-07) para ``UC_ACC_01 Asignar
Funciones``. El ``AccessAdmin`` asigna funciones RBAC
atómicas (no AGRs) a un ``TargetUser``, con validación de
SoD (BR-007 + CNST-005) y emisión obligatoria de
``AuditEvent`` (P-09 audit-or-abort).

.. uml::
 :caption: UC_ACC_01 Asignar Funciones — pipeline de
           validaciones (`<<include>>`) + notificación
           opcional (`<<extend>>`).

 @startuml
 left to right direction

 actor AccessAdmin
 actor TargetUser
 actor Auditor

 rectangle "MOD_Access" {
   usecase "UC_ACC_01\nAsignar Funciones" as UC_ACC_01
   usecase "Validar User\ndestino" as VALIDATE_USER
   usecase "Validar funciones\n(existen + activas)" as VALIDATE_FUNCS
   usecase "Filtrar idempotente" as IDEMPOTENT
   usecase "Validar SoD\n(BR-007, CNST-005)" as VALIDATE_SOD
   usecase "Registrar N\nAssignments" as PERSIST
   usecase "Invalidar cache\nde permisos" as INVALIDATE_CACHE
   usecase "Notificar via\nInternalMailbox" as NOTIFY
   usecase "Emitir AuditEvent\nFUNCTIONS_ASSIGNED" as AUDIT
 }

 AccessAdmin --> UC_ACC_01

 UC_ACC_01 ..> VALIDATE_USER    : <<include>>
 UC_ACC_01 ..> VALIDATE_FUNCS   : <<include>>
 UC_ACC_01 ..> IDEMPOTENT       : <<include>>
 UC_ACC_01 ..> VALIDATE_SOD     : <<include>>
 UC_ACC_01 ..> PERSIST          : <<include>>
 UC_ACC_01 ..> INVALIDATE_CACHE : <<include>>
 UC_ACC_01 ..> AUDIT            : <<include>>

 NOTIFY    ..> UC_ACC_01        : <<extend>>

 NOTIFY    --> TargetUser
 AUDIT     --> Auditor

 note bottom of VALIDATE_SOD
   BR-007 + CNST-005:
   all-or-nothing — una violación
   SoD bloquea toda la asignación.
 end note

 note bottom of VALIDATE_FUNCS
   P-15 RBAC granular:
   función canónica (codename),
   no AGR.
 end note

 note bottom of AUDIT
   P-09 audit-or-abort:
   sin AuditEvent no hay COMMIT.
 end note

 @enduml

Lectura del diagrama
====================

- ``AccessAdmin`` (AGR-007 ``permission_admin_group``)
  inicia la asignación.
- El UC incluye **7 sub-UCs** que detallan el pipeline:
  validar User destino, validar funciones, filtrar
  idempotente (ya asignadas), validar SoD, persistir,
  invalidar cache, auditar.
- ``Notificar via InternalMailbox`` ``<<extend>>`` el UC
  base — es **opcional** (algunas asignaciones críticas
  no requieren notificación user-facing).
- **Beneficiarios:**

  - ``TargetUser`` recibe la notificación.
  - ``Auditor`` (AGR-008) consume el ``AuditEvent``
    generado.

Especificación textual
======================

- :doc:`/requisitos/casos-uso/access/uc-acc-01/index`
  — spec completa de 12 partes.

Implementación en domain-model
==============================

- :doc:`/arquitectura-tecnica/domain-model/assignment`
  — entidad creada en ``Registrar N Assignments``.
- :doc:`/arquitectura-tecnica/domain-model/assignment-repo`
  — repositorio de persistencia.
- :doc:`/arquitectura-tecnica/domain-model/separation-rule`
  — reglas SoD evaluadas por ``Validar SoD``.
- :doc:`/arquitectura-tecnica/domain-model/permission-cache`
  — cache invalidado tras commit.
- :doc:`/arquitectura-tecnica/domain-model/audit-service`
  / :doc:`/arquitectura-tecnica/domain-model/audit-event`
  — emisión P-09.
- :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`
  — destino de la notificación.

.. seealso::

 :doc:`/arquitectura-tecnica/use-case-view/access/index`
  — vista módulo MOD_Access.
 :doc:`/arquitectura-tecnica/use-case-view/mapa-funciones-rbac`
  — modelo plano RBAC.
