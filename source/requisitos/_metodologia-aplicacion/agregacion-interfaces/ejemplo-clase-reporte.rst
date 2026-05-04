6.1 Ejemplo — clase ``Reporte``
-------------------------------

.. uml::

   @startuml
   allowmixing

   class Reporte {
     - segmento_aplicado : SegmentoDatos
     - cache_ttl : Integer
     - sql_crudo : String
     # registrarConsulta()
     # invalidarCache()
     + generar(filtros : Filtro)
     + exportar(formato : Enum)
     + getResultados()
   }
   note right of Reporte
     Visibilidad:
       + generar / exportar / getResultados
         → interfaz pública del UC_RPT
       # registrarConsulta / invalidarCache
         → heredable por subtipos
         (ReporteHistorico, ReporteAgentes...)
       - segmento_aplicado / cache_ttl /
         sql_crudo → detalles internos
         (segmentación BR_012, SLA CNST_017)
   end note
   @enduml
