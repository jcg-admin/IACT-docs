Multiplicidad mínima del primer modelo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aunque este es un primer paso, conviene incorporar
multiplicidad desde el inicio. La forma del par
Llamada-Segmento en IACT:

.. uml::

   @startuml
   class Call {
     - id : Integer
     - duration_sec : Integer
     - date : DateTime
   }
   class Segment {
     - id : Integer
     - name : String
   }
   Call "1..*" -- "1" Segment : belongs to
   @enduml

Lectura: cada ``Llamada`` pertenece a un único
``Segmento`` (un segmento por llamada — BR_012); cada
``Segmento`` puede tener muchas llamadas (1 a varias).
Esa precisión es lo que diferencia un modelo embrionario
de uno operativo.
