8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ALR_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "acknowledge_alert" as INVOKER
 actor "AlertRepo" as REPO <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_03\nReconocer Alerta" as UC_ALR_03
   usecase "Validar Alert existe\n+ state=firing" as VALIDAR_ALERT
   usecase "Validar scope ⊆\nsegmentos del User" as VALIDAR_SCOPE
   usecase "Transicionar\nstate=acknowledged" as TRANSICIONAR
   usecase "Registrar acknowledged_by\n+ acknowledged_at" as REGISTRAR
   usecase "Detener notificaciones\nde la regla" as STOP_NOT
   usecase "AuditEvent\nALERT_ACKNOWLEDGED\n(P-39)" as AUDIT
 }

 INVOKER --> UC_ALR_03
 UC_ALR_03 ..> VALIDAR_ALERT : <<include>>
 UC_ALR_03 ..> VALIDAR_SCOPE : <<include>>
 UC_ALR_03 ..> TRANSICIONAR : <<include>>
 UC_ALR_03 ..> REGISTRAR : <<include>>
 UC_ALR_03 ..> STOP_NOT : <<include>>
 UC_ALR_03 ..> AUDIT : <<include>>

 TRANSICIONAR --> REPO
 REGISTRAR --> REPO
 Sistema --> AUDIT
 AUDIT --> view_audit_log

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
