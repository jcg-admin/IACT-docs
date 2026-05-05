8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ALR_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "acknowledge_alert" as INVOKER
 actor "AlertRepo" as AR <<sistema>>
 actor "Alert" as A <<sistema>>
 actor "AlertHook" as AH <<sistema>>
 actor "AuditService" as AS <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_03\nReconocer Alerta" as UC_ALR_03
   usecase "Validar Alert existe\n+ state=firing" as VALIDAR_ALERT
   usecase "Validar scope ⊆\nsegmentos del User" as VALIDAR_SCOPE
   usecase "Transicionar Alert\nstate=acknowledged" as TRANSICIONAR
   usecase "Registrar acknowledged_by\n+ acknowledged_at" as REGISTRAR
   usecase "Detener notificaciones\nde la regla" as STOP_NOT
   usecase "Emitir AuditEvent\nALERT_ACKNOWLEDGED\n(P-39)" as AUDIT
 }

 INVOKER --> UC_ALR_03
 UC_ALR_03 ..> VALIDAR_ALERT : <<include>>
 UC_ALR_03 ..> VALIDAR_SCOPE : <<include>>
 UC_ALR_03 ..> TRANSICIONAR : <<include>>
 UC_ALR_03 ..> REGISTRAR : <<include>>
 UC_ALR_03 ..> STOP_NOT : <<include>>
 UC_ALR_03 ..> AUDIT : <<include>>

 VALIDAR_ALERT --> AR
 TRANSICIONAR --> A
 REGISTRAR --> AR
 STOP_NOT --> AH
 AUDIT --> AS
 AS --> view_audit_log

 note bottom of VALIDAR_SCOPE
   CNST-008: User solo puede ack
   alertas de sus segmentos.
 end note

 note bottom of STOP_NOT
   Stop notifications hasta que la
   alerta cambie de estado de nuevo.
   Tracking de tiempo de respuesta.
 end note

 note bottom of AUDIT
   P-39 audit reforzado.
   CNST-008/009/013/025.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/alert` —
   entidad Alert (transita firing → acknowledged).
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo` —
   repositorio que persiste la transicion.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   regla origen (consultada para stop notifications).
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook` —
   detiene notificaciones de la regla.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent ALERT_ACKNOWLEDGED (P-39).
