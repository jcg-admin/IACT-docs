8.4 Diagrama de estados — Assignment
====================================

.. uml::
 :caption: Maquina de estados de un Assignment

 @startuml

 [*] --> ACTIVE : UC_ACC_01\n(asignacion)

 ACTIVE --> REVOKED : UC_ACC_02\n(revocacion explicita)
 ACTIVE --> REVOKED : UC_USR_04\n(eliminacion del User)
 ACTIVE --> EXPIRED : cron job\n(marca_tiempo_actual > expires_at)
 ACTIVE --> ACTIVE : UC_ACC_01 idempotente\n(no cambia)

 REVOKED --> [*]
 EXPIRED --> [*]

 note right of ACTIVE
   UNIQUE (user, function, ACTIVE)
   impide duplicados
 end note

 note right of REVOKED
   Preservado como historial.
   Re-asignacion crea NUEVO Assignment
   (no reactiva — FA-06)
 end note

 @enduml

