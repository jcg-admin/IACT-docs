.. _uc-usr-05-parte-08-diagrama-caso-de-uso:

8.1 Diagrama de caso de uso
============================

.. uml::

   @startuml

   left to right direction

   actor "block_users" as ADMIN
   actor "AuthorizationGuard" as GUARD
   actor "AuditService" as AUDIT

   rectangle "Sistema IACT — UC_USR_05" {
     usecase "Bloquear Usuario" as UC
     usecase "Validar funcion\nblock_users" as INC1 <<include>>
     usecase "Cerrar sesiones\nactivas" as INC2 <<include>>
     usecase "Blacklistear\ntokens vivos" as INC3 <<include>>
     usecase "Emitir AuditEvent\nUSER_BLOCKED" as INC4 <<include>>
     usecase "Override razon\nsi bloqueo automatico\nprevio" as EXT1 <<extend>>
   }

   ADMIN --> UC

   UC ..> INC1 : <<include>>
   UC ..> INC2 : <<include>>
   UC ..> INC3 : <<include>>
   UC ..> INC4 : <<include>>
   UC <.. EXT1 : <<extend>>

   INC1 --> GUARD
   INC4 --> AUDIT

   note right of UC
     Pre: User.state = ACTIVE
     Post: User.state = BLOCKED
     Reversible: UC_USR_06
     Distinto de BR-015 (automatico)
   end note

   @enduml
