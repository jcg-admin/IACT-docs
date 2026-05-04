8.4 Diagrama de estados — User.state
====================================

.. uml::
 :caption: Maquina de estados del User en UC_USR_03

 @startuml

 [*] --> ACTIVE : UC_USR_01

 ACTIVE --> INACTIVE : UC_USR_03\n(suspension temporal)
 ACTIVE --> BLOCKED : UC_USR_03\n(bloqueo administrativo)\n+cierra Sessions
 INACTIVE --> ACTIVE : UC_USR_03\n(reactivacion)
 INACTIVE --> BLOCKED : UC_USR_03
 BLOCKED --> ACTIVE : UC_USR_03\n(desbloqueo)
 BLOCKED --> INACTIVE : UC_USR_03

 ACTIVE --> ELIMINATED : UC_USR_04
 INACTIVE --> ELIMINATED : UC_USR_04
 BLOCKED --> ELIMINATED : UC_USR_04

 ELIMINATED --> [*]

 note right of BLOCKED
   Side-effect:
   Sessions ACTIVE -> CLOSED
   tokens blacklisted
 end note

 note right of ELIMINATED
   UC_USR_03 NO permite
   transicion hacia
   ELIMINATED — solo
   UC_USR_04
 end note

 @enduml
