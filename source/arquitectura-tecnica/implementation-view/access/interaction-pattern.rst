.. meta::
 :artefacto: AT_IMPL_SEQ_ACCESS
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_access:

============================================================
Implementation View — MOD_Access: Patron de Interaccion
============================================================

Secuencia de llamadas reales entre las capas Django/DRF para
el flujo de asignacion de ``FunctionGroup`` a un usuario, con
verificacion previa de SoD (Separation of Duties).

A diferencia de
:doc:`/arquitectura-tecnica/design-view/access/interaction-pattern`
(actores de dominio, abstracciones), este diagrama nombra
**clases y metodos reales** del codigo Django: views DRF,
serializers, services y repositories.

.. uml::
 :caption: MOD_Access impl seq — assign POST → SoD check → ORM persist + audit.

 @startuml

 actor PipelineAdmin
 participant "AssignmentView\n(APIView)" as View <<api>>
 participant "AssignmentSerializer\n(ModelSerializer)" as Serializer <<serializer>>
 participant "AccessService" as Service <<service>>
 participant "SeparationRuleRepository" as SRRepo <<repository>>
 participant "AssignmentRepository" as ARepo <<repository>>
 participant "AssignmentORM\n(Django Model)" as ORM <<orm>>
 participant "AuditService" as Audit <<service>>
 database PostgreSQL

 PipelineAdmin -> View : POST /api/v1/access/assignments/\n{user_id, group_ref}
 activate View

 View -> View : permission_classes\n[HasAssignFunctionsPerm]
 note right
   DRF permission class —
   resuelve via PermissionsService
   sin tocar BD por request.
 end note

 View -> Serializer : .is_valid(raise_exception=True)
 activate Serializer
 Serializer --> View : validated_data
 deactivate Serializer

 View -> Service : assign(user_id, group_ref, actor=request.user)
 activate Service

 Service -> SRRepo : check_conflict(user_id, group_ref)
 activate SRRepo
 SRRepo -> ORM : SeparationRuleORM.objects.\nfilter(group__in=[...]).exists()
 ORM -> PostgreSQL : SELECT 1 FROM separation_rule ...
 PostgreSQL --> ORM
 ORM --> SRRepo : QuerySet
 SRRepo --> Service : SoDResult(ok|conflict)
 deactivate SRRepo

 alt conflict detected
   Service --> View : raise SoDViolationError
   View --> PipelineAdmin : HTTP 422 + error_code=\nSEPARATION_VIOLATION
 else no conflict
   Service -> ARepo : create(user_id, group_ref, actor)
   activate ARepo
   ARepo -> ORM : AssignmentORM.objects.create(...)
   ORM -> PostgreSQL : INSERT INTO assignment ...
   PostgreSQL --> ORM : id
   ORM --> ARepo : Assignment
   ARepo --> Service : Assignment
   deactivate ARepo

   Service -> Audit : record(\nACCESS_CHANGE, actor, target=user_id)
   activate Audit
   Audit -> ORM : AuditEventORM.objects.create(...)
   ORM -> PostgreSQL : INSERT INTO audit_event ...
   deactivate Audit

   Service --> View : Assignment
 end

 View -> Serializer : .to_representation(instance)
 Serializer --> View : dict
 View --> PipelineAdmin : HTTP 201 + body
 deactivate View

 @enduml

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Capa
   - Archivo
 * - View
   - ``apps/access/api/views.py: AssignmentView``
 * - Serializer
   - ``apps/access/api/serializers.py: AssignmentSerializer``
 * - Service
   - ``apps/access/services/access_service.py: AccessService``
 * - Repository
   - ``apps/access/repositories/assignment_repo.py``
     ``apps/access/repositories/separation_rule_repo.py``
 * - ORM
   - ``apps/access/models.py:
     AssignmentORM, SeparationRuleORM``
 * - Audit
   - ``apps/audit/services/audit_service.py: AuditService``
     (cross-modulo)

Invariantes de implementacion
==============================

- **I-IMPL-ACC-01:** la verificacion SoD ejecuta **antes** de
  ``ARepo.create``. Si la verificacion falla, no hay write a
  ``assignment`` ni a ``audit_event``.
- **I-IMPL-ACC-02:** ``AccessService.assign`` se ejecuta dentro
  de un ``transaction.atomic()`` — INSERT de assignment +
  audit forman una unica transaccion.
- **I-IMPL-ACC-03:** la permission class del view se resuelve
  con cache en memoria (``PermissionsService``); no hace
  query por request.

----

.. seealso::

 - :doc:`layer-structure` — vista de paquetes/componentes.
 - :doc:`rbac-enforcement-pattern` — patron de enforcement
   transversal a todas las views DRF.
 - :doc:`/arquitectura-tecnica/design-view/access/interaction-pattern` —
   secuencia equivalente en DesignView (dominio).
