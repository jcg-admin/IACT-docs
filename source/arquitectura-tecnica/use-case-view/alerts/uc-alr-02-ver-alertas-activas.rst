.. meta::
 :artefacto: AT_UC_ALR_02_USECASE
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

.. _at_uc_alr_02_ver_alertas_activas:

============================================================
UC_ALR_02 — Ver Alertas Activas
============================================================

List de ``Alert`` en estado firing/acknowledged ordenadas por severity
+ recency. Auto-refresh 10s. CNST-008 isolation: solo alertas con
scope ⊆ segmentos del User. Read-only (sin meta-audit por invocacion).

.. uml::
 :caption: UC_ALR_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_alerts" as view_alerts
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "AlertRepo" as AlertRepo <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_02\nVer Alertas Activas\n.. extension points ..\nAutoRefresh" as UC_ALR_02
   usecase "Verificar\nview_alerts" as VERIFICAR_AGR
   usecase "Filtrar por scope\n⊆ segmentos del User" as FILTRAR_SCOPE
   usecase "Filtrar por estado\n(firing | acknowledged)" as FILTRAR_ESTADO
   usecase "Ordenar por severity\n+ recency" as ORDENAR
   usecase "Auto-refresh 10s" as REFRESH
 }

 view_alerts --> UC_ALR_02

 UC_ALR_02 ..> VERIFICAR_AGR : <<include>>
 UC_ALR_02 ..> FILTRAR_SCOPE : <<include>>
 UC_ALR_02 ..> FILTRAR_ESTADO : <<include>>
 UC_ALR_02 ..> ORDENAR : <<include>>
 REFRESH ..> UC_ALR_02 : <<extend>> (AutoRefresh)

 VERIFICAR_AGR --> AuthorizationGuard
 FILTRAR_SCOPE --> SegmentResolver
 FILTRAR_ESTADO --> AlertRepo

 note bottom of FILTRAR_SCOPE
   CNST-008 isolation: solo
   alertas cuyo scope ⊆
   segmentos del User.
 end note

 note bottom of REFRESH
   Auto-refresh 10s — mas
   frecuente que reportes
   por naturaleza operacional.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert` —
   instancia firing/acknowledged.
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   origen de la alerta.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   isolation CNST-008.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/alerts/uc-alr-02/index` —
   spec textual.
