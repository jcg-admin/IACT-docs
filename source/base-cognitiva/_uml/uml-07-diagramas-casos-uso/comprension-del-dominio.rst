Comprensión del dominio
-----------------------

Para dicha compresión se tiene que empezar con las entrevistas
al cliente; en la entrevista tiene que surgir el diagrama de
clases.

El diagrama de clases podría incluir las siguientes clases:
``Consultor``, ``Cliente``, ``Proyecto``, ``Propuesta``,
``Datos`` e ``Informe``.

.. uml::

   @startuml

   class Consultor
   class Cliente
   class Proyecto
   class Propuesta
   class Datos
   class Informe

   Consultor "1..*" -- "0..*" Proyecto      : trabaja en
   Cliente   "1"    -- "0..*" Proyecto      : encarga
   Proyecto  "1"    -- "1..*" Propuesta     : produce
   Proyecto  "1"    -- "0..*" Datos         : recopila
   Proyecto  "1"    -- "1..*" Informe       : entrega
   @enduml
