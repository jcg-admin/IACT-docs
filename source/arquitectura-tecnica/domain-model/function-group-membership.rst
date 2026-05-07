.. meta::
 :artefacto: AT_DM_CLASS_FUNCTION_GROUP_MEMBERSHIP
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

.. _dm_class_function_group_membership:

========================
FunctionGroupMembership
========================

Tabla intermedia (entidad asociativa) que materializa la
relacion M:N entre ``AccessGroup`` y ``Function`` en el
catalogo RBAC v5.6.x. Cada membresia representa que un
``AccessGroup`` (AGR) **contiene** una ``Function``
particular como parte de su definicion de capabilities.

Esta entidad NO existe como tabla intermedia anonima — es
explicita, lo que permite:

1. Auditar cuando una function fue agregada o removida de
   un AGR (``added_at``).
2. Distinguir membresias temporales de permanentes (campo
   ``expires_at`` opcional, futuro).
3. Soportar consultas inversas (``Function`` -> AGRs que
   la incluyen) sin recorrer todas las AGRs.

.. uml::
 :caption: FunctionGroupMembership — relacion M:N
           explicita entre AccessGroup y Function.

 @startuml

 class FunctionGroupMembership {
   + id : UUID
   + group : AccessGroup
   + function : Function
   + added_at : DateTime
   + added_by : User
 }

 class AccessGroup
 class Function

 AccessGroup "1" --> "*" FunctionGroupMembership : contains
 FunctionGroupMembership "*" --> "1" Function : grants

 @enduml

Atributos
=========

- ``id : UUID`` — identificador unico.
- ``group : AccessGroup`` — el AccessGroup contenedor.
- ``function : Function`` — la Function granted.
- ``added_at : DateTime`` — timestamp de creacion.
- ``added_by : User`` — usuario que la agrego (codename
  ``manage_access_groups``).

Restricciones aplicables
========================

- **CNST-032** — el menu dinamico se construye recorriendo
  estas membresias para resolver capabilities efectivas
  por usuario.
- **BR-009** — la baja es logica via ``state`` de
  ``AccessGroup`` (no por delete fisico de la membresia).

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
  AGR como agregacion de functions.
- :doc:`/requisitos/casos-uso/admin/uc-adm-02/index` —
  modificacion del catalogo de AGRs.

Relaciones
==========

- ``AccessGroup`` "1" --> "*" ``FunctionGroupMembership``.
- ``FunctionGroupMembership`` "*" --> "1" ``Function``.
- Es leida por ``UserCapabilityResolver`` para resolver
  el set de capabilities efectivas de un usuario.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/access-group`
 - :doc:`/arquitectura-tecnica/domain-model/function`
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function`
 - :doc:`/arquitectura-tecnica/domain-model/user-capability-resolver`
 - :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`
