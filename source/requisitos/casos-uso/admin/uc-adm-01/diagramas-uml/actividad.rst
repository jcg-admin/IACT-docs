8.2 Actividad — Crear regla SoD
================================

.. uml::

 @startuml
 start
 :POST /api/admin/sod-rules/;
 :JWT + verificar AGR-009;
 if (Sin AGR-009?) then (si)
   :403; stop
 endif
 :Validar conjuntos disjuntos;
 if (Interseccion?) then (si)
   :400 conjuntos invalidos; stop
 endif
 :Validar funciones en catalogo;
 if (Funcion inexistente?) then (si)
   :400 funcion invalida; stop
 endif
 :INSERT SoDRule (ACTIVE);
 :Audit SOD_RULE_CREATED;
 :EnforcementEngine.reload();
 :201;
 stop
 @enduml
