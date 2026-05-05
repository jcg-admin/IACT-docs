8.3 Estado
==========

.. uml::

 @startuml
 [*] --> available
 available --> on_break : POST
 on_break --> available : POST resume
 @enduml

