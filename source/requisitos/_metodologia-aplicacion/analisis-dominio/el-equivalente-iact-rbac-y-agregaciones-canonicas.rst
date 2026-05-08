El equivalente IACT — RBAC y agregaciones canónicas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El cluster RBAC de IACT (ver § 11 de
:doc:`/requisitos/_metodologia-aplicacion/agregacion-interfaces/index`) está construido sobre
agregaciones, no composiciones:

.. uml::

   @startuml
   class Group
   class Function
   class User
   class Permission
   class SeparationRule

   Group "1" o-- "*" Function : groups
   Group "1" o-- "*" User : assigns
   SeparationRule "1" -- "2..*" Function : restricts
   Permission ..> Group : belongs
   @enduml

Lectura:

- ``Grupo`` ◇ ``Funcion`` — **agregación**. Las
  funciones del catálogo RBAC existen
  independientemente de cualquier grupo. Eliminar un
  grupo no elimina las funciones (CNST-030 separacion de funciones se
  conserva a nivel de catálogo).
- ``Grupo`` ◇ ``Usuario`` — **agregación**. Los
  usuarios existen sin grupos; pueden pertenecer a
  varios; eliminar un grupo no elimina los usuarios.
- ``ReglaSeparacion`` ↔ ``Funcion`` — asociación: la regla
  referencia funciones del catálogo; ambas existen
  independientemente.
