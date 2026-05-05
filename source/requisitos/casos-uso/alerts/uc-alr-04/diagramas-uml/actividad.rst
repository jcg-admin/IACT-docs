8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET con filtros + period;
 :JWT + RBAC + segmento;
 :Validar range ≤ 1 ano;
 :Cache lookup;
 :Query Alert resolved/closed;
 :Calcular time-to-ack/resolve;
 :Build summary;
 :Cache write;
 :200;
 stop
 @enduml

