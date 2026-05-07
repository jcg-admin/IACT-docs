.. meta::
 :artefacto: AT_DM_CLASS_SUBSCRIPTION_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_subscription_repo:

================
SubscriptionRepo
================

Repositorio de persistencia y consulta de instancias
``Subscription``. Una ``Subscription`` representa el interes
de un ``User`` en recibir notificaciones cuando una
``AlertRule`` dispara, restringido al ``SegmentScope`` del
usuario al momento de suscribirse.

Soporta operaciones de gestion del ciclo de vida (``create``,
``pause``, ``resume``, ``cancel``) y consultas tipicas para
el motor de notificaciones (``find_active_for_rule``,
``by_user``).

.. uml::
 :caption: SubscriptionRepo — gestion de Subscription
           con pausa por revocacion de scope.

 @startuml

 class SubscriptionRepo {
   - storage_backend : StorageBackend
   --
   + create(sub : Subscription) : Subscription
   + by_user(user_id : UUID) : List<Subscription>
   + by_id(sub_id : UUID) : Subscription
   + find_active_for_rule(rule_id : UUID) : List<Subscription>
   + pause(sub_id : UUID, reason : String) : Subscription
   + resume(sub_id : UUID) : Subscription
   + cancel(sub_id : UUID) : Subscription
 }

 class Subscription
 class SubscriptionFilters {
   + state : SubscriptionState
   + rule_id : UUID
 }

 SubscriptionRepo "1" ..> "0..*" Subscription : persists/queries
 SubscriptionRepo "1" ..> "0..*" SubscriptionFilters : queries with

 @enduml

Operaciones principales
=======================

- ``create(sub)`` — registra una nueva suscripcion.
- ``by_user(user_id)`` — todas las suscripciones del user.
- ``find_active_for_rule(rule_id)`` — todas las
  suscripciones ``ACTIVE`` para una regla; consumido por el
  motor de notificaciones cuando la regla dispara.
- ``pause(sub_id, reason)`` — suspende temporalmente. Es
  invocado por ``SegmentChangeListener`` cuando el scope
  del user pierde el segmento de la suscripcion.
- ``resume(sub_id)`` — reactiva una pausada (si scope
  vuelve a incluir el segmento).
- ``cancel(sub_id)`` — baja logica permanente (BR-009).

Restricciones aplicables
========================

- **BR-009** — ``cancel`` no elimina; cambia el ``state`` a
  ``CANCELLED``.
- **CNST-025** — operaciones de mutacion se auditan.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-05/index` —
  gestion del ciclo de vida de Subscription.

Relaciones
==========

- Maneja entidad ``Subscription``.
- Es invocado por ``SegmentChangeListener`` (pause/resume).
- Es consultado por el motor de notificaciones cuando
  una ``AlertRule`` dispara.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/subscription`
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule`
 - :doc:`/arquitectura-tecnica/domain-model/segment-scope`
 - :doc:`/requisitos/reglas-negocio/br-009-bajas-logicas`
