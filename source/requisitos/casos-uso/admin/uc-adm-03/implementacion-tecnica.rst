.. _uc-adm-03-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- SystemGroupEndpoint (GET, POST function, DELETE function, GET impact)
- AuthorizationGuard (requiere AGR-010)
- SystemGroupGuard (verifica is_system=True)
- SeparationPreCheckValidator (valida contra reglas activas)
- FunctionGroupRepo
- PermissionsEngine.recalculate(agr_id)
- AuditService

11.2 Contratos
==============

::

   contract SystemGroupService:
     add_function(group_id, codename, invoker)
       returns: FunctionGroup
     remove_function(group_id, codename, invoker)
     get_composition(group_id)
       returns: FunctionGroup
     get_impact(group_id, codename, operation)
       returns: ImpactReport

11.3 Pseudocodigo
=================

::

   procedure add_function(group_id, codename, invoker):
       require AuthorizationGuard.has_agr(
                 invoker, 'AGR-010')
       group = FunctionGroupRepo.get(group_id)
       require group.is_system == True
       fn = FunctionRepo.get_active(codename)
       SeparationPreCheckValidator.validate(
         group, fn)
       FunctionGroupRepo.add_function(
         group, fn)
       AuditService.emit(
         'AGR_FUNCTION_ADDED',
         criticality=HIGH)
       PermissionsEngine.recalculate(group_id)
       return group

11.4 Stack-agnostico
====================

- PermissionsEngine.recalculate puede ser
  sincrono (grupos pequenos) o asincrono
  (grupos con mas de 100 usuarios, via task queue).
