8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET con filtros + period;
 if (JWT?) then (no)
   :401; stop
 endif
 if (RBAC?) then (no)
   :403; stop
 endif
 :Resolver segmento;
 :Cache lookup;
 if (Hit?) then (si)
   :return cached;
   stop
 endif
 :Query AgentDailyStat agregado;
 :Calcular KPIs derivados;
 :Construir summary;
 :Cache write;
 :200;
 stop
 @enduml

