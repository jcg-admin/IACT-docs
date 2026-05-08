8.4 Diagrama de estados — SoDRule
=================================

.. uml::
 :caption: Maquina de estados de SoDRule

 @startuml

 [*] --> ACTIVE : UC_ACC_05 CREATE

 ACTIVE --> ACTIVE : UC_ACC_05 PATCH
 ACTIVE --> RETIRED : UC_ACC_05 DELETE
 RETIRED --> [*] : (terminal — historial\npreservado)

 note right of RETIRED
   retired_at, retired_by_admin_id,
   retire_reason
   No vuelve a ACTIVE
   (migracion: CREATE nueva)
 end note

 @enduml
