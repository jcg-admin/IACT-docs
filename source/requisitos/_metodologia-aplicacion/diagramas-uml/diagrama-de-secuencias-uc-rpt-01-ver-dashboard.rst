5. Diagrama de secuencias — UC_RPT_01 (ver dashboard)
=====================================================

.. uml::

   @startuml

   actor Operador
   participant ":Frontend\n(React)"   as Frontend
   participant ":Backend\n(Django)"   as Backend
   participant ":SecRules"            as SecRules
   participant ":AuditLog"            as AuditLog
   participant ":BD Analytics"        as BdAnalytics

   Operador -> Frontend  : 1. Click "Ver Dashboard"
   Frontend -> Backend         : 2. GET /api/reports/dashboard

   Backend -> SecRules        : 3. verificarPermiso(view_dashboard)

   alt Permiso aprobado
     SecRules --> Backend     : 4a. autorizado + segmento
     Backend -> AuditLog      : 5. registrar(VIEW_DASHBOARD)
     Backend -> BdAnalytics      : 6. SELECT con filtro de segmento
     BdAnalytics --> Backend     : 7. filas
     Backend --> Frontend      : 8. {datos, métricas, ts}
     Frontend --> Operador : 9. dashboard renderizado
   else Permiso denegado
     SecRules --> Backend     : 4b. denegado
     Backend -> AuditLog      : 5. registrar(VIEW_DASHBOARD_DENIED)
     Backend --> Frontend      : 6. {error: 403}
     Frontend --> Operador : 7. ✗ "Sin permiso"
   end
   @enduml

**Aplicación:** DOC-25 (Secuencias críticas).

----
