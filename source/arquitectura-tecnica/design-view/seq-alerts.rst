.. meta::
 :artefacto: AT_DESIGN_MOD_ALERTS
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_alerts:

===============================================
Design View — MOD_Alerts: Gestion de Alertas
===============================================

Patron de interaccion del modulo de alertas. Muestra el flujo de
reconocimiento de ``Alert``: transicion de estado ACTIVE →
ACKNOWLEDGED (D-02: closed-loop), con registro de
``AuditEvent(ALERT_ACKNOWLEDGED)`` por CNST-025.

.. uml::
 :caption: Design View MOD_Alerts — reconocimiento de alerta con auditoria.

 @startuml

 actor AGR_SUPERVISOR

 participant InterfazMonitor   <<frontend>>
 participant ServicioAlertas   <<api>>
 participant RepositorioAlert  <<repository>>
 database    AlmacenDatos      <<postgresql>>

 AGR_SUPERVISOR -> InterfazMonitor : GET /alerts?state=ACTIVE
 activate InterfazMonitor

 InterfazMonitor -> ServicioAlertas : listarAlertas(state:AlertState.ACTIVE)
 activate ServicioAlertas
 ServicioAlertas -> AlmacenDatos : SELECT alerts WHERE state=ACTIVE
 AlmacenDatos --> ServicioAlertas : List<Alert>
 ServicioAlertas --> InterfazMonitor : alertas activas
 deactivate ServicioAlertas

 InterfazMonitor --> AGR_SUPERVISOR : lista de alertas
 deactivate InterfazMonitor

 AGR_SUPERVISOR -> InterfazMonitor : POST /alerts/{alert_id}/acknowledge
 activate InterfazMonitor

 InterfazMonitor -> ServicioAlertas : reconocerAlerta(alert_id, user_id)
 activate ServicioAlertas

 ServicioAlertas -> RepositorioAlert : buscar(alert_id)
 activate RepositorioAlert
 RepositorioAlert -> AlmacenDatos : SELECT alerts WHERE alert_id=?
 AlmacenDatos --> RepositorioAlert : Alert{state:ACTIVE}
 RepositorioAlert --> ServicioAlertas : Alert
 deactivate RepositorioAlert

 note right of ServicioAlertas
   D-02: closed-loop alerts.
   ACTIVE → ACKNOWLEDGED
 end note

 ServicioAlertas -> RepositorioAlert : actualizar(Alert{\n  state:AlertState.ACKNOWLEDGED,\n  acknowledged_by:user_id,\n  acknowledged_at\n})
 activate RepositorioAlert
 RepositorioAlert -> AlmacenDatos : UPDATE alerts SET state=ACKNOWLEDGED
 AlmacenDatos --> RepositorioAlert : OK
 RepositorioAlert --> ServicioAlertas : Alert actualizada
 deactivate RepositorioAlert

 ServicioAlertas -> AlmacenDatos : INSERT audit_events\n{event_type:ALERT_ACKNOWLEDGED,\n actor_user_id, details:{alert_id}}\n<<CNST-025>>
 AlmacenDatos --> ServicioAlertas : AuditEvent registrado

 ServicioAlertas --> InterfazMonitor : 200 OK
 deactivate ServicioAlertas
 InterfazMonitor --> AGR_SUPERVISOR : confirmacion
 deactivate InterfazMonitor

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/alert`
 :doc:`/arquitectura-tecnica/domain-model/threshold`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
