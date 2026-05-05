5.1 Clase ``Reporte`` (UC_RPT)
------------------------------

.. uml::

   @startuml

   class Reporte {
     == interfaz pública ==
     + generar(filtros : FiltroReporte) : Reporte
     + exportar(formato : Enum) : Archivo
     + getResultados() : List<Fila>
     + getMetadatos() : Metadatos
     == privado / oculto ==
     - validarSegmentoUsuario()
     - construirQuerySQL()
     - aplicarFiltrosPorSegmento()
     - cachearResultado()
     - registrarConsulta()
     - aplicarThrottling(formato)
   }
   note right of Reporte
     El cliente sólo ve:
       generar(), exportar(),
       getResultados(),
       getMetadatos()
     El sistema gestiona internamente:
       segmentación (CNST_008), SQL,
       cache, auditoría, throttling
       (CNST_020).
   end note
   @enduml
