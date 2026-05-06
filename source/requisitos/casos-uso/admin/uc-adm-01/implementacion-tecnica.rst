.. _uc-adm-01-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- SoDRuleEndpoint (CRUD + disable + reactivate)
- AuthorizationGuard (requiere AGR-010)
- DisjointSetValidator
- SoDRuleRepo
- EnforcementEngine.reload()
- AuditService

11.2 Contratos
==============

::

   contract SoDRuleService:
     create(payload, invoker)
       returns: SoDRule
     update(id, payload, invoker)
       returns: SoDRule
     disable(id, invoker)
     reactivate(id, invoker)
     list(filters) -> List[SoDRule]

11.3 Pseudocodigo
=================

::

   procedure create(payload, invoker):
       require AuthorizationGuard.has_agr(
                 invoker, 'AGR-010')
       DisjointSetValidator.validate(
         payload.group_a, payload.group_b)
       FunctionValidator.all_exist(
         payload.group_a + payload.group_b)
       rule = SoDRule(
         name=payload.name,
         group_a=payload.group_a,
         group_b=payload.group_b,
         rationale=payload.rationale,
         state=ACTIVE, version=1)
       SoDRuleRepo.save(rule)
       AuditService.emit(
         'SOD_RULE_CREATED',
         criticality=HIGH)
       EnforcementEngine.reload()
       return rule

11.4 Stack-agnostico
====================

- EnforcementEngine puede ser in-process
  o servicio separado (pub/sub para reload).
- SoDRule persiste en BD relacional.
