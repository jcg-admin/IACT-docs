.. meta::
 :artefacto: AT_UC_ALR_04_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_alr_04_ver_historial_de_alertas:

==============================
UC_ALR_04 — Ver Historial Alertas
==============================

Analiza tendencias: alertas mas frecuentes, tiempo medio de ack,
tiempo medio de resolve. ``view_alert_history`` con period max 1 ano
online (mas antiguo via export). Insumo para mejorar reglas (UC_ALR_01)
y SLAs.

.. uml::
 :caption: UC_ALR_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_alert_history" as view_alert_history
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AlertRepo" as AlertRepo <<sistema>>
 actor "TimingCalculator" as TimingCalculator <<sistema>>
 actor "CursorEncoder" as CursorEncoder <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_04\nVer Historial de Alertas" as UC_ALR_04
   usecase "Verificar\nview_alert_history" as VERIFICAR_AGR
   usecase "Validar period\n(<=1 ano online)" as VALIDAR_PERIOD
   usecase "Filtrar por rule_id\n+ severity" as FILTRAR
   usecase "Calcular tiempo\nmedio de ack" as METRICA_ACK
   usecase "Calcular tiempo\nmedio de resolve" as METRICA_RESOLVE
   usecase "Cursor pagination" as PAGINACION
 }

 view_alert_history --> UC_ALR_04

 UC_ALR_04 ..> VERIFICAR_AGR : <<include>>
 UC_ALR_04 ..> VALIDAR_PERIOD : <<include>>
 UC_ALR_04 ..> FILTRAR : <<include>>
 UC_ALR_04 ..> METRICA_ACK : <<include>>
 UC_ALR_04 ..> METRICA_RESOLVE : <<include>>
 UC_ALR_04 ..> PAGINACION : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 FILTRAR --> AlertRepo
 METRICA_ACK --> TimingCalculator
 METRICA_RESOLVE --> TimingCalculator
 METRICA_ACK --> AlertRepo
 PAGINACION --> CursorEncoder

 note bottom of VALIDAR_PERIOD
   Hasta 1 ano online. Mas antiguo
   requiere export con archive.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert` —
   timestamps de transiciones.
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo` —
   filter por period + rule_id + severity.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   reglas referenciadas.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   tiempos medios.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   pagination.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/alerts/uc-alr-04/index` —
   spec textual.
