8.4 Diagrama de relaciones
==========================

.. uml::
 :caption: UC_ACC_09 consume eventos de los
           UCs productores

 @startuml

 [UC_ACC_01 (assign)] --> [AuditEvent]
 [UC_ACC_02 (revoke)] --> [AuditEvent]
 [UC_ACC_04 (AGR)] --> [AuditEvent]
 [UC_ACC_05 (separation of duties)] --> [AuditEvent]
 [UC_ACC_08 (excepc)] --> [AuditEvent]
 [UC_USR_04 (eliminate)] --> [AuditEvent]
 [AuditEvent] --> [UC_ACC_09 (vista audit)]
 [UC_ACC_09 (vista audit)] --> [Auditor]

 note bottom of [AuditEvent]
   AuditEvent es append-only
   (CNST-025); UC_ACC_09 solo lee.
 end note

 @enduml
