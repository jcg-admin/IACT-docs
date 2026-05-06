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
