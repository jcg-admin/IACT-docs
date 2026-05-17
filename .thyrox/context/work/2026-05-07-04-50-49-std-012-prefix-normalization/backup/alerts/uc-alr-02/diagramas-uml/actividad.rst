8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/alerts/active/;
 :JWT + RBAC + segmento;
 :Query AlertRepo state ∈ {firing, ack};
 :Ordenar severity + fired_at;
 :200 OK;
 :Frontend renderiza + auto-refresh 10s;
 stop
 @enduml

