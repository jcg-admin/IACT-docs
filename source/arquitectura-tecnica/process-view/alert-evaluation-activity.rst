.. meta::
 :artefacto: AT_PROC_ALERT_EVALUATION_ACTIVITY
 :tipo: Diagrama Arquitectonico — Process View — Activity
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_proc_alert_evaluation_activity:

============================================================
Process View — Evaluacion de alertas: flujo de actividades
============================================================

Diagrama de actividades del evaluador de alertas —
complementa :doc:`alert-evaluation-concurrency` (vista de
secuencia de participantes) con la perspectiva del **flujo
de control**: filtrado de reglas habilitadas, evaluacion
de threshold, deduplicacion y notificacion.

.. uml::
 :caption: ProcessView alerts — flujo de actividades con decisiones y deduplicacion.

 @startuml

 start

 :Tick scheduler (60s)\nEvaluatorJob.run();

 :SELECT enabled_rules
 FROM alert_rule
 WHERE enabled = TRUE;

 if (¿hay reglas?) then (no)
   stop
 else (si)
 endif

 partition "Loop por cada rule" {
   :leer rule.metric;

   :MetricSource.current_value
   (con timeout 5s);

   if (¿timeout o error en metric?) then (si)
     :log warning
     (no se evalua esta rule);
     :continue;
   else (no)
   endif

   if (¿threshold superado?) then (si — disparo)
     :SELECT alert WHERE rule_id = ?
     AND status IN
     ('raised','acknowledged','silenced');

     if (¿hay Alert activa?) then (si)
       note right
         deduplicacion:
         no se crea Alert
         duplicada para
         rule ya activa.
       end note
       :continue;
     else (no)
       :INSERT alert
       (status='raised',
       valor_actual);

       fork
         :send notification
         (email + in-app);
       fork again
         :emit metric
         (alerts_raised_total);
       end fork
     endif
   else (no — back to normal)
     :SELECT alert WHERE rule_id = ?
     AND status IN
     ('raised','acknowledged');

     if (¿hay Alert activa?) then (si)
       :UPDATE alert
       SET status='resolved'
       (auto-resolve);
       :emit metric
       (alerts_auto_resolved);
     else (no)
       :continue;
     endif
   endif
 }

 :EvaluationResult
 (rules_evaluated, fired,
 auto_resolved, errors);

 stop

 @enduml

Decisiones modeladas
=====================

.. list-table::
 :widths: 28 72
 :header-rows: 1

 * - Decision
   - Detalle
 * - Filtro de reglas habilitadas
   - Solo reglas con ``enabled = TRUE`` se evaluan; las
     deshabilitadas via consola admin no consumen tiempo
     del scheduler.
 * - Timeout por metric
   - 5s. Si el ``MetricSource`` (Prometheus o BD) no
     responde, la rule se omite ese tick — NO bloquea las
     demas. Se reintenta en el siguiente tick (60s).
 * - Deduplicacion
   - Si ya existe ``Alert`` con
     ``status IN ('raised','acknowledged','silenced')``
     para esta rule, no se crea otra. Coherente con FSM
     en :doc:`/arquitectura-tecnica/design-view/alerts/alert-event-lifecycle`.
 * - Auto-resolve
   - Cuando el threshold vuelve a estar dentro de rango,
     las alertas en ``raised|acknowledged`` pasan a
     ``resolved`` automaticamente.
 * - Notificacion best-effort
   - Un fallo en ``send_notification`` no aborta el INSERT
     del Alert — el operador siempre puede ver el alert
     en consola.

----

.. seealso::

 - :doc:`alert-evaluation-concurrency` — secuencia de
   participantes (scheduler, workers).
 - :doc:`/arquitectura-tecnica/design-view/alerts/alert-evaluation-flow` —
   flujo de actividad equivalente en DesignView (logica
   de dominio, no de runtime).
 - :doc:`/arquitectura-tecnica/design-view/alerts/alert-event-lifecycle` —
   FSM del Alert.
 - :doc:`/arquitectura-tecnica/implementation-view/alerts/evaluator-scheduler-binding` —
   binding APScheduler.
