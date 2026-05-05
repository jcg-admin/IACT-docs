Cómo se ve aplicado
~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   title Modelo de dominio IACT — cluster RBAC
   class Usuario
   class Grupo
   class Funcion
   Usuario "0..*" o-- "0..*" Grupo : asignado a
   Grupo "1..*" o-- "0..*" Funcion : agrupa
   @enduml

El título aparece centrado en la parte superior del
diagrama, ofreciendo contexto inmediato sin que el
lector tenga que leer el cuerpo para entender de qué
trata.
