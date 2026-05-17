.. meta::
 :artefacto: AT_UC_ALR_03_USECASE
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

.. _at_uc_alr_03_reconocer_alerta:

==============================
UC_ALR_03 — Reconocer Alerta
==============================

User indica que vio la alerta y se hace cargo. ``Alert.state`` transita
firing → acknowledged + ``acknowledged_by`` + ``acknowledged_at``.
Detiene notificaciones de la regla hasta proximo state change. P-39
audit reforzado.

.. uml::
 :caption: UC_ALR_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "acknowledge_alert" as acknowledge_alert
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "AlertRepo" as AlertRepo <<sistema>>
 actor "Alert" as Alert <<sistema>>
 actor "AlertHook" as AlertHook <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_03\nReconocer Alerta" as UC_ALR_03
   usecase "Verificar\nacknowledge_alert" as VERIFICAR_AGR
   usecase "Validar Alert existe\n+ state=firing" as VALIDAR_STATE
   usecase "Validar scope ⊆\nsegmentos del User" as VALIDAR_SCOPE
   usecase "Transicionar\nstate=acknowledged" as TRANSICIONAR
   usecase "Registrar acknowledged_by\n+ acknowledged_at" as REGISTRAR
   usecase "Detener notificaciones\nde la regla" as STOP_NOT
   usecase "Emitir AuditEvent\nALERT_ACKNOWLEDGED (P-39)" as AUDITAR
 }

 acknowledge_alert --> UC_ALR_03

 UC_ALR_03 ..> VERIFICAR_AGR : <<include>>
 UC_ALR_03 ..> VALIDAR_STATE : <<include>>
 UC_ALR_03 ..> VALIDAR_SCOPE : <<include>>
 UC_ALR_03 ..> TRANSICIONAR : <<include>>
 UC_ALR_03 ..> REGISTRAR : <<include>>
 UC_ALR_03 ..> STOP_NOT : <<include>>
 UC_ALR_03 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_STATE --> AlertRepo
 VALIDAR_SCOPE --> SegmentResolver
 TRANSICIONAR --> Alert
 REGISTRAR --> AlertRepo
 STOP_NOT --> AlertHook
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of STOP_NOT
   AlertHook detiene notificaciones
   de la regla hasta que la alerta
   cambie de estado de nuevo
   (firing → resolved).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert` —
   transita firing → acknowledged.
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo` —
   persiste transicion.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   regla origen.
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook` —
   detiene notificaciones.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   CNST-008.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor (P-39).
 - :doc:`/requisitos/casos-uso/alerts/uc-alr-03/index` —
   spec textual.
