.. _uc-opr-07-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "request_break" as request_break
 rectangle "MOD_Operator" {
   usecase "UC_OPR_07\nBreak" as UC
   usecase "UC_OPR_01\nState change" as S
 }
 request_break --> UC
 UC ..> S : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST break;
 :Validar quota;
 if (Excedida?) then (si)
   :409; stop
 endif
 :Delegar UC_OPR_01;
 :Iniciar timer;
 :200;
 stop
 @enduml

8.3 Estado
==========

.. uml::

 @startuml
 [*] --> available
 available --> on_break : POST
 on_break --> available : POST resume
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "request_break" as request_break
 participant "Endpoint" as Endpoint
 participant "Policy" as Policy
 request_break -> Endpoint: POST break
 Endpoint -> Policy: check quota
 Policy --> Endpoint: ok
 Endpoint --> request_break: 200
 @enduml
