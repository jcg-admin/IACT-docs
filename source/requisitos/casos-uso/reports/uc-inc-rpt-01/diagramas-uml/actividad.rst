8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Leer DIDs RBAC del usuario;
 if (Es administrador global?) then (si)
   :Retornar todos los segmentos;
   stop
 endif
 :Mapear DIDs a segmentos;
 if (Sin segmentos?) then (si)
   :Error EX-02;
   stop
 endif
 :Retornar lista de segmentos accesibles;
 stop
 @enduml

