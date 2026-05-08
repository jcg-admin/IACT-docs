8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST rule;
 :JWT + RBAC;
 :Validar metric, scope, condition;
 if (Cross-segmento?) then (si)
   :400; stop
 endif
 if (Action invalido?) then (si)
   :400; stop
 endif
 :registrar;
 :Audit ALERT_RULE_CREATED;
 :Notificar reload;
 :201;
 stop
 @enduml

