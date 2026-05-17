8. Generalización entre actores
===============================

La generalización también aplica entre **actores** — útil
para mostrar la jerarquía de roles del proyecto.

.. uml::

   @startuml

   actor Usuario
   actor Operador
   actor Supervisor
   actor "Admin Acceso"   as AdminAcceso
   actor "Admin Pipeline" as AdminPipeline
   actor Auditor

   Usuario <|-- Operador
   Usuario <|-- Supervisor
   Usuario <|-- AdminAcceso
   Usuario <|-- AdminPipeline
   Usuario <|-- Auditor

   note right of Usuario
     Usuario base:
       login(), logout(),
       changePassword().
     Cada rol especializado
     hereda esto + agrega
     funciones específicas.
   end note
   @enduml
