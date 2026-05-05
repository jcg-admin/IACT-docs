Diagrama de componentes
=======================

El moderno desarrollo de software se realiza mediante
**componentes**, lo que es particularmente importante en los
procesos de desarrollo en equipo.

A continuación, la manera en que UML representa un componente de
software.

.. uml::

   @startuml

   component "Controlador\nde Lavado" as C {
     [Lógica de Ciclo]
     [Sensor de Carga]
   }
   @enduml
