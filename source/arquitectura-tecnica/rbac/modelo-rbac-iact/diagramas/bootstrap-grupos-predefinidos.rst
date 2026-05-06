.. meta::
 :artefacto: AT_RBAC_BOOTSTRAP_GRUPOS
 :tipo: Diagrama Arquitectonico — Bootstrap RBAC Groups
 :dominio: arquitectura_tecnica
 :subdominio: rbac/modelo-rbac-iact/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _rbac_bootstrap_grupos:

================================================================
Bootstrap de Grupos Predefinidos (AGR-001..012) — RBAC v5.6.0
================================================================

Cómo se materializan los 12 ``AccessGroup`` del modelo RBAC
v5.6.0 al inicializar el sistema. Cubre la pregunta operativa:
*"¿quién crea los grupos AGR-001..012, cuándo, y con qué
funciones asociadas?"*

Decisión arquitectónica de fondo:
:doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`.

Mapeo canónico AGR → grupo (estado v5.6.0)
==========================================

.. list-table::
 :widths: 12 30 12 12 34
 :header-rows: 1

 * - Código
   - ``AccessGroup.name``
   - Funciones
   - ``is_system``
   - Estado
 * - AGR-001
   - ``basic_operator_group``
   - 4
   - ``True``
   - In-scope (activo)
 * - AGR-002
   - ``report_viewer_group``
   - 8
   - ``True``
   - In-scope (activo)
 * - AGR-003
   - ``quality_supervisor_group``
   - 11
   - ``True``
   - In-scope (activo)
 * - AGR-004
   - ``data_exporter_group``
   - 14
   - ``True``
   - In-scope (activo)
 * - AGR-005
   - ``alert_manager_group``
   - 6
   - ``True``
   - In-scope (activo)
 * - AGR-006
   - ``user_admin_group``
   - 9
   - ``True``
   - In-scope (activo)
 * - AGR-007
   - ``permission_admin_group``
   - 5
   - ``True``
   - In-scope (activo)
 * - AGR-008
   - ``auditor_group``
   - 4
   - ``True``
   - In-scope (activo)
 * - AGR-009
   - ``pipeline_admin_group``
   - 4
   - ``True``
   - In-scope (activo)
 * - AGR-010
   - ``system_admin_group``
   - 6
   - ``True``
   - In-scope (activo) — ``MOD_Admin``
 * - AGR-011
   - ``call_center_operator_group``
   - 10
   - ``True``
   - **RESERVADO** open-closed (``MOD_Operator``)
 * - AGR-012
   - ``call_center_supervisor_group``
   - 3 + AGR-003
   - ``True``
   - **RESERVADO** open-closed (``MOD_Supervision``)

.. note:: Conteos detallados por grupo en
 :doc:`/requisitos/reglas-negocio/rbac/grupos-funciones`.
 La columna "Funciones" puede solaparse con ``Function``
 compartidas entre AGRs (M2M).

Diagrama de actividad: bootstrap automatico via ``migrate``
============================================================

.. uml::
 :caption: Bootstrap de los 12 AGR + 64 Function activas + 3 SoD durante ``python manage.py migrate``.

 @startuml

 |Operador|
 start
 :Ejecuta ``python manage.py migrate``;

 |Django Migrations Engine|
 :Aplica migraciones schema en orden;
 :Ejecuta data migration\n``RunPython(create_default_groups)``;

 |Data Migration|
 partition "Catalogo de Function (64 activas)" {
   :Recorre lista declarada de codenames;
   :Para cada codename ejecuta\n``Function.objects.get_or_create(codename=...)``;
   note right
     Idempotente — no duplica si re-ejecuta
   end note
 }

 partition "12 AccessGroup (system)" {
   :Recorre lista AGR-001..012\ncon (agr_code, name, is_system=True);
   :``AccessGroup.objects.get_or_create(agr_code=...)``\ncon ``defaults={name, is_system: True}``;
   :Asocia ``Function`` correspondientes via\n``group.functions.set(...)``;
 }

 partition "3 reglas SoD" {
   :``FunctionSeparationRule.objects.get_or_create(...)``\ncon pares de grupos mutuamente exclusivos;
 }

 |Django Migrations Engine|
 :Marca migracion como aplicada en\ntabla django_migrations;

 |Operador|
 :Sistema RBAC listo;
 :``createsuperuser`` (asigna AGR-010);
 stop

 @enduml

Diagrama de secuencia: resolucion de permiso en runtime
=======================================================

.. uml::
 :caption: ``user.has_perm("functioncode")`` — flujo de check al ejecutar un endpoint protegido.

 @startuml

 actor User
 participant "DRF View\n(decorator)" as View
 participant "Custom Permission\nBackend" as Backend
 database "AccessGroup\n(M2M con Function)" as DB

 User -> View: HTTP request
 View -> Backend: user.has_perm("view_reports")
 Backend -> Backend: get_all_permissions(user)
 Backend -> DB: user.access_groups.functions
 DB --> Backend: Set[Function]
 Backend -> DB: user.individual_function_assignments
 DB --> Backend: Set[Function] (extras)
 Backend -> Backend: union de codenames
 Backend --> View: bool (permite o no)

 alt permitido
   View --> User: 200 OK + payload
 else denegado
   View --> User: 403 Forbidden
 end

 @enduml

Pseudocodigo del bootstrap (data migration canonica)
====================================================

.. code-block:: python

 # apps/access/migrations/00NN_bootstrap_rbac.py
 from django.db import migrations

 PREDEFINED_GROUPS = [
     ('AGR-001', 'basic_operator_group',        ['view_own_sessions', ...]),
     ('AGR-002', 'report_viewer_group',         ['view_reports', ...]),
     ('AGR-003', 'quality_supervisor_group',    [...]),
     ('AGR-004', 'data_exporter_group',         ['export_csv', ...]),
     ('AGR-005', 'alert_manager_group',         ['view_alerts', ...]),
     ('AGR-006', 'user_admin_group',            ['create_users', ...]),
     ('AGR-007', 'permission_admin_group',      ['assign_functions', ...]),
     ('AGR-008', 'auditor_group',               ['view_audit_log', ...]),
     ('AGR-009', 'pipeline_admin_group',        ['view_pipeline_status', ...]),
     ('AGR-010', 'system_admin_group',          ['create_separation_rule', ...]),
     # RESERVADOS open-closed v5.6.0 — no se ejecutan en esta release:
     # ('AGR-011', 'call_center_operator_group', [...]),
     # ('AGR-012', 'call_center_supervisor_group', [...]),
 ]

 SOD_RULES = [
     ('SOD-001', 'pipeline_audit_separation',
      ['AGR-009'], ['AGR-008']),
     ('SOD-002', 'user_audit_separation',
      ['AGR-006'], ['AGR-008']),
     ('SOD-003', 'access_audit_separation',
      ['AGR-007'], ['AGR-008']),
 ]

 def bootstrap_rbac(apps, schema_editor):
     Function     = apps.get_model('access', 'Function')
     AccessGroup  = apps.get_model('access', 'AccessGroup')
     SoDRule      = apps.get_model('access',
                                   'FunctionSeparationRule')

     for agr_code, group_name, function_codenames in PREDEFINED_GROUPS:
         group, _ = AccessGroup.objects.get_or_create(
             agr_code=agr_code,
             defaults={
                 'name': group_name,
                 'is_system': True,
             },
         )
         functions = Function.objects.filter(
             codename__in=function_codenames,
         )
         group.functions.set(functions)

     for sod_code, sod_name, group_a, group_b in SOD_RULES:
         SoDRule.objects.get_or_create(
             code=sod_code,
             defaults={
                 'name': sod_name,
                 'group_a_codes': group_a,
                 'group_b_codes': group_b,
             },
         )

 class Migration(migrations.Migration):
     dependencies = [
         ('access', '00NN-1_initial_schema'),
     ]
     operations = [
         migrations.RunPython(
             bootstrap_rbac,
             migrations.RunPython.noop,
         ),
     ]

Custom groups (``is_system=False``)
====================================

Los grupos creados por administradores en runtime via UC_PERM_05
NO se bootstrap aquí — se crean dinámicamente con
``is_system=False``. Esto permite:

- AGR-001..012 son **inmutables** (regla del sistema).
- Custom groups son editables / eliminables por
  ``permission_admin`` (AGR-007).
- ``django.admin`` puede mostrar ambos pero **filtrar
  ``is_system=True``** del set de grupos editables.

Ver :doc:`/requisitos/casos-uso/permissions/uc-perm-05/index`
para el caso de uso de creación de custom groups.

Reglas SoD (Separation of Duties)
=================================

.. list-table::
 :widths: 15 30 25 30
 :header-rows: 1

 * - Código
   - Nombre
   - Grupo A
   - Grupo B (mutuamente excluyente)
 * - SOD-001
   - ``pipeline_audit_separation``
   - AGR-009 (``pipeline_admin_group``)
   - AGR-008 (``auditor_group``)
 * - SOD-002
   - ``user_audit_separation``
   - AGR-006 (``user_admin_group``)
   - AGR-008 (``auditor_group``)
 * - SOD-003
   - ``access_audit_separation``
   - AGR-007 (``permission_admin_group``)
   - AGR-008 (``auditor_group``)

**Patrón:** todas las reglas v5.6.0 separan ``auditor_group``
(AGR-008) de roles administrativos. Esto previene que un
admin audite sus propias acciones — base teórica de SoD.

Ver :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod`
para la formalización SBVR.

Trazabilidad
============

- ADR de la decisión: :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`.
- Modelo de datos: :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/modelo-datos`.
- Diagrama de clases entidades: :doc:`clases-entidades-rbac`.
- Flujo enforcement runtime: :doc:`flujo-enforcement-rbac`.
- Implementación detalle: :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/implementacion`.
- Catálogo funciones: :doc:`/requisitos/reglas-negocio/rbac/catalogo-funciones`.
- Especificación grupos: :doc:`/requisitos/reglas-negocio/rbac/grupos-funciones`.
- SoD: :doc:`/requisitos/reglas-negocio/rbac/sod`.
- Vista UC del módulo Admin: :doc:`/arquitectura-tecnica/use-case-view/admin/index`.
