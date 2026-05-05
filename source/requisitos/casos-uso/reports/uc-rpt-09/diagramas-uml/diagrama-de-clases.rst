8.3 Diagrama de clases
======================

.. uml::
 :caption: Estructura

 @startuml
 class SavedFilter {
   id, name, filters,
   period_relative, applies_to,
   is_default, is_invalid
 }
 class FilterValidator {
   validate(filter, user_segments)
 }
 SavedFilter -- FilterValidator
 @enduml

