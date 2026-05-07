.. meta::
 :artefacto: BACK_RBAC_IMPLEMENTATION_GUIDE
 :tipo: Guia de Implementacion
 :dominio: backend
 :subdominio: rbac
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _back-rbac-implementation-guide:

============================================================
Guía de Implementación RBAC — Django + DRF (Findings Q1-Q8)
============================================================

Mapea los hallazgos del WP-5 (research AGR-NNN vs Django) a
**código Django/DRF concreto**. Cada sección referencia el
finding original, cita la documentación oficial y muestra el
patrón de implementación canónico para IACT.

**Decisión arquitectónica raíz:** ADR-BACK-007 (mantener
modelo custom + fixes idiomáticos). Esta guía aterriza esa
decisión a archivos, código y tests.

**Origen del research:** WP
``2026-05-06-19-27-21-agr-django-permission-groups-research``,
con hallazgos verbatim en ``research/raw/Q1..Q8.md``.

----

Estructura de archivos del backend
==================================

::

   apps/access/
   ├── __init__.py
   ├── apps.py
   ├── models.py                          # Function, AccessGroup, FunctionSeparationRule, ...
   ├── managers.py                        # AccessGroupManager con queryset.system() / .custom()
   ├── permissions.py                     # FunctionAuthBackend + DRF FunctionPermission
   ├── signals.py                         # SoD enforcement en pre_save
   ├── admin.py                           # ModelAdmin con is_system protection
   ├── migrations/
   │   ├── 0001_initial.py                # schema (AutoFields + indexes)
   │   └── 0002_bootstrap_rbac.py         # RunPython data migration (Q2)
   ├── management/commands/
   │   └── initialize_permissions.py      # convenience wrapper (delega en migration)
   └── tests/
       ├── test_models.py
       ├── test_bootstrap_migration.py
       ├── test_permission_backend.py
       ├── test_sod_enforcement.py
       └── test_drf_integration.py

----

Q1 — Modelos: ``Function`` y ``AccessGroup`` custom
====================================================

**Finding (verbatim):**

   *"Django's Group models are a generic way of categorizing
   users so you can apply permissions, or some other label, to
   those users."*
   — `django.contrib.auth docs
   <https://docs.djangoproject.com/en/6.0/ref/contrib/auth/>`_.

**Decisión IACT:** modelo custom independiente (ADR-BACK-007).

**Implementación — ``apps/access/models.py``:**

.. code-block:: python

 from django.db import models
 from django.contrib.auth import get_user_model

 User = get_user_model()


 class Function(models.Model):
     """Permiso atómico — análogo a auth.Permission.

     Naming verbatim de Django (Q6): codename en snake_case con
     verbo imperativo. Ej: 'view_reports', 'export_csv'.
     """

     codename = models.CharField(max_length=100, unique=True)
     name = models.CharField(max_length=255)
     module = models.CharField(max_length=10)  # AUTH, USR, ACC, ...
     description = models.TextField(blank=True)
     is_active = models.BooleanField(default=True)

     class Meta:
         db_table = "functions"
         ordering = ("module", "codename")
         indexes = [
             models.Index(fields=("module",)),
             models.Index(fields=("is_active",)),
         ]

     def __str__(self) -> str:
         return self.codename


 class AccessGroup(models.Model):
     """Grupo de funciones — análogo a auth.Group.

     Diferencias con auth.Group (justificadas en ADR-BACK-007):
     - agr_code: natural key estable (AGR-001..012).
     - is_system: enforcement de inmutabilidad (predefinidos).
     - profile_description: metadata extendido.
     """

     agr_code = models.CharField(
         max_length=10,
         unique=True,
         help_text="AGR-001..012 (system) o AGR-CUSTOM-NNNN",
     )
     name = models.CharField(max_length=100, unique=True)
     profile_description = models.TextField(blank=True)
     is_system = models.BooleanField(
         default=False,
         help_text="True para AGR-001..012 (no editables)",
     )
     functions = models.ManyToManyField(
         Function,
         through="FunctionGroupMembership",
         related_name="access_groups",
     )
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
         db_table = "access_groups"
         ordering = ("agr_code",)
         indexes = [models.Index(fields=("is_system",))]

     def __str__(self) -> str:
         return f"{self.agr_code}: {self.name}"


 class FunctionGroupMembership(models.Model):
     """M2M tabla intermedia (permite metadata futura)."""

     group = models.ForeignKey(AccessGroup, on_delete=models.CASCADE)
     function = models.ForeignKey(Function, on_delete=models.CASCADE)
     assigned_at = models.DateTimeField(auto_now_add=True)

     class Meta:
         db_table = "function_group_membership"
         unique_together = ("group", "function")


 class UserAccessGroupAssignment(models.Model):
     """Asignación de grupo a usuario (con expiración opcional)."""

     user = models.ForeignKey(User, on_delete=models.CASCADE)
     access_group = models.ForeignKey(AccessGroup, on_delete=models.PROTECT)
     assigned_at = models.DateTimeField(auto_now_add=True)
     expires_at = models.DateTimeField(null=True, blank=True)
     assigned_by = models.ForeignKey(
         User, on_delete=models.PROTECT,
         related_name="assignments_made",
     )

     class Meta:
         db_table = "user_function_group_assignments"
         indexes = [
             models.Index(fields=("user", "access_group")),
             models.Index(fields=("expires_at",)),
         ]


 class FunctionSeparationRule(models.Model):
     """Regla SoD — pares de grupos mutuamente exclusivos.

     Custom porque Django no provee SoD nativo (Q7).
     """

     code = models.CharField(max_length=10, unique=True)  # SOD-001..
     name = models.CharField(max_length=100)
     description = models.TextField()
     groups_a = models.ManyToManyField(
         AccessGroup, related_name="sod_rules_as_a",
     )
     groups_b = models.ManyToManyField(
         AccessGroup, related_name="sod_rules_as_b",
     )
     is_active = models.BooleanField(default=True)

     class Meta:
         db_table = "function_separation_rules"

     def __str__(self) -> str:
         return f"{self.code}: {self.name}"

----

Q2 — Bootstrap: data migration con ``RunPython``
=================================================

**Finding (verbatim):**

   *"RunPython is generally the operation you would use to
   create data migrations, run custom data updates and
   alterations."*
   — `Migration Operations
   <https://docs.djangoproject.com/en/5.0/ref/migration-operations/>`_.

**Implementación — ``apps/access/migrations/0002_bootstrap_rbac.py``:**

.. code-block:: python

 # apps/access/migrations/0002_bootstrap_rbac.py
 from django.db import migrations

 # Tuplas: (codename, name, module, description)
 PREDEFINED_FUNCTIONS = [
     # MOD_Auth (4)
     ("view_own_sessions", "Ver sesiones propias", "AUTH", "..."),
     ("close_user_session", "Cerrar sesión", "AUTH", "..."),
     ("reset_password", "Reset contraseña", "AUTH", "..."),
     ("view_all_active_sessions", "Ver sesiones del sistema", "AUTH", "..."),
     # MOD_Users (9), MOD_Access (12), ... — total 64 in-scope
     # ...
 ]

 # Tuplas: (agr_code, name, profile_description, function_codenames)
 PREDEFINED_GROUPS = [
     ("AGR-001", "basic_operator_group",
      "Operador básico — operación diaria",
      ["view_own_sessions", "view_reports", "..."]),
     ("AGR-007", "permission_admin_group",
      "Admin de permisos — asigna funciones a usuarios",
      ["assign_functions", "revoke_functions", "..."]),
     ("AGR-008", "auditor_group",
      "Auditor — solo lectura de eventos inmutables",
      ["view_audit_log", "search_audit_log", "..."]),
     ("AGR-010", "system_admin_group",
      "System admin — gestiona el catálogo del modelo RBAC",
      ["create_separation_rule", "manage_function_catalog",
       "assign_functions_to_group"]),
     # ... 10 grupos in-scope
     # AGR-011 y AGR-012 RESERVADOS open-closed v5.6.0:
     # NO se ejecutan en esta release. Documentados pero comentados.
 ]

 # Tuplas: (code, name, description, group_a_codes, group_b_codes)
 SOD_RULES = [
     ("SOD-001", "pipeline_audit_separation",
      "Pipeline admin no puede ser auditor",
      ["AGR-009"], ["AGR-008"]),
     ("SOD-002", "user_audit_separation",
      "User admin no puede ser auditor",
      ["AGR-006"], ["AGR-008"]),
     ("SOD-003", "access_audit_separation",
      "Permission admin no puede ser auditor",
      ["AGR-007"], ["AGR-008"]),
 ]


 def bootstrap_rbac(apps, schema_editor):
     """Idempotente: get_or_create no duplica."""
     Function    = apps.get_model("access", "Function")
     AccessGroup = apps.get_model("access", "AccessGroup")
     SoDRule     = apps.get_model("access", "FunctionSeparationRule")

     # 1. Function (64 in-scope)
     for codename, name, module, desc in PREDEFINED_FUNCTIONS:
         Function.objects.get_or_create(
             codename=codename,
             defaults={
                 "name": name,
                 "module": module,
                 "description": desc,
             },
         )

     # 2. AccessGroup (10 in-scope; AGR-011/012 reservados)
     for agr_code, name, desc, function_codenames in PREDEFINED_GROUPS:
         group, _ = AccessGroup.objects.get_or_create(
             agr_code=agr_code,
             defaults={
                 "name": name,
                 "profile_description": desc,
                 "is_system": True,
             },
         )
         functions = Function.objects.filter(
             codename__in=function_codenames,
         )
         group.functions.set(functions)

     # 3. SoD rules (3)
     for code, name, desc, codes_a, codes_b in SOD_RULES:
         rule, _ = SoDRule.objects.get_or_create(
             code=code,
             defaults={
                 "name": name,
                 "description": desc,
                 "is_active": True,
             },
         )
         rule.groups_a.set(
             AccessGroup.objects.filter(agr_code__in=codes_a)
         )
         rule.groups_b.set(
             AccessGroup.objects.filter(agr_code__in=codes_b)
         )


 def reverse_bootstrap(apps, schema_editor):
     """Reverse: borrar SoD + groups + functions creados aquí.

     Solo borra is_system=True para preservar custom groups.
     """
     SoDRule     = apps.get_model("access", "FunctionSeparationRule")
     AccessGroup = apps.get_model("access", "AccessGroup")
     Function    = apps.get_model("access", "Function")

     SoDRule.objects.filter(
         code__in=[code for code, *_ in SOD_RULES],
     ).delete()
     AccessGroup.objects.filter(is_system=True).delete()
     Function.objects.filter(
         codename__in=[c for c, *_ in PREDEFINED_FUNCTIONS],
     ).delete()


 class Migration(migrations.Migration):
     dependencies = [("access", "0001_initial")]
     operations = [
         migrations.RunPython(bootstrap_rbac, reverse_bootstrap),
     ]

----

Q3 — Inmutabilidad: ``is_system=True`` enforcement
===================================================

**Finding (verbatim de Q3):**

   *"For Django's Group model specifically, using primary keys
   to reference objects in fixtures is not always a good idea
   ... a natural key for the group can be its name since two
   groups can't have the same name."*

**Decisión IACT:** ``agr_code`` (AGR-001..012) como natural key
+ ``is_system=True`` para enforcement programático.

**Implementación — ``apps/access/admin.py``:**

.. code-block:: python

 from django.contrib import admin
 from django.utils.translation import gettext_lazy as _

 from .models import AccessGroup, Function, FunctionSeparationRule


 @admin.register(AccessGroup)
 class AccessGroupAdmin(admin.ModelAdmin):
     list_display = ("agr_code", "name", "is_system", "created_at")
     list_filter = ("is_system",)
     search_fields = ("agr_code", "name")
     readonly_fields_system = ("agr_code", "is_system")

     def has_delete_permission(self, request, obj=None):
         """Predefinidos NO se borran via admin."""
         if obj and obj.is_system:
             return False
         return super().has_delete_permission(request, obj)

     def get_readonly_fields(self, request, obj=None):
         """Predefinidos: agr_code e is_system NO editables."""
         if obj and obj.is_system:
             return self.readonly_fields_system
         return ()

----

Q4 — DRF Integration: custom permission backend
================================================

**Finding (verbatim de Q4):**

   *"DjangoModelPermissions ties into Django's standard
   django.contrib.auth model permissions."*
   — `DRF Permissions
   <https://www.django-rest-framework.org/api-guide/permissions/>`_.

**Decisión IACT:** custom permission backend que usa ``Function``
en lugar de ``auth.Permission``. Compatible con
``user.has_perm()`` para mantener API DRF estándar.

**Implementación — ``apps/access/permissions.py``:**

.. code-block:: python

 from typing import Set
 from django.utils import timezone

 from rest_framework.permissions import BasePermission

 from .models import AccessGroup, UserAccessGroupAssignment


 class FunctionAuthBackend:
     """Custom auth backend que extiende permissions con Function.

     Settings:
         AUTHENTICATION_BACKENDS = [
             'django.contrib.auth.backends.ModelBackend',
             'apps.access.permissions.FunctionAuthBackend',
         ]
     """

     def authenticate(self, request, **credentials):
         return None  # No autentica, solo provee permissions

     def get_user_permissions(self, user_obj, obj=None) -> Set[str]:
         return set()

     def get_group_permissions(self, user_obj, obj=None) -> Set[str]:
         """Retorna codenames de Function vía AccessGroup activos."""
         if not user_obj.is_authenticated:
             return set()

         now = timezone.now()
         active_assignments = UserAccessGroupAssignment.objects.filter(
             user=user_obj,
         ).filter(
             models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=now),
         )

         codenames: Set[str] = set()
         for assignment in active_assignments.select_related("access_group"):
             codenames.update(
                 assignment.access_group.functions.filter(
                     is_active=True,
                 ).values_list("codename", flat=True),
             )
         return codenames

     def get_all_permissions(self, user_obj, obj=None) -> Set[str]:
         return self.get_group_permissions(user_obj, obj)

     def has_perm(self, user_obj, perm, obj=None) -> bool:
         """user.has_perm('view_reports') → bool."""
         return perm in self.get_all_permissions(user_obj, obj)


 class FunctionPermission(BasePermission):
     """DRF permission class — usar en views.

     Uso:
         class MyView(APIView):
             permission_classes = [FunctionPermission]
             required_function = 'view_reports'
     """

     def has_permission(self, request, view) -> bool:
         required = getattr(view, "required_function", None)
         if not required:
             return True  # endpoint sin gating
         return request.user.is_authenticated and request.user.has_perm(required)

**Uso en una view DRF:**

.. code-block:: python

 from rest_framework.views import APIView
 from rest_framework.response import Response

 from apps.access.permissions import FunctionPermission


 class ReportListView(APIView):
     permission_classes = [FunctionPermission]
     required_function = "view_reports"   # ← Function codename

     def get(self, request):
         # ... lógica
         return Response(data)

----

Q5 — Custom vs auth.Group: justificado en ADR-BACK-007
=======================================================

Sin código nuevo — la decisión es **arquitectónica**, no
código. La implementación de los modelos custom de Q1 ya
materializa esta decisión.

**Punto crítico:** el code review del backend debe verificar
que ``apps.access.models.AccessGroup`` no extienda
``django.contrib.auth.models.Group``. Si lo hace, viola la
decisión de ADR-BACK-007.

**Test guardrail — ``apps/access/tests/test_models.py``:**

.. code-block:: python

 from django.contrib.auth.models import Group as DjangoAuthGroup

 from apps.access.models import AccessGroup


 def test_access_group_is_not_auth_group_subclass():
     """ADR-BACK-007: AccessGroup es independiente de auth.Group."""
     assert not issubclass(AccessGroup, DjangoAuthGroup)


 def test_access_group_does_not_have_django_auth_relations():
     """No hay FK accidental hacia auth_group."""
     fields = {f.name for f in AccessGroup._meta.get_fields()}
     assert "group_ptr" not in fields  # OneToOne wrapper signal
     assert "auth_group" not in fields

----

Q6 — Naming: snake_case + verbo imperativo (idiomatic)
=======================================================

IACT ya cumple esta convención. Validación automática:

**Test — ``apps/access/tests/test_models.py``:**

.. code-block:: python

 import re
 import pytest

 from apps.access.models import Function

 # Pattern: snake_case + verbo imperativo. Sin prefijo `can_`.
 # Verbos comunes: view, list, search, create, update, delete,
 # assign, revoke, manage, export, import, schedule, share, ...
 CODENAME_PATTERN = re.compile(
     r"^(view|list|search|create|update|delete|assign|revoke|"
     r"manage|export|import|schedule|share|grant|disable|"
     r"reactivate|block|unblock|deactivate|configure|pause|"
     r"reset|generate|read|save|acknowledge|subscribe|"
     r"unsubscribe|request|monitor|barge_in|broadcast|hold|"
     r"close|answer|make|enter|transfer)_[a-z0-9_]+$",
 )


 @pytest.mark.django_db
 def test_all_functions_follow_codename_convention():
     for fn in Function.objects.all():
         assert CODENAME_PATTERN.match(fn.codename), (
             f"{fn.codename} no sigue convención snake_case + verbo"
         )

----

Q7 — SoD enforcement: signal en pre_save
=========================================

**Finding (verbatim de Q7):**

   *"In RBAC, permissions are associated with roles, and users
   are granted membership in appropriate roles ... RBAC uses
   mutual exclusion constraints to implement SoD policies."*
   — `Purdue paper on SoD
   <https://www.cs.purdue.edu/homes/ninghui/papers/sod-j.pdf>`_.

**Decisión IACT:** ``FunctionSeparationRule`` validada en
``pre_save`` signal cuando se crea ``UserAccessGroupAssignment``.

**Implementación — ``apps/access/signals.py``:**

.. code-block:: python

 from django.core.exceptions import ValidationError
 from django.db.models.signals import pre_save
 from django.dispatch import receiver

 from .models import (
     AccessGroup,
     FunctionSeparationRule,
     UserAccessGroupAssignment,
 )


 @receiver(pre_save, sender=UserAccessGroupAssignment)
 def enforce_sod(sender, instance, **kwargs):
     """Bloquea asignar grupo que viole una regla SoD."""

     candidate_group: AccessGroup = instance.access_group

     # Grupos ya asignados al user (excluyendo el propio assignment)
     existing_groups = AccessGroup.objects.filter(
         useraccessgroupassignment__user=instance.user,
     ).exclude(pk=candidate_group.pk).distinct()

     # Para cada SoD rule, ¿el candidato + existentes activan
     # la mutua exclusión?
     active_rules = FunctionSeparationRule.objects.filter(is_active=True)

     for rule in active_rules.prefetch_related("groups_a", "groups_b"):
         a_codes = set(rule.groups_a.values_list("agr_code", flat=True))
         b_codes = set(rule.groups_b.values_list("agr_code", flat=True))

         # ¿El candidato está en A y el user ya tiene alguno de B?
         existing_codes = set(
             existing_groups.values_list("agr_code", flat=True)
         )

         if candidate_group.agr_code in a_codes and existing_codes & b_codes:
             conflict = (existing_codes & b_codes).pop()
             raise ValidationError(
                 f"SoD violación ({rule.code}): "
                 f"{candidate_group.agr_code} no puede coexistir con "
                 f"{conflict} en el mismo usuario.",
             )

         # Y simétricamente: candidato en B con A existente
         if candidate_group.agr_code in b_codes and existing_codes & a_codes:
             conflict = (existing_codes & a_codes).pop()
             raise ValidationError(
                 f"SoD violación ({rule.code}): "
                 f"{candidate_group.agr_code} no puede coexistir con "
                 f"{conflict} en el mismo usuario.",
             )

----

Q8 — django-guardian: NO incluido en v5.6.0
============================================

**Finding (Q8):** IACT no requiere object-level permissions.
Las decisiones de acceso son **model-level** + **segment-bound
queryset filter** (ver UC_INC_RPT_01).

**Implementación — segment-bound filter (sin django-guardian):**

.. code-block:: python

 # En cada ViewSet/View que devuelve datos segmentados:

 from rest_framework.viewsets import ReadOnlyModelViewSet


 class ReportViewSet(ReadOnlyModelViewSet):
     permission_classes = [FunctionPermission]
     required_function = "view_reports"

     def get_queryset(self):
         """Filtra por segmento del User (BR-012)."""
         qs = Report.objects.all()
         user = self.request.user
         if user.segment_id:
             qs = qs.filter(segment_id=user.segment_id)
         return qs

**Si en el futuro se necesita object-level:** documentado como
TD-RBAC-02 (re-evaluar wrapper ``OneToOneField`` para
compatibilidad con ``django-guardian``).

----

Tests obligatorios
==================

.. code-block:: python

 # apps/access/tests/test_bootstrap_migration.py
 import pytest
 from django.core.management import call_command

 from apps.access.models import AccessGroup, Function, FunctionSeparationRule


 @pytest.mark.django_db
 def test_bootstrap_creates_64_in_scope_functions():
     # La migración corre automáticamente al setup de DB de tests
     assert Function.objects.count() == 64


 @pytest.mark.django_db
 def test_bootstrap_creates_10_in_scope_groups():
     # AGR-011/012 RESERVADOS no se crean en v5.6.0
     assert AccessGroup.objects.filter(is_system=True).count() == 10


 @pytest.mark.django_db
 def test_bootstrap_creates_3_sod_rules():
     assert FunctionSeparationRule.objects.filter(is_active=True).count() == 3


 @pytest.mark.django_db
 def test_agr_010_is_system_admin_group():
     g = AccessGroup.objects.get(agr_code="AGR-010")
     assert g.name == "system_admin_group"
     assert g.is_system is True


 @pytest.mark.django_db
 def test_agr_007_is_permission_admin_group():
     g = AccessGroup.objects.get(agr_code="AGR-007")
     assert g.name == "permission_admin_group"


 @pytest.mark.django_db
 def test_agr_008_is_auditor_group():
     g = AccessGroup.objects.get(agr_code="AGR-008")
     assert g.name == "auditor_group"


 @pytest.mark.django_db
 def test_sod_001_separates_pipeline_from_auditor():
     rule = FunctionSeparationRule.objects.get(code="SOD-001")
     assert rule.groups_a.filter(agr_code="AGR-009").exists()
     assert rule.groups_b.filter(agr_code="AGR-008").exists()


 # apps/access/tests/test_sod_enforcement.py
 @pytest.mark.django_db
 def test_sod_blocks_pipeline_admin_with_auditor(user, request_user):
     pipeline = AccessGroup.objects.get(agr_code="AGR-009")
     auditor = AccessGroup.objects.get(agr_code="AGR-008")

     UserAccessGroupAssignment.objects.create(
         user=user, access_group=pipeline, assigned_by=request_user,
     )

     with pytest.raises(ValidationError, match="SoD violación"):
         UserAccessGroupAssignment.objects.create(
             user=user, access_group=auditor, assigned_by=request_user,
         )


 # apps/access/tests/test_permission_backend.py
 @pytest.mark.django_db
 def test_user_with_agr_002_has_view_reports(user_with_agr):
     u = user_with_agr("AGR-002")  # report_viewer_group
     assert u.has_perm("view_reports") is True


 @pytest.mark.django_db
 def test_expired_assignment_revokes_permission(user_with_agr_expired):
     u = user_with_agr_expired("AGR-002")
     assert u.has_perm("view_reports") is False

----

Mapping completo Q1-Q8 → archivos
==================================

.. list-table::
 :widths: 6 30 32 32
 :header-rows: 1

 * - Q
   - Hallazgo
   - Archivo de implementación
   - Test
 * - Q1
   - Modelos custom
   - ``apps/access/models.py``
   - ``test_models.py``
 * - Q2
   - Bootstrap RunPython
   - ``apps/access/migrations/0002_bootstrap_rbac.py``
   - ``test_bootstrap_migration.py``
 * - Q3
   - is_system enforcement
   - ``apps/access/admin.py`` + Manager
   - ``test_models.py``
 * - Q4
   - DRF integration
   - ``apps/access/permissions.py``
   - ``test_drf_integration.py``
 * - Q5
   - Custom vs auth.Group
   - (decisión arquitectónica)
   - ``test_models.py`` (guardrail)
 * - Q6
   - Naming idiomatic
   - (ya cumplido)
   - ``test_models.py`` (regex)
 * - Q7
   - SoD signal
   - ``apps/access/signals.py``
   - ``test_sod_enforcement.py``
 * - Q8
   - Sin object-level permissions
   - segment-bound filter en ViewSet
   - ``test_drf_integration.py``

----

Settings.py — registro
======================

.. code-block:: python

 # config/settings.py

 INSTALLED_APPS = [
     # ...
     "apps.access",
 ]

 AUTHENTICATION_BACKENDS = [
     "django.contrib.auth.backends.ModelBackend",
     "apps.access.permissions.FunctionAuthBackend",
 ]

 # Conectar signal SoD al app config
 # apps/access/apps.py:
 #   def ready(self):
 #       from . import signals  # noqa
 INSTALLED_APPS_DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

----

Trazabilidad
============

- **ADR raíz:** :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`.
- **WP de research:** ``2026-05-06-19-27-21-agr-django-permission-groups-research``.
- **Hallazgos verbatim:** ``research/raw/Q1.md`` ... ``Q8.md``.
- **Modelo conceptual:** :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.
- **Bootstrap diagrama:** :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/diagramas/bootstrap-grupos-predefinidos`.
- **SQL schema:** :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/implementacion` §8.
- **Convenciones REST API:** :doc:`/normativa/estandares/std-013-rest-api-conventions`.

----

Q9 — MenuItem UI metadata layer + UserCapabilityResolver
=========================================================

Extension de la guia para v5.6.x con la capa UX persistida del
menu (``MenuItem``) y el resolver canonico de capabilities. Las
decisiones arquitectonicas viven en ADR-BACK-008/009/010 y
CNST-032 v2.0.0.

Q9.1 Modelo MenuItem
--------------------

``MenuItem`` es **wrapper UX 1:1** sobre ``Function``. Ver
ADR-BACK-008 para invariantes I-1..I-4 y rationale completo.

.. code-block:: python

   # apps/access/models.py
   class MenuItem(models.Model):
       function = models.OneToOneField(
           Function,
           on_delete=models.PROTECT,
           related_name="menu_item",
       )
       display_label = models.CharField(max_length=100)
       icon = models.CharField(max_length=100, blank=True)
       display_order = models.IntegerField(default=0)
       route_path = models.URLField(max_length=200)
       parent = models.ForeignKey(
           "self", null=True, blank=True,
           on_delete=models.SET_NULL,
           related_name="children",
       )
       status = models.CharField(
           max_length=20,
           choices=[
               ("DRAFT", "Borrador"),
               ("ACTIVE", "Activo"),
               ("DEPRECATED", "Deprecado"),
               ("ARCHIVED", "Archivado"),
           ],
           default="DRAFT",
       )
       deprecated_at = models.DateTimeField(null=True, blank=True)
       archived_at = models.DateTimeField(null=True, blank=True)
       block_auto_archive = models.BooleanField(default=False)
       block_reason = models.CharField(max_length=500, blank=True, default="")
       block_set_by = models.ForeignKey(
           User, null=True, blank=True,
           on_delete=models.PROTECT,
           related_name="menu_items_archive_blocked",
       )
       block_set_at = models.DateTimeField(null=True, blank=True)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       created_by = models.ForeignKey(
           User, on_delete=models.PROTECT,
           related_name="menu_items_created",
       )

       objects = MenuItemQuerySet.as_manager()

       class Meta:
           db_table = "menu_items"
           ordering = ("display_order",)
           indexes = [
               models.Index(fields=("status",)),
               models.Index(fields=("status", "display_order")),
               models.Index(fields=("deprecated_at",)),
           ]

Q9.2 Function extendida con is_critical
---------------------------------------

.. code-block:: python

   class Function(models.Model):
       # ... campos existentes ...
       is_critical = models.BooleanField(
           default=False,
           help_text=(
               "Si True, has_capability bypassa el cache. "
               "Cambiable solo via data migration "
               "(ADR-BACK-010)."
           ),
       )

       class Meta:
           db_table = "functions"
           indexes = [
               models.Index(fields=("codename",)),
               models.Index(fields=("is_active",)),
               models.Index(fields=("module",)),
               models.Index(fields=("codename", "is_active")),
           ]

Q9.3 UserCapabilityResolver canonico
------------------------------------

Unico punto de computo de capabilities. Endpoints,
middlewares, views y serializers consumen este resolver — NO
calculan capabilities ad-hoc.

.. code-block:: python

   # apps/access/resolvers.py
   from django.core.cache import cache, CacheError
   from django.db.models import Q
   from django.utils import timezone

   from .models import Function


   class UserCapabilityResolver:
       CACHE_TTL = 300
       CRITICAL_TTL = 60

       @staticmethod
       def resolve(user) -> set[str]:
           """Cache-first. Para reads (AP-2a)."""
           if not user or not user.is_authenticated:
               return set()
           key = f"caps:user:{user.id}"
           try:
               cached = cache.get(key)
               if cached is not None:
                   return cached
           except CacheError:
               pass  # degraded mode — continua a DB
           codenames = UserCapabilityResolver._query_db(user)
           try:
               cache.set(key, codenames, timeout=UserCapabilityResolver.CACHE_TTL)
           except CacheError:
               pass
           return codenames

       @staticmethod
       def resolve_uncached(user) -> set[str]:
           """DB-first. Para critical writes (AP-2b)."""
           if not user or not user.is_authenticated:
               return set()
           return UserCapabilityResolver._query_db(user)

       @staticmethod
       def has_capability(user, codename: str) -> bool:
           """Decide cache vs DB segun is_critical."""
           critical_set = UserCapabilityResolver._critical_codenames()
           if codename in critical_set:
               return codename in UserCapabilityResolver.resolve_uncached(user)
           return codename in UserCapabilityResolver.resolve(user)

       @staticmethod
       def _query_db(user) -> set[str]:
           now = timezone.now()
           codenames = (
               Function.objects
               .filter(is_active=True)
               .filter(access_groups__useraccessgroupassignment__user=user)
               .filter(
                   Q(access_groups__useraccessgroupassignment__expires_at__isnull=True)
                   | Q(access_groups__useraccessgroupassignment__expires_at__gt=now)
               )
               .values_list("codename", flat=True)
               .distinct()
           )
           return set(codenames)

       @staticmethod
       def _critical_codenames() -> set[str]:
           cached = cache.get("func:critical_set") if cache else None
           if cached is not None:
               return cached
           codenames = set(
               Function.objects
                       .filter(is_critical=True, is_active=True)
                       .values_list("codename", flat=True)
           )
           cache.set("func:critical_set", codenames,
                     timeout=UserCapabilityResolver.CRITICAL_TTL)
           return codenames

Q9.4 Invalidacion explicita en UCs
----------------------------------

Helper centralizado, llamado desde cada UC mutating de RBAC:

.. code-block:: python

   # apps/access/cache.py
   import logging

   from django.core.cache import cache, CacheError

   logger = logging.getLogger(__name__)


   def invalidate_user_capabilities(user_id: int) -> None:
       try:
           cache.delete(f"caps:user:{user_id}")
       except CacheError as exc:
           logger.error(
               "cache_invalidation_failed",
               extra={"user_id": user_id, "exc": str(exc)},
           )
           # NO re-raise — degraded mode (ADR-BACK-009)


   def invalidate_critical_set() -> None:
       """Llamado solo por migrations que cambian is_critical."""
       try:
           cache.delete("func:critical_set")
       except CacheError:
           pass

Patron de uso en UC:

.. code-block:: python

   from django.db import transaction
   from .cache import invalidate_user_capabilities


   class AssignFunctionsToGroupUC:
       @transaction.atomic
       def execute(self, group_id: int, function_codes: list[str], invoker):
           # ... insert/update FunctionGroupMembership ...
           affected_user_ids = list(
               UserAccessGroupAssignment.objects
               .filter(group_id=group_id)
               .values_list("user_id", flat=True)
           )
           transaction.on_commit(
               lambda: [
                   invalidate_user_capabilities(uid)
                   for uid in affected_user_ids
               ]
           )

Q9.5 MenuItem queryset visible / for_user
-----------------------------------------

.. code-block:: python

   # apps/access/managers.py
   from django.db import models

   from .resolvers import UserCapabilityResolver


   class MenuItemQuerySet(models.QuerySet):
       def visible(self):
           """ACTIVE + Function activa."""
           return self.filter(
               status="ACTIVE",
               function__is_active=True,
           )

       def for_user(self, user):
           """MenuItems que el user puede ver."""
           codenames = UserCapabilityResolver.resolve(user)
           return self.visible().filter(
               function__codename__in=codenames,
           ).select_related("function")

       def with_status_for_admin(self, statuses):
           """Para preview admin de items DRAFT/DEPRECATED."""
           return self.filter(
               status__in=statuses,
               function__is_active=True,
           )

Q9.6 Endpoint GET /api/v1/menu/
-------------------------------

.. code-block:: python

   # apps/access/views.py
   from rest_framework.permissions import IsAuthenticated
   from rest_framework.response import Response
   from rest_framework.views import APIView

   from .resolvers import UserCapabilityResolver
   from .models import MenuItem
   from .serializers import MenuItemSerializer


   class UserMenuView(APIView):
       permission_classes = [IsAuthenticated]

       def get(self, request):
           user = request.user
           capabilities = UserCapabilityResolver.resolve(user)
           items = MenuItem.objects.for_user(user)
           return Response({
               "capabilities": sorted(capabilities),
               "menu_items": MenuItemSerializer(items, many=True).data,
           })

Shape de respuesta:

.. code-block:: text

   GET /api/v1/menu/

   200 OK
   {
     "capabilities": ["view_reports", "manage_menu_catalog"],
     "menu_items": [
       {
         "id": 12,
         "codename": "view_reports",
         "display_label": "Mis Reportes",
         "icon": "BarChartIcon",
         "route_path": "/reports",
         "display_order": 10,
         "parent_id": null,
         "status": "ACTIVE"
       }
     ]
   }

Q9.7 Indices que sostienen P95 ≤ 20ms
-------------------------------------

13 indices distribuidos en 4 tablas:

.. list-table::
 :widths: 30 60 10
 :header-rows: 1

 * - Tabla
   - Indices
   - Total
 * - ``user_access_group_assignment`` (UAGA)
   - ``user_id``, ``group_id``, ``(user_id, expires_at)``,
     ``expires_at``
   - 4
 * - ``function_group_membership`` (FGM)
   - ``group_id``, ``function_id``
   - 2
 * - ``functions``
   - ``codename``, ``is_active``, ``module``,
     ``(codename, is_active)``
   - 4
 * - ``menu_items``
   - ``status``, ``(status, display_order)``,
     ``deprecated_at``
   - 3

Q9.8 Tests obligatorios extension
---------------------------------

.. code-block:: python

   @pytest.mark.django_db
   def test_user_capability_resolver_query_count():
       """resolve() ejecuta exactamente 1 query."""
       user = make_user_with_agr("AGR-002")
       cache.clear()
       with django_assert_num_queries(1):
           UserCapabilityResolver.resolve(user)


   @pytest.mark.django_db
   def test_critical_capability_bypasses_cache():
       fn = Function.objects.create(
           codename="assign_functions", module="ADM",
           is_critical=True, is_active=True,
       )
       user = make_user_with_capability("assign_functions")
       cache.set(f"caps:user:{user.id}", set())  # cache vacio
       assert UserCapabilityResolver.has_capability(
           user, "assign_functions",
       ) is True


   @pytest.mark.django_db
   def test_invalidate_user_capabilities_no_raise_on_cache_error():
       """Degraded mode: cache fail no aborta UC."""
       with mock.patch.object(cache, "delete",
                                side_effect=CacheError):
           invalidate_user_capabilities(1)  # no debe lanzar

Q9.9 Mapping Q9 → archivos
--------------------------

.. list-table::
 :widths: 6 30 32 32
 :header-rows: 1

 * - Q9
   - Hallazgo
   - Archivo de implementacion
   - Test
 * - 9.1
   - MenuItem wrapper UX
   - ``apps/access/models.py``
   - ``test_menu_item.py``
 * - 9.2
   - is_critical en Function
   - ``apps/access/models.py``
   - ``test_models.py``
 * - 9.3
   - UserCapabilityResolver
   - ``apps/access/resolvers.py``
   - ``test_resolvers.py``
 * - 9.4
   - Invalidacion explicita
   - ``apps/access/cache.py``
   - ``test_cache.py``
 * - 9.5
   - Queryset MenuItem
   - ``apps/access/managers.py``
   - ``test_menu_item.py``
 * - 9.6
   - Endpoint /api/v1/menu/
   - ``apps/access/views.py``
   - ``test_menu_endpoint.py``
 * - 9.7
   - Indices P95
   - ``apps/access/models.py`` (Meta.indexes)
   - ``test_models.py`` (assert indexes)

----

Sources Django/DRF (verbatim)
=============================

- `django.contrib.auth — Django docs
  <https://docs.djangoproject.com/en/6.0/ref/contrib/auth/>`_
- `Migration Operations — Django docs
  <https://docs.djangoproject.com/en/5.0/ref/migration-operations/>`_
- `Permissions — DRF docs
  <https://www.django-rest-framework.org/api-guide/permissions/>`_
- `Customizing authentication in Django — Django docs
  <https://docs.djangoproject.com/en/6.0/topics/auth/customizing/>`_
- `Django ticket #29748 — AUTH_GROUP_MODEL
  <https://code.djangoproject.com/ticket/29748>`_
