8.4 Diagrama de estados — Session (foco UC_AUTH_05)
===================================================

.. uml::
 :caption: Estados Session relevantes a UC_AUTH_05

 @startuml

 [*] --> ACTIVE : UC_AUTH_01

 ACTIVE --> CLOSED : UC_AUTH_05 (ADMIN_REVOKED)
 ACTIVE --> CLOSED : UC_AUTH_02 (USER_LOGOUT)
 ACTIVE --> CLOSED : CNST-004 (SUPERSEDED)
 ACTIVE --> CLOSED : CNST-005 (TIMEOUT)
 ACTIVE --> CLOSED : UC_AUTH_03 (PASSWORD_RESET)

 note right of CLOSED
   close_reason indica origen
   UC_AUTH_05 solo origina ADMIN_REVOKED
 end note

 CLOSED --> [*]

 @enduml
