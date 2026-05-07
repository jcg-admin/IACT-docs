8.3 Estados AccessGroup
=======================

.. uml::
 :caption: Maquina de estados

 @startuml

 [*] --> ACTIVE : UC_PERM_05 CREATE\n(o predefinido seed)
 ACTIVE --> ACTIVE : UC_PERM_05 PATCH
 ACTIVE --> RETIRED : UC_PERM_05 DELETE
 RETIRED --> [*]

 note right of RETIRED
   No vuelve a ACTIVE
   Migracion: nuevo CREATE
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/access-group`
 - :doc:`/arquitectura-tecnica/domain-model/access-group-repo`
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function`
 - :doc:`/requisitos/reglas-negocio/br-009-bajas-logicas`
