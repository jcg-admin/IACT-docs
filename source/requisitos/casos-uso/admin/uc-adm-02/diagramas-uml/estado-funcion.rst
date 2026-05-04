8.3 Estado de Function
======================

.. uml::

 @startuml
 [*] --> ACTIVE : manage_function_catalog\n(crear)
 ACTIVE --> INACTIVE : manage_function_catalog\n(deactivate)
 INACTIVE --> ACTIVE : manage_function_catalog\n(reactivate)
 ACTIVE --> ACTIVE : manage_function_catalog\n(update description/scope)
 @enduml
