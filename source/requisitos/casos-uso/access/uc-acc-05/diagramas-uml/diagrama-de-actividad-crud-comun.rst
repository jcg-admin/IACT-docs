8.3 Diagrama de actividad (CRUD comun)
======================================

.. uml::
 :caption: UC_ACC_05 — actividad de operacion CRUD generica

 @startuml

 start

 :Request CRUD recibido;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (RBAC apropiado para operacion?) then (no)
   :403;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (Validar payload + recursos?) then (no)
   :400 / 404 / 409; stop
 else (si)
 endif

 :Iniciar transaccion atomica;
 :Aplicar operacion (registrar, actualizar, o
  actualizar state=RETIRED segun caso);
 :registrar AuditEvent SOD_RULE_X;
 :Commit transaccion;

 if (Transaccion OK?) then (no)
   :ROLLBACK; :500/503;
   stop
 else (si)
 endif

 :SoDRuleCache.invalidate (post-COMMIT);
 :200 / 201;

 stop

 @enduml

Cada sub-flujo (LISTAR, CREAR, MODIFICAR,
RETIRAR) sigue este esqueleto comun. Las
validaciones especificas por operacion estan
en Parte 5 — Excepciones.

