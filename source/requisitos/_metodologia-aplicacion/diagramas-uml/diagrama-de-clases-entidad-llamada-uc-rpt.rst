1. Diagrama de clases — entidad ``Llamada`` (UC_RPT)
====================================================

.. uml::

   @startuml

   class Llamada {
     - id : Integer
     - centro_id : Integer
     - campana_id : Integer
     - servicio_id : Integer
     - tipo : Enum
     - duracion_seg : Integer
     - tiempo_espera_seg : Integer
     - resultado : Enum
     - fecha : DateTime
     + getDuracion() : Integer
     + esAbandonada() : Boolean
     + perteneceA(segmento : SegmentoDatos) : Boolean
   }
   @enduml

**Aplicación:** UC_RPT_01..14 consumen ``getDuracion()`` y
``esAbandonada()`` para calcular métricas. BR_012 valida
``perteneceA(segmento)`` antes de devolver filas. DOC-24
integra ésta con todas las demás clases.

**Perspectiva:** ESTÁTICA. **Audiencia:** Devs / Arquitectos.

----
