3.4 Ejemplo IACT — los tres tipos en UC_RPT_01
----------------------------------------------

.. uml::

   @startuml

   actor Operador
   participant ":Frontend"   as Frontend
   participant ":Backend"    as Backend
   participant ":SecRules"   as SecRules
   participant ":BDAnalytics" as BDAnalytics
   participant ":AuditLog"   as AuditLog

   Operador -> Frontend   : 1. clic "Ver Dashboard"        (simple)
   Frontend -> Backend          : 2. GET /api/dashboard          (sincrónico)
   activate Backend
   Backend -> SecRules         : 3. verificarPermiso(view_dashboard)\n  (sincrónico)
   activate SecRules
   SecRules --> Backend        : 4. autorizado + segmento
   deactivate SecRules
   Backend -> BDAnalytics         : 5. SELECT con filtro segmento  (sincrónico)
   activate BDAnalytics
   BDAnalytics --> Backend        : 6. filas
   deactivate BDAnalytics
   Backend ->> AuditLog        : 7. registrar(VIEW_DASHBOARD)   (asincrónico,\n     CNST_025)
   Backend --> Frontend         : 8. {datos, métricas, ts}
   deactivate Backend
   Frontend --> Operador  : 9. dashboard renderizado
   @enduml
