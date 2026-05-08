8.3 Estado de SoDRule
=====================

.. uml::

 @startuml
 [*] --> ACTIVE : create_separation_rule
 ACTIVE --> INACTIVE : disable_separation_rule
 INACTIVE --> ACTIVE : reactivate\n(PATCH state=ACTIVE)
 ACTIVE --> ACTIVE : update_separation_rule\n(incrementa version)
 @enduml
