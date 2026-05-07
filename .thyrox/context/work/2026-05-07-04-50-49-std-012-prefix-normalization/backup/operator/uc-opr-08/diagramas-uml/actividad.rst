8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /me/dashboard;
 :JWT;
 :Cache lookup;
 :Query own stats;
 :Calcular KPIs;
 :Ranking opt-in;
 :200;
 stop
 @enduml

