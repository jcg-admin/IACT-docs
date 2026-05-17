8.2 Restricción ``{xor}`` — Permiso vía grupo o excepcional
-----------------------------------------------------------

Un usuario obtiene permiso a una función **vía un grupo asignado
o vía un permiso excepcional**, no ambos a la vez para la misma
función:

.. uml::

   @startuml

   class User
   class Group
   class ExceptionalPermission

   User --> Group : assigned_to
   User --> ExceptionalPermission : has
   note "{xor} para una misma\nfunción atómica" as NotaXor
   Group .. NotaXor
   ExceptionalPermission .. NotaXor
   @enduml
