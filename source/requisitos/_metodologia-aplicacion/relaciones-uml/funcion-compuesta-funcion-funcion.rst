5.2 Función compuesta — Funcion → Funcion
-----------------------------------------

Algunas funciones del catálogo RBAC se componen de otras
(macro-funciones que implican varias atómicas):

.. uml::

   @startuml

   class Function
   Function "0..*" -- "0..*" Function : implies
   note right of Function
     Reflexiva en el catálogo
     de 74 funciones (CNST_029):
       p.ej. ``manage_users``
       implica view_users +
       create_users +
       modify_users +
       deactivate_users.
   end note
   @enduml
