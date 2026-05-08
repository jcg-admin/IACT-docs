8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/datos/disponibilidad/?trimestre=;
 :JWT + RBAC (view_data_availability);
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

