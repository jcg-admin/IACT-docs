.. _uc-alr-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_alerts" as view_alerts
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_02\nAlertas Activas" as UC02
   usecase "UC_ALR_03\nAck inline" as UC03
   usecase "Auto-refresh" as AutoRefresh
 }
 view_alerts --> UC02
 UC02 ..> AutoRefresh : <<extend>>
 UC02 ..> UC03 : <<extend>>
 @enduml

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

8.3 Estado de la alerta
=======================

.. uml::

 @startuml
 [*] --> firing : evaluator dispara
 firing --> acknowledged : UC_ALR_03
 firing --> resolved : metric vuelve normal
 acknowledged --> resolved : metric normal
 acknowledged --> closed : forced close
 resolved --> closed : auto cleanup
 closed --> [*]
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "view_alerts" as view_alerts
 participant "Frontend" as Frontend
 participant "Endpoint" as Endpoint
 database "AlertRepo" as Alertrepo

 view_alerts -> Frontend: abrir vista
 loop cada 10s
   Frontend -> Endpoint: GET /alerts/active
   Endpoint -> Endpoint: JWT + RBAC
   Endpoint -> Alertrepo: query active
   Alertrepo --> Endpoint: rows
   Endpoint --> Frontend: 200
   Frontend -> view_alerts: actualizar UI
 end
 @enduml
