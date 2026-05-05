.. meta::
 :artefacto: AT_UC_MOD_ALERTS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_alerts:

====================================================
MOD_Alerts — Alertas y Notificaciones: UC por Modulo
====================================================

Configuración de umbrales críticos, recepción y reconocimiento
de alertas del sistema IVR (BR-016: tasa de abandono > 30%).
Las alertas se generan automáticamente por el motor de
alertas y por el pipeline.

.. uml::
 :caption: MOD_Alerts — Operator consume; Supervisor configura
           y reconoce; AlertEngine es actor sistema.

 @startuml
 left to right direction

 actor Operator
 actor Supervisor
 actor "AlertEngine\n<<system>>" as AlertEngine

 Operator <|-- Supervisor

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar Umbrales\nde Alertas" as AL01   usecase "UC_ALR_02\nVer Alertas Activas\n.. extension points ..\nReconocer / Notificacion automatica" as AL02
   usecase "UC_ALR_03\nReconocer Alerta" as AL03
   usecase "UC_ALR_04\nVer Historial\nde Alertas" as AL04
   usecase "UC_ALR_05\nNotificacion\nAutomatica" as AL05
   usecase "Generar Alerta\n(automatico)" as GEN_ALERTA
 }

 Operator   --> AL02
 Operator   --> AL04
 Supervisor --> AL01
 Supervisor --> AL03
 AlertEngine --> AL05
 AlertEngine --> GEN_ALERTA

 AL03 ..> AL02 : <<extend>>
 AL02 ..> AL05 : <<extend>>
 AL01 ..> GEN_ALERTA : <<include>>

 note right of MOD_Alerts
   Codenames RBAC:
     Operator (AGR-001) → view_alerts,
       view_alert_history
     Supervisor (AGR-005 alert_manager) →
       configure_team_alerts, acknowledge_alert,
       pause_alerts, delete_alerts
     AlertEngine: actor sistema (interno) que
       evalúa reglas y emite UC_ALR_05.
 end note

 @enduml

Lectura del diagrama
====================

- ``Operator`` consume alertas activas e historial.
- ``Supervisor`` (rol especializado) hereda esas
  capacidades y agrega configuración y reconocimiento.
- ``AlertEngine`` es un **actor sistema** (no humano)
  que ejecuta ``UC_ALR_05`` en ciclo continuo
  evaluando reglas configuradas por
  ``UC_ALR_01``.
- ``UC_ALR_02`` ``<<extend>>`` ``UC_ALR_03``: tras ver
  una alerta el supervisor puede reconocerla.

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/alert` — Alert entity.
- :doc:`/arquitectura-tecnica/domain-model/alert-rule` — AlertRule (UC_ALR_01).
- :doc:`/arquitectura-tecnica/domain-model/alert-repo` — AlertRepo.
- :doc:`/arquitectura-tecnica/domain-model/alert-hook` — AlertHook (notificación).
- :doc:`/arquitectura-tecnica/domain-model/rule-validator` — RuleValidator.
- :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` — EvaluatorReloader.
- :doc:`/arquitectura-tecnica/domain-model/timing-calculator` — TimingCalculator.
- :doc:`/arquitectura-tecnica/domain-model/threshold` — Threshold.
- :doc:`/arquitectura-tecnica/domain-model/subscription` — Subscription.

Casos de uso del módulo
=========================

Cada UC tiene su especificación textual completa y su diagrama
individual (con `<<include>>` y `<<extend>>` per uml-07) en
``source/requisitos/casos-uso/``:

.. list-table::
 :header-rows: 1
 :widths: 20 50 30

 * - UC
   - Nombre
   - Diagrama
 * - :doc:`UC_ALR_01 </requisitos/casos-uso/alerts/uc-alr-01/index>`
   - Configurar Umbrales de Alertas
   - :doc:`Diagrama </requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_ALR_02 </requisitos/casos-uso/alerts/uc-alr-02/index>`
   - Ver Alertas Activas
   - :doc:`Diagrama </requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_ALR_03 </requisitos/casos-uso/alerts/uc-alr-03/index>`
   - Reconocer Alerta
   - :doc:`Diagrama </requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_ALR_04 </requisitos/casos-uso/alerts/uc-alr-04/index>`
   - Ver Historial de Alertas
   - :doc:`Diagrama </requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_ALR_05 </requisitos/casos-uso/alerts/uc-alr-05/index>`
   - Gestionar Suscripciones
   - :doc:`Diagrama </requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-caso-de-uso>`

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
