8.4 Secuencia
=============

.. uml::

 @startuml
 actor "manage_own_agent_state" as manage_own_agent_state
 participant "Endpoint" as Endpoint
 database "AgentStateRepo" as Agentstaterepo
 participant "AuditSvc" as Auditsvc
 participant "CallRouter" as Callrouter
 manage_own_agent_state -> Endpoint: POST new_state
 Endpoint -> Agentstaterepo: BEGIN
 Endpoint -> Agentstaterepo: actualizar state
 Endpoint -> Auditsvc: emit AGENT_STATE_CHANGED
 Endpoint -> Agentstaterepo: COMMIT
 Endpoint -> Callrouter: state changed
 Endpoint --> manage_own_agent_state: 200
 @enduml
