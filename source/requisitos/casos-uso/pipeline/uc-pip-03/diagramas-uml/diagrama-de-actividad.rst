.. _uc-pip-03-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Consultar disponibilidad de datos
================================================================

.. uml::
 :caption: UC_PIP_03 — flujo de consulta de frescura.

 @startuml

 start
 :Invoker emite GET /api/v1/datos/disponibilidad/ con trimestre;
 :Servicio de Aplicacion verifica capability view_data_availability;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Consultar PipelineExecutionRepo (ultima exitosa);
 if (Existe ejecucion exitosa?) then (no)
   :Retornar estado_frescura=vencido;
   :200 OK;
   stop
 endif
 :Calcular minutos_desde_etl;
 :Asignar estado_frescura (fresco / degradado / vencido);
 :200 OK con DisponibilidadDatos;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-componentes`.
 - :doc:`diagrama-de-estados-frescura-datos`.
