8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_09 — crear

 @startuml
 start
 :POST /api/me/filters/;
 if (JWT?) then (no)
   :401; stop
 endif
 :Validar nombre + filtros + segmentos;
 if (Cross-segmento?) then (si)
   :400 SEGMENT_VIOLATION; stop
 endif
 if (User > 50?) then (si)
   :429; stop
 endif
 :registrar;
 :201;
 stop
 @enduml

