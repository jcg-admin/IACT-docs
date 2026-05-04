.. _uc-opr-09-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_own_call_history" as view_own_call_history
 rectangle "MOD_Operator" {
   usecase "UC_OPR_09\nMy History" as UC
 }
 view_own_call_history --> UC
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /me/calls/;
 :JWT;
 :Validar range;
 :Query own;
 :Sanitize;
 :Paginar;
 :200;
 stop
 @enduml

8.3 Componentes
===============

.. uml::

 @startuml
 component "Endpoint" as Endpoint
 component "CallSessionRepo" as Callsessionrepo
 component "Sanitizer" as Sanitizer
 Endpoint --> Callsessionrepo
 Endpoint --> Sanitizer
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "view_own_call_history" as view_own_call_history
 participant "Endpoint" as Endpoint
 database "Calls" as Calls
 view_own_call_history -> Endpoint: GET /me/calls
 Endpoint -> Calls: query own
 Calls --> Endpoint: rows
 Endpoint --> view_own_call_history: 200
 @enduml
