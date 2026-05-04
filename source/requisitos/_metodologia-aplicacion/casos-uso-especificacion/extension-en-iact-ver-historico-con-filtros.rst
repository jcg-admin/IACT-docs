6.1 Extensión en IACT — Ver histórico con filtros
-------------------------------------------------

Caso base: ``UC_RPT_03`` (Ver reportes históricos).
Extensión: ``UC_RPT_09`` (Configurar filtros) — opcional para
acotar el conjunto de filas.

.. uml::

   @startuml

   left to right direction
   actor Supervisor

   rectangle "IACT" {
     usecase "UC_RPT_03\nVer reportes\nhistóricos\n(BASE)"           as RPT03
     usecase "UC_RPT_09\nConfigurar\nfiltros\n(EXTIENDE)"            as RPT09
     usecase "UC_RPT_10\nGuardar vista\n(EXTIENDE)"                  as RPT10
     usecase "UC_RPT_11\nCompartir reporte\n(EXTIENDE)"              as RPT11
   }

   Supervisor --> RPT03
   RPT09 ..> RPT03 : <<extend>>
   RPT10 ..> RPT03 : <<extend>>
   RPT11 ..> RPT03 : <<extend>>
   @enduml

::

 UC_RPT_03 (Ver reportes históricos) — base
   1. Supervisor abre histórico
   2. Sistema valida permiso
   3. Sistema lista reportes filtrados
      por segmento del usuario
   4. Sistema muestra resultados

 UC_RPT_09 (Configurar filtros) — extensión
   Punto de extensión: paso 3
   Pasos adicionales:
     3a1. Supervisor agrega filtros
          (fecha / centro / campaña)
     3a2. Sistema aplica filtros junto
          con BR_012 (segmento)
     3a3. Sistema actualiza resultados
