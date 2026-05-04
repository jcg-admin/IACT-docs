7. Diagrama de colaboraciones
-----------------------------

**Propósito:** cómo los objetos trabajan juntos para cumplir un
objetivo. Objetos + enlaces + mensajes numerados.

**Cuándo usarlo:** cuando quieres mostrar la **arquitectura de
interacción** entre componentes (quién trabaja con quién).

**Lección completa:** :doc:`uml-10-diagramas-colaboraciones`.

.. uml::

   @startuml

   object Cronometro
   object Manguera
   object Tambor

   Cronometro -> Manguera : "2: detener agua"
   Cronometro -> Tambor   : "3: activar giro"
   Manguera   -> Tambor   : "1: abrir / llenar"
   @enduml

----
