.. meta::
 :artefacto: AT_IMPL_SEQ_ALERTS
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_alerts:

============================================================
Implementation View — MOD_Alerts: Patron de Interaccion
============================================================

Secuencia para "evaluar reglas de alerta y emitir notificacion"
(UC_ALR_05 trigger). El evaluator es ejecutado por scheduler,
no por request.

.. uml::
 :caption: MOD_Alerts impl seq — evaluator → AlertService → notify.

 @startuml

 participant "EvaluatorJob\n(APScheduler tick 60s)" as Job <<scheduler>>
 participant "AlertService" as Svc <<service>>
 participant "AlertRuleRepository" as RuleRepo <<repository>>
 participant "MetricSource\n(prometheus / DB)" as Metrics <<gateway>>
 participant "AlertRepository" as ARepo <<repository>>
 participant "NotificationGateway" as Notify <<gateway>>
 database PostgreSQL

 Job -> Svc : evaluate_all()
 activate Svc

 Svc -> RuleRepo : enabled_rules()
 activate RuleRepo
 RuleRepo -> PostgreSQL : SELECT * FROM alert_rule\nWHERE enabled = TRUE
 PostgreSQL --> RuleRepo
 RuleRepo --> Svc : list[AlertRule]
 deactivate RuleRepo

 loop por cada rule
   Svc -> Metrics : current_value(rule.metric)
   Metrics --> Svc : value
   alt threshold exceeded
     Svc -> ARepo : get_active(rule.id)
     ARepo --> Svc : Alert | None
     alt sin alert activa (no duplicada)
       Svc -> ARepo : create(rule.id, value)
       ARepo -> PostgreSQL : INSERT INTO alert ...
       Svc -> Notify : send(rule.subscribers, alert)
       Notify --> Svc : delivered_count
     end
   else back to normal
     Svc -> ARepo : auto_resolve(rule.id)
     ARepo -> PostgreSQL : UPDATE alert SET status='resolved' ...
   end
 end

 Svc --> Job : EvaluationResult
 deactivate Svc

 @enduml

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Capa
   - Archivo
 * - View (CRUD reglas)
   - ``apps/alerts/api/views.py: AlertRuleView, AlertView,
     SubscriptionView``
 * - Evaluator job
   - ``apps/alerts/jobs/evaluator.py: EvaluatorJob``
 * - Service
   - ``apps/alerts/services/alert_service.py``
 * - Repositories
   - ``apps/alerts/repositories/alert_rule_repo.py``
     ``apps/alerts/repositories/alert_repo.py``
     ``apps/alerts/repositories/subscription_repo.py``
 * - Notification
   - ``apps/alerts/gateways/notification_gateway.py``
     (email + in-app)

Invariantes de implementacion
==============================

- **I-IMPL-ALR-01:** la deteccion de duplicados se hace
  en ``ARepo.get_active`` ANTES del INSERT — evita crear
  ``Alert`` duplicadas para una rule en estado
  ``raised|ack|silenced``.
- **I-IMPL-ALR-02:** ``Notify.send`` es **best-effort** —
  un fallo en notificacion NO revierte el INSERT del Alert.
  El operador siempre puede ver el alert en la consola.

----

.. seealso::

 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`evaluator-scheduler-binding` — patron de scheduling
   del evaluator.
 - :doc:`/arquitectura-tecnica/design-view/alerts/alert-evaluation-flow` —
   flujo en DesignView.
 - :doc:`/arquitectura-tecnica/design-view/alerts/alert-event-lifecycle` —
   FSM del Alert.
