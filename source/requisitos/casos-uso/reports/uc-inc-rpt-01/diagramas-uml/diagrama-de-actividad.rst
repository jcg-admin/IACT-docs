.. _uc-inc-rpt-01-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Resolver segmento
================================================

.. uml::
 :caption: UC_INC_RPT_01 — flujo de resolucion de segmento del user.

 @startuml

 start
 :Leer assignments RBAC del usuario;
 if (Es global con view_all_segments?) then (si)
   :Retornar todos los segmentos (es_global=True);
   stop
 endif
 :Mapear segment_id del User a segments accesibles;
 if (Sin segmentos asignados?) then (si)
   :Error EX-02 NoSegmentAssigned;
   stop
 endif
 :Retornar lista de segmentos accesibles;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso-relacion-de-inclusion`.
 - :doc:`diagrama-de-clases`.
 - :doc:`/requisitos/reglas-negocio/br-012-usuario-segmento-unico`.
