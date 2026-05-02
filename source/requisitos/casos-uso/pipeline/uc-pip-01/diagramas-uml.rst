.. _uc-pip-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Supervisor\nde Operaciones" as USR
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_01\nSupervisar ETL" as UC01
   usecase "Ver errores ETL" as DR
 }
 USR --> UC01
 UC01 ..> DR : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/etl/supervision/;
 :JWT + RBAC (view_etl_status);
 :Consultar Registro de Ejecuciones;
 :Construir ResumenSalud;
 :200 con estado general;
 stop
 @enduml

8.3 Estados de ejecucion ETL
=============================

.. uml::

 @startuml
 [*] --> en_ejecucion : Disparador ETL invoca SP
 en_ejecucion --> exitoso : SP completa sin errores
 en_ejecucion --> fallido : SP lanza error
 exitoso --> [*]
 fallido --> [*]
 @enduml

8.4 Clases
==========

.. uml::

 @startuml
 class SupervisionETLService
 class ETLEjecucionRepo
 class ResumenSaludBuilder
 SupervisionETLService --> ETLEjecucionRepo
 SupervisionETLService --> ResumenSaludBuilder
 @enduml
