8.4 Diagrama de estados de Session
==================================

Ciclo de vida de la entidad ``Session`` desde la
perspectiva de UC_AUTH_01 y los UCs que la
consumen.

.. uml::
 :caption: Estados de la clase Session

 @startuml

 [*] --> ACTIVE : UC_AUTH_01\n(crear)

 ACTIVE --> ACTIVE : actividad del\nusuario\n(extiende\nexpires_at)

 ACTIVE --> CLOSED : UC_AUTH_02\n(cierre por\nusuario)
 ACTIVE --> CLOSED : UC_AUTH_01 nuevo\n(SUPERSEDED\npor CNST-004)
 ACTIVE --> CLOSED : UC_AUTH_05\n(admin close)
 ACTIVE --> EXPIRED : timeout\n(CNST-005)\nsin actividad

 CLOSED --> [*]
 EXPIRED --> [*]

 note right of ACTIVE
   state vigente
   permite uso de tokens
   expires_at se actualiza
   con cada request
 end note

 note bottom of CLOSED
   close_reason ∈ {
     USER_LOGOUT,
     SUPERSEDED,
     ADMIN_CLOSE,
     EXPIRED
   }
   closed_at = marca_tiempo_actual
 end note

 note bottom of EXPIRED
   transicion automatica
   cuando expires_at < marca_tiempo_actual
   y no hay actividad
 end note

 @enduml

