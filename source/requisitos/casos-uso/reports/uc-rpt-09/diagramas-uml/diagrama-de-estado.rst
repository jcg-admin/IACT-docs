8.4 Diagrama de estado
======================

.. uml::
 :caption: SavedFilter

 @startuml
 [*] --> active : crear
 active --> invalid : segmentos cambian
 invalid --> active : segmentos restored
 active --> [*] : delete
 invalid --> [*] : delete
 @enduml
