8.4 Diagrama de estados — User.state
====================================

.. uml::
 :caption: User.state con foco en transicion a ELIMINATED

 @startuml

 [*] --> ACTIVE : UC_USR_01

 ACTIVE --> INACTIVE : UC_USR_03
 ACTIVE --> BLOCKED : UC_USR_03
 INACTIVE --> ACTIVE : UC_USR_03
 BLOCKED --> ACTIVE : UC_USR_03

 ACTIVE --> ELIMINATED : UC_USR_04\n+ revoke Assignments\n+ close Sessions
 INACTIVE --> ELIMINATED : UC_USR_04
 BLOCKED --> ELIMINATED : UC_USR_04

 ELIMINATED --> [*] : (terminal — registro\npreservado por BR-009)

 note right of ELIMINATED
   - eliminated_at, eliminated_by_admin_id
   - email/username NO liberados
   - data historica preservada
   - retencion CNST-006 (2 anios)
 end note

 @enduml

