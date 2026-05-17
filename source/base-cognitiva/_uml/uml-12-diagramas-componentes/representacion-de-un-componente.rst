Representación de un componente
-------------------------------

El símbolo principal es un **rectángulo que tiene otros dos
rectángulos pequeños sobrepuestos en su lado izquierdo**.

.. uml::

   @startuml
   allowmixing

   component "MiComponente" as C
   @enduml

Si el componente es miembro de un **paquete**, puede usar el
nombre del paquete como prefijo. También puede agregar
información que muestre algún detalle del componente, como las
clases que implementa.

.. uml::

   @startuml
   allowmixing

   package "Editor" {
     component "Editor.exe" as Ed {
       component "Documento"    as Doc
       component "Vista"        as Vis
       component "Controlador"  as Ctrl
     }
   }
   @enduml

Otra forma de mostrar las clases que implementa un componente
(aunque por lo general desordena el diagrama):

.. uml::

   @startuml
   allowmixing

   component "Editor.exe" as Ed
   class Documento
   class Vista
   class Controlador
   Ed ..> Documento  : <<implements>>
   Ed ..> Vista       : <<implements>>
   Ed ..> Controlador : <<implements>>
   @enduml
