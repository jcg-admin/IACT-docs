.. _uc-opr-08-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_own_performance_dashboard" as view_own_performance_dashboard
 rectangle "MOD_Operator" {
   usecase "UC_OPR_08\nMy Dashboard" as UC
 }
 view_own_performance_dashboard --> UC
 @enduml

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

8.3 Componentes
===============

.. uml::

 @startuml
 component "Endpoint" as Endpoint
 component "Cache" as Cache
 component "AgentDailyStatRepo" as Agentdailystatrepo
 component "RankingService" as Rankingservice
 Endpoint --> Cache
 Endpoint --> Agentdailystatrepo
 Endpoint --> Rankingservice
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "view_own_performance_dashboard" as view_own_performance_dashboard
 participant "Endpoint" as Endpoint
 database "Stats" as Stats
 view_own_performance_dashboard -> Endpoint: GET dashboard
 Endpoint -> Stats: query own
 Stats --> Endpoint: rows
 Endpoint --> view_own_performance_dashboard: 200 + KPIs
 @enduml
