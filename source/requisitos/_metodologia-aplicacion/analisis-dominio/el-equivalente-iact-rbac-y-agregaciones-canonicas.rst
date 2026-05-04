El equivalente IACT — RBAC y agregaciones canónicas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El cluster RBAC de IACT (ver § 11 de
:doc:`/requisitos/_metodologia-aplicacion/agregacion-interfaces/index`) está construido sobre
agregaciones, no composiciones:

.. uml::

   @startuml
   class Grupo
   class Funcion
   class Usuario
   class Permiso
   class ReglaSoD

   Grupo "1" o-- "*" Funcion : agrupa
   Grupo "1" o-- "*" Usuario : asigna
   ReglaSoD "1" -- "2..*" Funcion : restringe
   Permiso ..> Grupo : pertenece
   @enduml

Lectura:

- ``Grupo`` ◇ ``Funcion`` — **agregación**. Las
  funciones del catálogo RBAC existen
  independientemente de cualquier grupo. Eliminar un
  grupo no elimina las funciones (CNST_030 SoD se
  conserva a nivel de catálogo).
- ``Grupo`` ◇ ``Usuario`` — **agregación**. Los
  usuarios existen sin grupos; pueden pertenecer a
  varios; eliminar un grupo no elimina los usuarios.
- ``ReglaSoD`` ↔ ``Funcion`` — asociación: la regla
  referencia funciones del catálogo; ambas existen
  independientemente.
