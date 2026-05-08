.. _uc-adm-01-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Crear regla SoD
============================================

.. uml::
 :caption: UC_ADM_01 — flujo de creacion de SeparationRule.

 @startuml

 start
 :Invoker emite POST /api/v1/admin/separation-rules/;
 :Servicio de Aplicacion verifica capability
   create_separation_rule (AGR-010);
 if (Capability presente?) then (no)
   :403 Forbidden;
   :Audit CAPABILITY_DENIED;
   stop
 endif

 :Validar conjuntos group_a y group_b disjuntos
   (CNST-030);
 if (Interseccion encontrada?) then (si)
   :400 conjuntos invalidos;
   stop
 endif

 :Validar Functions referenciadas existen y
   estan activas (FunctionRepo);
 if (Function inexistente / inactiva?) then (si)
   :422 funcion invalida;
   stop
 endif

 :Validar nombre unico
   (no existe SeparationRule con mismo name);
 if (Nombre duplicado?) then (si)
   :409 Conflict;
   stop
 endif

 :BEGIN TRANSACTION;
 :INSERT SeparationRule (state=ACTIVE, version=1);
 :Audit SOD_RULE_CREATED
   (actor=invoker, snapshot del rule);
 :COMMIT;

 :EvaluatorReloader.reload()
   (post-COMMIT, hot reload del catalogo SoD);
 if (Reload OK?) then (no)
   :Log + telemetria
   (degraded — operaciones siguen
    funcionando con catalogo previo);
 endif

 :201 Created con SeparationRule;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones`.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule`.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`.
