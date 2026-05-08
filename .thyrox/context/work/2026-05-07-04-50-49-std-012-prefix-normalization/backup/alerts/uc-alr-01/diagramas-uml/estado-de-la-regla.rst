8.3 Estado de la regla
======================

.. uml::

 @startuml
 [*] --> active : crear
 active --> paused : pause
 paused --> active : resume
 active --> [*] : delete
 paused --> [*] : delete
 @enduml

