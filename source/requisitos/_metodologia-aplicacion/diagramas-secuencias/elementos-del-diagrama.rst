2.1 Elementos del diagrama
--------------------------

Cinco elementos canónicos: **participantes** (rectángulos
arriba), **línea de vida** (punteada vertical),**activación**
(rectángulo en línea de vida), **mensaje** (flecha horizontal
etiquetada), **tiempo** (eje vertical, arriba → abajo).

.. uml::

   @startuml

   participant Objeto1
   participant Objeto2
   participant Objeto3

   Objeto1 -> Objeto2 : mensaje 1
   activate Objeto2
   Objeto2 -> Objeto3 : mensaje 2
   activate Objeto3
   Objeto3 --> Objeto2 : retorno
   deactivate Objeto3
   Objeto2 --> Objeto1 : retorno
   deactivate Objeto2
   @enduml
