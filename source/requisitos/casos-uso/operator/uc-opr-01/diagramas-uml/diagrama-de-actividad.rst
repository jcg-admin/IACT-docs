8.3 Diagrama de actividad
=========================

.. uml::

 @startuml
 start
 :POST cambiar estado;
 :JWT;
 :Validar new_state + transicion;
 if (Reason requerida y missing?) then (si)
   :400; stop
 endif
 :BEGIN tx;
 :actualizar AgentState;
 :registrar AgentStateHistory;
 :Audit AGENT_STATE_CHANGED;
 :COMMIT;
 :Notify CallRouter;
 :200;
 stop
 @enduml

