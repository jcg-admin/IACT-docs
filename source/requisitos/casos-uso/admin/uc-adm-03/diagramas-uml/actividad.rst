8.2 Actividad — Agregar funcion a AGR sistema
==============================================

.. uml::

 @startuml
 start
 :POST /api/admin/system-groups/{id}/functions/;
 :JWT + verificar AGR-009;
 if (Sin AGR-009?) then (si)
   :403; stop
 endif
 :Verificar is_system=True;
 if (No es sistema?) then (si)
   :403 usar UC_PERM_06; stop
 endif
 :Verificar funcion en catalogo activo;
 if (No existe?) then (si)
   :400; stop
 endif
 :Verificar SoD precheck;
 if (Conflicto SoD?) then (si)
   :400 + detalle regla; stop
 endif
 :INSERT GroupFunction;
 :Audit AGR_FUNCTION_ADDED;
 :PermissionsEngine.recalculate(group_id);
 :201;
 stop
 @enduml
