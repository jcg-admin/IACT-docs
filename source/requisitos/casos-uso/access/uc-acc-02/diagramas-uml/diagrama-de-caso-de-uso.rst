8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "revoke_functions" as INVOKER
 actor "User destino" as TARGET <<receptor>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_02\nRevocar Funciones" as UC02
   usecase "Validar P-11\nanti-self-revoke" as P11
   usecase "Localizar Assignments\nACTIVE matching" as LOC
   usecase "Calcular post-revoke\n+ warnings" as CALC
   usecase "actualizar → REVOKED" as UPD
   usecase "Invalidar cache" as CACHE
   usecase "Notificar via\nInternalMailbox" as NOT
   usecase "AuditEvent\nFUNCTIONS_REVOKED" as EMI
 }

 INVOKER --> UC02
 UC02 ..> P11 : <<include>>
 UC02 ..> LOC : <<include>>
 UC02 ..> CALC : <<include>>
 UC02 ..> UPD : <<include>>
 UC02 ..> CACHE : <<include>>
 UC02 ..> NOT : <<extend>>
 UC02 ..> EMI : <<include>>
 NOT --> TARGET
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of UPD
   BR-009: soft-delete via state,
   no DELETE fisico
 end note
 note bottom of CALC
   warnings: no_functions,
   critical_revoked, last_holder
 end note

 @enduml

