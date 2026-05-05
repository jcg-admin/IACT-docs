6.1 Ejemplo IACT — UC_RPT_03 (Ver reportes históricos) extendido
----------------------------------------------------------------

.. uml::

   @startuml

   left to right direction
   actor Supervisor

   rectangle "IACT" {
     usecase "UC_RPT_03\nVer reportes\nhistóricos\n.. extension points ..\nresultados listados\nen pantalla"   as RPT03
     usecase "UC_RPT_09\nConfigurar filtros"          as RPT09
     usecase "UC_RPT_10\nGuardar vista"               as RPT10
     usecase "UC_RPT_11\nCompartir reporte"           as RPT11
   }

   Supervisor --> RPT03

   RPT09 ..> RPT03 : <<extend>>\n(resultados listados)
   RPT10 ..> RPT03 : <<extend>>\n(resultados listados)
   RPT11 ..> RPT03 : <<extend>>\n(resultados listados)

   note right of RPT03
     Punto de extensión:
       "resultados listados en pantalla"

     UC_RPT_03 (base) puede ser
     extendido opcionalmente por:
       - UC_RPT_09 (configurar filtros)
       - UC_RPT_10 (guardar vista actual)
       - UC_RPT_11 (compartir vía link)
     Las extensiones son opcionales,
     no obligatorias.
   end note
   @enduml
