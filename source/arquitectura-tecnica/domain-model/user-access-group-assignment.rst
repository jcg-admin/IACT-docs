.. meta::
 :artefacto: AT_DM_CLASS_USER_ACCESS_GROUP_ASSIGNMENT
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_user_access_group_assignment:

==========================
UserAccessGroupAssignment
==========================

Tabla intermedia (entidad asociativa) que materializa la
relacion M:N entre ``User`` y ``AccessGroup`` en el catalogo
RBAC v5.6.x. Es el lado complementario de
``FunctionGroupMembership`` (User -> AGR vs AGR -> Function).

Cada asignacion representa que a un usuario se le
**concedio** un AccessGroup particular, otorgando todas las
``Function`` agrupadas. La separacion en entidad explicita
permite:

1. Auditar el origen de una capability efectiva
   (``granted_at``, ``granted_by``).
2. Soportar asignaciones temporales (``expires_at``).
3. Implementar revocacion sin perder historial
   (``state = REVOKED``).

.. uml::
 :caption: UserAccessGroupAssignment — relacion M:N
           explicita entre User y AccessGroup.

 @startuml

 class UserAccessGroupAssignment {
   + id : UUID
   + user : User
   + group : AccessGroup
   + state : AssignmentState
   + granted_at : DateTime
   + granted_by : User
   + expires_at : DateTime
 }

 enum AssignmentState {
   ACTIVE
   REVOKED
   EXPIRED
 }

 class User
 class AccessGroup

 User "1" --> "*" UserAccessGroupAssignment : has
 UserAccessGroupAssignment "*" --> "1" AccessGroup : grants
 UserAccessGroupAssignment --> AssignmentState

 @enduml

Atributos
=========

- ``id : UUID`` — identificador unico.
- ``user : User`` — usuario asignado.
- ``group : AccessGroup`` — AccessGroup concedido.
- ``state : AssignmentState`` — ACTIVE / REVOKED / EXPIRED.
- ``granted_at : DateTime`` — timestamp de concesion.
- ``granted_by : User`` — usuario que la concedio (codename
  ``manage_users`` o ``manage_access_groups``).
- ``expires_at : DateTime`` — opcional, fecha de expiracion
  automatica.

Restricciones aplicables
========================

- **CNST-030** — separacion de funciones (SoD) — al asignar
  un AGR, ``RuleValidator`` verifica que no genere conflicto
  con AGRs ya asignadas al usuario.
- **CNST-032** — el menu dinamico del usuario se construye
  recorriendo estas asignaciones via
  ``UserCapabilityResolver``.
- **BR-009** — la revocacion es logica
  (``state = REVOKED``); no se elimina el registro.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
  asignacion creada por UC_ACC_04.
- :doc:`/requisitos/casos-uso/admin/uc-adm-01/index` —
  validacion SoD al asignar.

Relaciones
==========

- ``User`` "1" --> "*" ``UserAccessGroupAssignment``.
- ``UserAccessGroupAssignment`` "*" --> "1" ``AccessGroup``.
- Es leida por ``UserCapabilityResolver`` para resolver el
  set efectivo de AGRs activas de un usuario.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user`
 - :doc:`/arquitectura-tecnica/domain-model/access-group`
 - :doc:`/arquitectura-tecnica/domain-model/function-group-membership`
 - :doc:`/arquitectura-tecnica/domain-model/user-capability-resolver`
 - :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones`
 - :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`
