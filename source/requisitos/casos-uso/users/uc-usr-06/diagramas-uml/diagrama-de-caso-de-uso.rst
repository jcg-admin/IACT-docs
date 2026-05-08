.. _uc-usr-06-parte-08-diagrama-caso-de-uso:

8.1 Diagrama de caso de uso
============================

.. uml::

   @startuml

   left to right direction

   actor "unblock_users" as ADMIN
   actor "AuthorizationGuard" as GUARD
   actor "AuditService" as AUDIT

   rectangle "Sistema IACT — UC_USR_06" {
     usecase "Desbloquear Usuario" as UC
     usecase "Validar funcion\nunblock_users" as INC1 <<include>>
     usecase "Lookup AuditEvent\nde bloqueo previo" as INC2 <<include>>
     usecase "Emitir AuditEvent\nUSER_UNBLOCKED" as INC3 <<include>>
     usecase "Emitir warning si\nestado inconsistente" as EXT1 <<extend>>
   }

   ADMIN --> UC

   UC ..> INC1 : <<include>>
   UC ..> INC2 : <<include>>
   UC ..> INC3 : <<include>>
   UC <.. EXT1 : <<extend>>

   INC1 --> GUARD
   INC2 --> AUDIT
   INC3 --> AUDIT
   EXT1 --> AUDIT

   note right of UC
     Pre: User.state = BLOCKED
     Post: User.state = ACTIVE
     Inversa de UC_USR_05
     Tambien desbloquea ACCOUNT_LOCKED (BR-015)
   end note

   @enduml
