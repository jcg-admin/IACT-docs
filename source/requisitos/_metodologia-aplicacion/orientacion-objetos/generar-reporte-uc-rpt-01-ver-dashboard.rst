6.1 Generar reporte — UC_RPT_01 (ver dashboard)
-----------------------------------------------

.. uml::

   @startuml

   participant ":Operador"   as Operador
   participant ":Dashboard"  as Dashboard
   participant ":Reporte"    as Reporte
   participant ":SecRules"   as SecRules
   participant ":BDAnalytics" as BDAnalytics

   Operador  -> Dashboard  : 1. abrirDashboard()
   Dashboard  -> Reporte  : 2. generar(filtros)
   Reporte  -> SecRules : 3. verificarPermiso(view_dashboard)
   SecRules --> Reporte : 4. autorizado + segmento del usuario
   Reporte  -> BDAnalytics : 5. SELECT con filtro de segmento
   BDAnalytics --> Reporte : 6. filas
   Reporte  --> Dashboard : 7. resultados
   Dashboard  --> Operador : 8. dashboard renderizado
   @enduml
