8.2 Actividad — Crear funcion atomica
======================================

.. uml::

 @startuml
 start
 :POST /api/admin/functions/;
 :JWT + verificar AGR-010;
 if (Sin AGR-010?) then (si)
   :403; stop
 endif
 :Validar codename snake_case;
 if (Formato invalido?) then (si)
   :400; stop
 endif
 :Verificar unicidad codename;
 if (Duplicado?) then (si)
   :409; stop
 endif
 :INSERT Function (is_active=True);
 :Audit FUNCTION_CREATED;
 :PermissionsEngine.reload_catalog();
 :201;
 stop
 @enduml
