.. meta::
 :artefacto: AT_DM_CLASS_SEGMENT_CHANGE_LISTENER
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

.. _dm_class_segment_change_listener:

======================
SegmentChangeListener
======================

Listener de eventos de cambio en el ``SegmentScope`` de un
usuario (alta/baja/modificacion de los segmentos visibles).
Su responsabilidad es **propagar** la consecuencia del
cambio a las suscripciones de alerta del usuario.

Cuando el ``SegmentScope`` pierde un segmento, las
``Subscription`` que dependian de ese segmento deben
**pausarse automaticamente** (no notificar mas) hasta que
el usuario las cancele explicitamente o el segmento vuelva
al scope.

.. uml::
 :caption: SegmentChangeListener — propagacion de cambios
           de scope a suscripciones de alerta.

 @startuml

 class SegmentChangeListener {
   - subscription_repo : SubscriptionRepo
   --
   + on_segment_change(event : SegmentChangeEvent) : void
   - resolve_affected_subscriptions(\
       user_id : UUID, \
       lost_segments : Set<UUID>) : List<Subscription>
 }

 class SegmentChangeEvent {
   + user_id : UUID
   + previous_scope : SegmentScope
   + new_scope : SegmentScope
   + change_type : ScopeChangeType
 }

 enum ScopeChangeType {
   ADDED
   REMOVED
   REPLACED
 }

 class Subscription
 class SubscriptionRepo

 SegmentChangeListener --> SubscriptionRepo : pauses on revoke
 SegmentChangeListener ..> SegmentChangeEvent : consumes
 SegmentChangeListener ..> Subscription : affects

 @enduml

Operaciones principales
=======================

- ``on_segment_change(event)`` — handler principal:

  1. Compara ``previous_scope`` vs ``new_scope`` para
     identificar segmentos perdidos.
  2. Resuelve suscripciones del usuario filtradas por esos
     segmentos.
  3. Invoca ``SubscriptionRepo.pause(sub_id, reason)`` para
     cada suscripcion afectada.
  4. (Opcional) ``resume`` cuando el cambio es ``ADDED``
     y hay suscripciones previamente pausadas por revoke
     del mismo segmento.

Restricciones aplicables
========================

- **CNST-018** — la propagacion mantiene la coherencia entre
  ``SegmentScope`` y suscripciones; nunca se notifica sobre
  segmentos no autorizados.
- **CNST-025** — los pause/resume automaticos se auditan con
  ``reason="SCOPE_CHANGE"``.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-05/index` —
  gestion de subscriptions, propagacion automatica.

Relaciones
==========

- Suscriptor a eventos de cambio de scope (publish/subscribe
  via ``InternalMailbox``).
- Modifica ``Subscription`` via ``SubscriptionRepo``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/segment-scope`
 - :doc:`/arquitectura-tecnica/domain-model/subscription-repo`
 - :doc:`/arquitectura-tecnica/domain-model/subscription`
