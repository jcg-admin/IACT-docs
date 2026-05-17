8.4 Diagrama de estados — Session
=================================

.. uml::
 :caption: Estados de la entidad Session relevantes a UC_AUTH_02

 @startuml

 [*] --> ACTIVE : UC_AUTH_01 exito

 ACTIVE --> CLOSED : UC_AUTH_02\n(USER_LOGOUT)
 ACTIVE --> CLOSED : CNST-005\n(TIMEOUT)
 ACTIVE --> CLOSED : CNST-004\n(SUPERSEDED) por\nUC_AUTH_01 nuevo
 ACTIVE --> CLOSED : UC_AUTH_05\n(ADMIN_REVOKED)

 CLOSED --> [*]

 note right of CLOSED
   close_reason indica la causa.
   Idempotente: re-entrar a CLOSED
   no cambia close_reason.
 end note

 @enduml
