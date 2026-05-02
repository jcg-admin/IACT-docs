.. _uc-pip-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Analista\nde Datos" as USR
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_03\nDisponibilidad\nde Datos" as UC03
 }
 USR --> UC03
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/datos/disponibilidad/?trimestre=;
 :JWT + RBAC (ver_disponibilidad_datos);
 :Consultar Registro de Ejecuciones (ultima exitosa);
 if (Existe ejecucion exitosa?) then (no)
   :Retornar estado_frescura=vencido;
   stop
 endif
 :Calcular minutos_desde_etl;
 :Asignar estado_frescura;
 :200 con DisponibilidadDatos;
 stop
 @enduml

8.3 Estado de frescura de datos
================================

.. uml::

 @startuml
 [*] --> fresco : ETL exitoso (< 12 hs)
 fresco --> degradado : > 12 hs sin actualizacion
 degradado --> vencido : > 24 hs sin actualizacion
 vencido --> fresco : ETL exitoso
 degradado --> fresco : ETL exitoso
 @enduml

8.4 Componentes
===============

.. uml::

 @startuml
 component "DisponibilidadDatosService" as S
 component "ETLEjecucionRepo" as R
 component "DisponibilidadBuilder" as B
 S --> R
 S --> B
 @enduml
