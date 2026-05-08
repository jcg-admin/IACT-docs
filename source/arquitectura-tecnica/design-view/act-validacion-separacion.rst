.. meta::
 :artefacto: AT_DESIGN_ACT_SEPARATION_CHECK
 :tipo: Diagrama Arquitectonico — Design View — Activity
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :flujo: separation-check
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_design_act_sod_check:

============================================================
Design View — Flujo: Verificacion Separation of Duties
============================================================

Flujo de verificacion de separacion (CNST-005) que se invoca antes de
crear o modificar cualquier ``Assignment``. Compara las
funciones que el usuario tendria post-asignacion contra todas
las ``SeparationRule`` activas.

Cubre los UCs UC_ACC_01 (asignar grupo), UC_ACC_03 (revocar
grupo), UC_PERM_03 (conceder permiso excepcional).

.. uml::
 :caption: Flujo separation check — antes de cualquier mutacion RBAC.

 @startuml

 start
 :Recibir check_separation(user_id, group_ref);

 :Consultar Assignments existentes(user_id);
 :existing_functions = UNION(grupos.funciones);

 :Consultar nuevas funciones (group_ref);
 :new_functions = group_ref.funciones;

 :Consultar ExceptionalPermissions(user_id);
 :exceptional_grants = filter(state=ACTIVE, type=GRANT);

 :total_set = existing_functions
              + new_functions
              + exceptional_grants;

 :Consultar SeparationRuleRepo.list_active();
 :rules = List<SeparationRule>;

 while (mas rules?) is (si)
   :rule = next();
   :Aplicar rule.evaluate(total_set);
   if (conjuntoA y conjuntoB ambos en total_set?) then (si)
     :violations.add(rule);
   endif
 endwhile (no)

 if (violations vacio?) then (si)
   :Retornar sod_ok=true;
 else (no)
   :Emitir AuditEvent(type=sod_violation_attempted,
   rules=violations);
   :Retornar sod_ok=false, violations=...;
 endif

 stop

 @enduml

----

Notas de diseno
================

- **CNST-005**: separacion se evalua sobre **funciones**, no sobre
  grupos. Dos grupos distintos pueden compartir funciones — la
  union es lo que cuenta.
- **Assignments + Exceptional Grants**: ambos se consideran en
  total_set; el separation check ve la realidad efectiva post-mutacion.
- **No revokes**: los exceptional revokes no afectan el check
  porque solo restringen, no expanden.
- **Audit en violacion**: cada intento bloqueado deja trazabilidad.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/seq-access`
 - :doc:`/arquitectura-tecnica/design-view/class-access`
 - :doc:`/arquitectura-tecnica/use-case-view/access/uc-acc-01-asignar-funciones`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule`
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo`
 - :doc:`/arquitectura-tecnica/domain-model/assignment`
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission`
