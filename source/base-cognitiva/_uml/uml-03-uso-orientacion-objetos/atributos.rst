Atributos
=========

Un atributo es una **propiedad o característica de una clase** y
describe un rango de valores que la propiedad podrá contener en
los objetos (instancias) de la clase. Una clase podrá contener
varios o ningún atributo.

Si el atributo consta de **una sola palabra** se escribe en
**minúsculas**. Si el nombre contiene **más de una palabra**,
cada palabra será unida a la anterior y comenzará con mayúscula,
**a excepción de la primera** que comenzará en minúscula
(``camelCase``).

Los atributos se inician luego de una línea que los separa del
nombre de la clase.

.. uml::

   @startuml

   class Lavadora {
     marca
     modelo
     numeroSerie
     capacidad
   }
   @enduml

Todo objeto de la clase tiene un valor específico en cada
atributo. El nombre de un objeto **inicia con minúscula**, está
**precedido de dos puntos** y luego del nombre de la clase, y
todo el nombre va subrayado.

El nombre ``miLavadora:Lavadora`` es una instancia con nombre,
pero también es posible tener una **instancia anónima**, como
``:Lavadora``.

.. uml::

   @startuml

   object "miLavadora : Lavadora" as ml {
     marca = "Laundatorium"
     modelo = "Washmeister"
     numeroSerie = "GL57774"
     capacidad = 7.0
   }
   object ":Lavadora" as anon {
     marca = "GenericBrand"
     capacidad = 8.0
   }
   @enduml

En el símbolo de la clase, podrá especificar un **tipo** para
cada valor del atributo: cadena (``String``), número de punto
flotante (``Float``), entero (``Integer``), booleano
(``Boolean``), así como otros tipos enumerados.

Para indicar un tipo, utilice dos puntos (``:``) para separar el
nombre del atributo de su tipo. También podrá indicar un
**valor predeterminado** para un atributo.

.. uml::

   @startuml

   class Lavadora {
     marca : String
     modelo : String
     numeroSerie : String
     capacidad : Float = 7.0
     activa : Boolean = false
   }
   @enduml

----
