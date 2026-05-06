1. Diagrama de clases — entidad ``Llamada`` (UC_RPT)
====================================================

.. uml::

   @startuml

   class Call {
     - id : Integer
     - center_id : Integer
     - campaign_id : Integer
     - service_id : Integer
     - type : Enum
     - duration_sec : Integer
     - wait_time_sec : Integer
     - outcome : Enum
     - date : DateTime
     + getDuration() : Integer
     + isAbandoned() : Boolean
     + belongsTo(segment : DataSegment) : Boolean
   }
   @enduml

**Aplicación:** UC_RPT_01..14 consumen ``getDuracion()`` y
``esAbandonada()`` para calcular métricas. BR_012 valida
``perteneceA(segmento)`` antes de devolver filas. DOC-24
integra ésta con todas las demás clases.

**Perspectiva:** ESTÁTICA. **Audiencia:** Devs / Arquitectos.
