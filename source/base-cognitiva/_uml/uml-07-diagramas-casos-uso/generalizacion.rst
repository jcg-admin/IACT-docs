Generalización
--------------

Las clases se heredan entre sí; lo mismo se aplica a los casos
de uso.

En la herencia de los casos de uso, el caso de uso secundario
hereda las acciones y significado del primario, y además agrega
sus propias acciones. Puede aplicar el caso de uso secundario en
cualquier lugar donde aplique el primario.

Deberá imaginar un caso de uso *"Comprar un vaso de gaseosa"*
que se hereda de *"Comprar gaseosa"*. El caso de uso secundario
tiene acciones como *"agregar hielo"* y *"mezclar marcas de
gaseosas"*.

Modelará la generalización de casos de uso con líneas continuas
y una **punta de flecha en forma de triángulo sin rellenar** que
apunta hacia el caso de uso primario.

.. uml::

   @startuml

   left to right direction
   actor Cliente
   rectangle "Máquina de Gaseosas" {
     usecase "Comprar gaseosa"          as UC1
     usecase "Comprar un vaso\nde gaseosa" as UC1G
   }
   Cliente --> UC1
   Cliente --> UC1G
   UC1G --|> UC1
   @enduml

La relación también se puede establecer entre **actores**, así
como entre casos de uso. Si cambia el nombre del representante
como ``Reabastecedor``, tanto éste como el ``Recolector`` serán
secundarios del ``AgenteProveedor``.

.. uml::

   @startuml

   actor "AgenteProveedor" as AP
   actor "Reabastecedor"   as VER_DASHBOARD_IVR
   actor "Recolector"      as RESOLVER_SEGMENTO
   AP <|-- VER_DASHBOARD_IVR
   AP <|-- RESOLVER_SEGMENTO
   @enduml
