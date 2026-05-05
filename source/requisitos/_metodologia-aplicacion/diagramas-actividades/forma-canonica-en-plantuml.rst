Forma canónica en PlantUML
--------------------------

.. uml::

   @startuml
   start
   :Actividad 1;
   :Actividad 2;
   if (condicion?) then (si)
     :Actividad 3;
   else (no)
     :Actividad 4;
   endif
   stop
   @enduml
