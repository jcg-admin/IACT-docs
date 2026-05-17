.. _uc-usr-07-parte-08-diagrama-caso-de-uso:

8.1 Diagrama de caso de uso
============================

.. uml::

   @startuml

   left to right direction

   actor "edit_own_profile" as USER
   actor "AuthorizationGuard" as GUARD
   actor "EmailValidator" as EMAIL
   actor "AuditService" as AUDIT

   rectangle "Sistema IACT — UC_USR_07" {
     usecase "Editar Perfil Propio" as UC
     usecase "Validar funcion\nedit_own_profile" as INC1 <<include>>
     usecase "Validar formato\ny unicidad email" as INC2 <<include>>
     usecase "Emitir AuditEvent\nPROFILE_UPDATED" as INC3 <<include>>
     usecase "Sin diff →\nno emit AuditEvent" as EXT1 <<extend>>
   }

   USER --> UC

   UC ..> INC1 : <<include>>
   UC ..> INC2 : <<include>>
   UC ..> INC3 : <<include>>
   UC <.. EXT1 : <<extend>>

   INC1 --> GUARD
   INC2 --> EMAIL
   INC3 --> AUDIT

   note right of UC
     Self-service: actor edita
     su propio perfil unicamente.
     target_user_id = jwt.user_id
     (no en URL — defensa contra
     impersonation).
   end note

   @enduml
