.. _uc-inc-rpt-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso — relacion de inclusion
========================================

.. uml::

 @startuml
 !include ../../_static/plantuml-styles.puml
 left to right direction
 actor "Analista / Supervisor\n(actor del UC invocador)" as USR
 rectangle "MOD_Reports" {
   usecase "UC_RPT_NN\n(cualquier reporte)" as RPTNN
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC01
 }
 USR --> RPTNN
 RPTNN ..> INC01 : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 !include ../../_static/plantuml-styles.puml
 start
 :Leer DIDs RBAC del usuario;
 if (Es administrador global?) then (si)
   :Retornar todos los segmentos;
   stop
 endif
 :Mapear DIDs a segmentos;
 if (Sin segmentos?) then (si)
   :Error EX-02;
   stop
 endif
 :Retornar lista de segmentos accesibles;
 stop
 @enduml

8.3 Clases
==========

.. uml::

 @startuml
 !include ../../_static/plantuml-styles.puml
 class SegmentResolver {
   + resolve(user_id) : list[str]
 }
 class RBACRepo {
   + get_did_assignments(user_id) : list[str]
   + is_global_admin(user_id) : bool
 }
 SegmentResolver --> RBACRepo
 @enduml
