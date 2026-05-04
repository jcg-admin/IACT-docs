.. _uc-adm-02-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- FunctionEndpoint (CRUD + deactivate + list)
- AuthorizationGuard (requiere AGR-009)
- FunctionValidator (codename format, uniqueness)
- FunctionRepo
- PermissionsEngine.reload_catalog()
- AuditService

11.2 Contratos
==============

::

   contract FunctionCatalogService:
     create(payload, invoker)
       returns: Function
     update(id, payload, invoker)
       returns: Function
     deactivate(id, invoker)
     list(module?, is_active?) -> List[Function]

11.3 Pseudocodigo
=================

::

   procedure create(payload, invoker):
       require AuthorizationGuard.has_agr(
                 invoker, 'AGR-009')
       FunctionValidator.validate_codename(
         payload.codename)
       FunctionValidator.unique(
         payload.codename)
       fn = Function(
         codename=payload.codename,
         description=payload.description,
         module=payload.module,
         scope=payload.scope,
         is_active=True)
       FunctionRepo.save(fn)
       AuditService.emit(
         'FUNCTION_CREATED',
         criticality=HIGH)
       PermissionsEngine.reload_catalog()
       return fn

11.4 Stack-agnostico
====================

- FunctionRepo puede ser ORM Django o
  repositorio abstracto.
- PermissionsEngine recibe hook de
  invalidacion de cache.
