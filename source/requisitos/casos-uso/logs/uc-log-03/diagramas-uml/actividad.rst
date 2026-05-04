8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST search;
 :JWT + RBAC;
 :Validar query + range;
 :Throttle;
 :FTS search;
 :Sanitize + cap;
 :200;
 stop
 @enduml

8.3 Componentes — identico a UC_AUD_02 FTS.

8.4 Secuencia — identica a UC_AUD_02.
