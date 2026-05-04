5. Diagrama de secuencias
-------------------------

**Propósito:** cómo interactúan objetos entre sí a lo largo del
tiempo. Participantes (rectángulos arriba) + mensajes (flechas)
+ tiempo (vertical, arriba→abajo).

**Cuándo usarlo:** cuando necesitas mostrar el **flujo
temporal** de interacciones (quién habla con quién, en qué
orden, qué se intercambian).

**Lección completa:** :doc:`/base-cognitiva/_uml/uml-09-diagramas-secuencias/index`.

.. uml::

   @startuml

   participant Manguera as M
   participant Tambor   as T
   participant Drenaje  as D

   M -> T : llenar()
   note right of T : reposar 5 min
   T -> M : cerrar()
   T -> T : girar 15 min
   T -> D : drenar()
   @enduml

----
