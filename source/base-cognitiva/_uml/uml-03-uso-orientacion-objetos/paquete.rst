Paquete
=======

El **paquete** puede jugar un papel en el nombre de la clase.

Un paquete es la manera en que UML **organiza un diagrama de
elementos**. UML representa un paquete como una **carpeta
tabular** cuyo nombre es una cadena de texto.

.. uml::

   @startuml

   package "Electrodomesticos" {
     class Lavadora
     class Refrigerador
     class HornoMicroondas
   }
   @enduml

.. note::

 Si la clase ``Lavadora`` es parte de un paquete llamado
 ``Electrodomesticos``, podrá darle el nombre
 ``Electrodomesticos::Lavadora``.

El par de dos puntos (``::``) separa al nombre del paquete (a la
izquierda) del nombre de la clase (a la derecha). A este tipo de
nombre se le conoce como **nombre de ruta** y refleja una
relación padre-hijo.

.. uml::

   @startuml

   class "Electrodomesticos::Lavadora" as L
   @enduml

.. caution::

 Evitamos los acentos en los diagramas, e igualmente la letra
 ``ñ``, que sustituimos por ``ni`` (como en ``Anio`` en lugar de
 ``Año``).
