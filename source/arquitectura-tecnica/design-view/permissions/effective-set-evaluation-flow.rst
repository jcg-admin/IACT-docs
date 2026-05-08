.. meta::
 :artefacto: AT_DESIGN_ACT_RBAC_EVAL
 :tipo: Diagrama Arquitectonico — Design View — Activity
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :flujo: rbac-effective-set-eval
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_design_act_rbac_effective_set_eval:

============================================================
Design View — Flujo: Evaluacion del Effective Set RBAC
============================================================

Flujo del calculo del **effective set** de funciones RBAC para
un usuario. Es el flujo invocado en CADA verificacion de permiso
del sistema. Combina assignments del catalogo, permisos
excepcionales, y aplica TTL del cache.

Cubre los UCs UC_PERM_07 (verificar permiso), UC_PERM_03
(conceder permiso excepcional), y todos los gateway checks de
otros modulos.

.. uml::
 :caption: Flujo evaluacion effective_set — desde verify hasta grant/deny.

 @startuml

 start
 :Recibir verify(user, function);

 if (Session activa?) then (no)
   :Retornar 401 unauthorized;
   stop
 else (si)
 endif

 :Consultar PermissionCache(user);
 if (cache hit?) then (si)
   :effective_set = cache;
 else (no)
   :Consultar Assignments del catalogo;
   :effective_set = UNION(grupos.funciones);

   :Consultar ExceptionalPermissionRepo(user);
   :grants = filter(state=ACTIVE, type=GRANT);
   :revokes = filter(state=ACTIVE, type=REVOKE);

   :effective_set = effective_set + grants - revokes;

   :Aplicar EvaluadorReloader si rules cambiaron;

   :Persistir en PermissionCache con TTL;
 endif

 if (function in effective_set?) then (si)
   :Emitir AuditEvent(result=grant);
   :Retornar grant;
 else (no)
   :Emitir AuditEvent(result=deny);
   :Retornar deny;
 endif

 stop

 @enduml

----

Notas de diseno
================

- **CNST-001**: cada verify produce AuditEvent (trazabilidad).
- **P-15**: la unidad de verificacion es la funcion RBAC, no el grupo.
- **TTL del cache**: configurado por ExpirationPolicy.
- **Re-load incremental**: si EvaluatorReloader detecta cambio en
  el catalogo (assignments o exceptional permissions), invalida
  cache para los usuarios afectados.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/permissions/interaction-pattern`
 - :doc:`/arquitectura-tecnica/design-view/permissions/bounded-context`
 - :doc:`/arquitectura-tecnica/use-case-view/permissions/uc-perm-07-verificar-permiso-de-usuario`
 - :doc:`/arquitectura-tecnica/domain-model/permission-service`
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator`
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache`
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo`
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`
