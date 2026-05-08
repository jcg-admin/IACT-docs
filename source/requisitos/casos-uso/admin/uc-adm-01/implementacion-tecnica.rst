.. _uc-adm-01-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- SeparationRuleEndpoint (CRUD + disable + reactivate)
- AuthorizationGuard (requiere AGR-010)
- DisjointSetValidator
- SeparationRuleRepo
- EnforcementEngine.reload()
- AuditService

11.2 Contratos
==============

::

   contract SeparationRuleService:
     create(payload, invoker)
       returns: SeparationRule
     update(id, payload, invoker)
       returns: SeparationRule
     disable(id, invoker)
     reactivate(id, invoker)
     list(filters) -> List[SeparationRule]

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
       rule = SeparationRule(
         name=payload.name,
         group_a=payload.group_a,
         group_b=payload.group_b,
         rationale=payload.rationale,
         state=ACTIVE, version=1)
       SeparationRuleRepo.save(rule)
       AuditService.emit(
         'SEPARATION_RULE_CREATED',
         criticality=HIGH)
       EnforcementEngine.reload()
       return rule

11.4 Stack-agnostico
====================

- EnforcementEngine puede ser in-process
  o servicio separado (pub/sub para reload).
- SeparationRule persiste en BD relacional.
