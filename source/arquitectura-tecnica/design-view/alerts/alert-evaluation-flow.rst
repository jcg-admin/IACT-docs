.. meta::
 :artefacto: AT_DESIGN_ACT_ALERT_EVAL
 :tipo: Diagrama Arquitectonico — Design View — Activity
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :flujo: alert-evaluation
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_design_act_alert_evaluation:

============================================================
Design View — Flujo: Evaluacion de Alertas
============================================================

Flujo del evaluador de alertas que corre en intervalos
periodicos. Para cada AlertRule activa, evalua su threshold
contra la metrica actual y decide si disparar Alert + notificar.

Cubre los UCs UC_ALR_01..05 (definir, ver, ack, historial,
suscripciones).

.. uml::
 :caption: Flujo evaluador de alertas — rule -> threshold -> notify.

 @startuml

 start
 :Tick del scheduler (cada N segundos);
 :EvaluatorReloader.get_active_rules();
 :rules = List<AlertRule>;

 while (mas rules?) is (si)
   :rule = next();
   :metric_value = Metric.current(rule.metric_id);

   :threshold = rule.get_threshold();
   :Threshold.configure_check(metric_value);

   if (threshold exceeded?) then (si)
     if (Alert activo para esta rule?) then (si)
       :Skip — ya hay Alert pendiente;
     else (no)
       :Alert.raise(rule, value, severity);
       :AlertRepo.persist(alert);

       fork
         :Notificar via AlertHook(s);
       fork again
         :Emitir AuditEvent(type=alert_raised);
       end fork
     endif
   else (no)
     if (Alert activo para esta rule?) then (si)
       :Alert.auto_resolve();
       :AlertRepo.update(alert.state=resolved);
       :Emitir AuditEvent(type=alert_resolved);
     else (no)
     endif
   endif
 endwhile (no)

 stop

 @enduml

----

Notas de diseno
================

- **Idempotencia**: si ya hay Alert activo para una rule, no se
  crea otra (evita storm).
- **Auto-resolve**: cuando el threshold deja de excederse, las
  alertas activas se resuelven automaticamente.
- **Severity**: definida en Threshold (info, warning, critical).
- **Reload incremental**: EvaluatorReloader detecta cambios en
  AlertRules sin restart del evaluador.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/alerts/interaction-pattern`
 - :doc:`/arquitectura-tecnica/design-view/alerts/alert-event-lifecycle`
 - :doc:`/arquitectura-tecnica/use-case-view/alerts/uc-alr-02-ver-alertas-activas`
 - :doc:`/arquitectura-tecnica/domain-model/alert`
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule`
 - :doc:`/arquitectura-tecnica/domain-model/threshold`
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook`
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`
