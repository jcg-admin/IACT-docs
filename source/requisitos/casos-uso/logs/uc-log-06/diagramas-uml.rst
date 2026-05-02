.. _uc-log-06-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "User con funcion\nview_system_status" as USR
 rectangle "MOD_Logs" {
   usecase "UC_LOG_06\nEstado Sistema" as UC06
   usecase "UC_PIP_01" as P
   usecase "UC_ALR_02" as A
 }
 USR --> UC06
 UC06 ..> P : <<include>>
 UC06 ..> A : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET status;
 :JWT + RBAC;
 :Cache lookup;
 fork
   :Check services;
 fork again
   :Check deps;
 fork again
   :Query ETL summary;
 fork again
   :Query alerts active count;
 end fork
 :Compute overall status;
 :Cache write;
 :200;
 stop
 @enduml

8.3 Estado overall
==================

.. uml::

 @startuml
 [*] --> green
 green --> yellow : 1+ deg
 yellow --> red : critical
 red --> yellow : recover
 yellow --> green : recover
 @enduml

8.4 Componentes
===============

.. uml::

 @startuml
 component "Status service" as S
 component "ServiceHealthChecker" as SH
 component "DepHealthChecker" as DH
 component "ETLProbe" as E
 component "AlertCounter" as A
 S --> SH
 S --> DH
 S --> E
 S --> A
 @enduml
