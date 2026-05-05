8.4 Diagrama de transicion Assignment.state
===========================================

.. uml::
 :caption: Maquina de estados Assignment con foco UC_ACC_02

 @startuml

 [*] --> ACTIVE : UC_ACC_01\n(asignacion)

 ACTIVE --> REVOKED : UC_ACC_02\n(revocacion explicita)
 ACTIVE --> REVOKED : UC_USR_04\n(eliminacion del User)
 ACTIVE --> EXPIRED : cron job\n(NOW > expires_at)

 REVOKED --> [*]
 EXPIRED --> [*]

 note right of REVOKED
   revoked_by_admin_id
   revoked_at
   revoke_reason (obligatorio)
   Historial preservado (BR-009)
 end note

 @enduml
