8.3 Diagrama de estructura del menu
===================================

.. uml::
 :caption: Estructura jerarquica

 @startuml

 class Menu {
   user_id
   locale_used
   generated_at
   cache: bool
 }

 class Domain {
   code
   label
   order
 }

 class Section {
   code
   label
   icon
   order
 }

 class Action {
   code
   label
   function_code
   order
 }

 Menu "1" -- "*" Domain
 Domain "1" -- "*" Section
 Section "1" -- "*" Action

 @enduml

