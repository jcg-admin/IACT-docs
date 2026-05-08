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

