Cómo se ve aplicado
~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   title Modelo de dominio IACT — cluster RBAC
   class User
   class Group
   class Function
   User "0..*" o-- "0..*" Group : assigned to
   Group "1..*" o-- "0..*" Function : groups
   @enduml

El título aparece centrado en la parte superior del
diagrama, ofreciendo contexto inmediato sin que el
lector tenga que leer el cuerpo para entender de qué
trata.
