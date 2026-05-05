7.1 Ejemplo IACT — cálculo de métrica BR_016 (tasa de abandono)
---------------------------------------------------------------

.. uml::

   @startuml
   allowmixing

   object ":Reporte"      as Reporte
   object ":Calculadora"  as Calculadora
   object ":BDAnalytics"  as BDAnalytics

   Reporte -> Calculadora  : "1: tasaAbandono :=\n   calcular_tasa_abandono(\n   periodo, segmento)"
   Calculadora -> BDAnalytics : "1.1: total :=\n   contar_llamadas(\n   periodo, segmento)"
   Calculadora -> BDAnalytics : "1.2: abandonadas :=\n   contar_llamadas(\n   periodo, segmento,\n   resultado=ABANDONADA)"
   Calculadora -> Reporte  : "1.3: tasaAbandono =\n   abandonadas / total\n   × 100"

   note right of Calculadora
     BR_016 — fórmula:
       (abandonadas / total) × 100
     Filtrado siempre por
     segmento del usuario
     (CNST_008, BR_012).
   end note
   @enduml
