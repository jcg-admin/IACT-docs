Demostraciones visuales
^^^^^^^^^^^^^^^^^^^^^^^

Cada tipo de flecha renderizado con dos nodos
genéricos. Útil como referencia rápida cuando se
duda si la sintaxis produce el efecto esperado.

**Flecha continua con cabeza**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A --> B
   @enduml

**Flecha continua etiquetada**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A --> B : text
   @enduml

**Línea sin cabeza**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A -- B
   @enduml

**Línea sin cabeza etiquetada**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A -- B : text
   @enduml

**Flecha punteada con cabeza**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A ..> B
   @enduml

**Flecha punteada etiquetada**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A ..> B : text
   @enduml

**Flecha gruesa con cabeza**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A -[bold]-> B
   @enduml

**Flecha gruesa etiquetada**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A -[bold]-> B : text
   @enduml

**Encadenamiento — A → B → C**

.. uml::

   @startuml
   rectangle A
   rectangle B
   rectangle C
   A --> B : text
   B --> C : text2
   @enduml

**Bifurcación múltiple — A → B/C → D**

.. uml::

   @startuml
   rectangle A
   rectangle B
   rectangle C
   rectangle D
   A --> B
   A --> C
   B --> D
   C --> D
   @enduml

**Flecha alargada — empuja al destino al siguiente
rango**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A ---> B : flecha mas larga
   @enduml

**Flecha forzada en dirección horizontal**

.. uml::

   @startuml
   rectangle A
   rectangle B
   A -right-> B : forzada a la derecha
   @enduml

Estas demos no representan ningún UC IACT
específico; sirven solo de **calibración visual**
del rendering. Para cualquier modelo del proyecto,
elegir el tipo según las políticas IACT de las
subsecciones anteriores.
