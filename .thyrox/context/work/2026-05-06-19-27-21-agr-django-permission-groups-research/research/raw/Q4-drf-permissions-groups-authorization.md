```yml
created_at: 2026-05-06 19:41:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 1 — DISCOVER (research)
author: NestorMonroy
status: Aprobado
version: 1.0.0
query_id: Q4
tier: 1 (oficial)
```

# Q4 — DRF: DjangoModelPermissions / DjangoObjectPermissions / Group authorization

## Query ejecutado

```
Django REST Framework permissions DjangoModelPermissions
DjangoObjectPermissions Group authorization
```

`allowed_domains=["django-rest-framework.org",
"www.django-rest-framework.org"]`

## Hallazgos verbatim (Tier 1 — django-rest-framework.org)

### `DjangoModelPermissions`

> "DjangoModelPermissions ties into Django's standard
> django.contrib.auth model permissions, and authorization will
> only be granted if the user is authenticated and has the
> relevant model permissions assigned. POST requests require
> the user to have the add permission on the model, PUT and
> PATCH requests require the user to have the change permission
> on the model, and DELETE requests require the user to have the
> delete permission on the model."

**Implicación:** DRF reusa `auth.Permission` directamente.
Mapping built-in: HTTP method → CRUD permission.

### `DjangoObjectPermissions`

> "DjangoObjectPermissions authorizes requests only if the user
> is authenticated and has the relevant per-object permissions
> and relevant model permissions assigned. For object level view
> permissions in GET, HEAD and OPTIONS requests using
> django-guardian, the DjangoObjectPermissionsFilter class
> ensures that list endpoints only return results including
> objects for which the user has appropriate view permissions."

**Implicación:** object-level (per-row) permissions vía
`django-guardian` (paquete tercero canónico). Útil si IACT
quiere "user X solo ve sus propios reportes" por instancia.

### Permission checks — el flow

> "Permission checks are always run at the very start of the
> view, before any other code is allowed to proceed, and will
> typically use the authentication information in the
> request.user and request.auth properties to determine if the
> incoming request should be permitted."

**Implicación:** DRF ya tiene gating canónico — no se necesita
middleware custom.

### Mapping IACT → DRF

| Concepto IACT | DRF nativo |
|---|---|
| `Function` (atomic permission) | `auth.Permission` con custom codename |
| `AccessGroup` (predefinido) | `auth.Group` creado via data migration |
| RBAC enforcement en API | `DjangoModelPermissions` o custom `BasePermission` |
| `view_reports` granular | Custom permission codename + `permission_classes = [HasFunctionPermission]` |

## Veredicto preliminar Q4

DRF **NO requiere modelo custom** para Group/Permission.
`DjangoModelPermissions` ata directamente con
`django.contrib.auth`. Si IACT-docs usa custom permission
classes (que parece probable dado los nombres custom de
funciones), debe basarse en `user.has_perm("app.codename")` que
funciona indistintamente con permissions directas + heredadas
de groups.

**Implicación clave:** el patrón de IACT (custom AccessGroup +
custom Function + custom assignment models) está construyendo
una capa paralela a `django.contrib.auth` + DRF
`DjangoModelPermissions`. Si la justificación es solo "we have
RBAC", es **redundante**. Si la justificación es features
adicionales (SoD, temporal permissions, segment-bound queries,
audit), entonces es **legítimo** pero hay que documentarlo.

## Sources

- [Permissions - Django REST framework](https://www.django-rest-framework.org/api-guide/permissions/)
- [4 - Authentication and permissions - Django REST framework](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/)
- [Authentication - Django REST framework](https://www.django-rest-framework.org/api-guide/authentication/)
