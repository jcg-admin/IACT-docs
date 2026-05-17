```yml
created_at: 2026-05-06 19:38:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 1 — DISCOVER (research)
author: NestorMonroy
status: Aprobado
version: 1.0.0
query_id: Q1
tier: 1 (oficial)
```

# Q1 — Django auth.Group y auth.Permission

## Query ejecutado

```
Django auth Group Permission model documentation
```

`allowed_domains=["docs.djangoproject.com"]` — restringido a docs
oficiales.

## Hallazgos verbatim (Tier 1 — docs.djangoproject.com)

### `Group` — modelo nativo

> "Django's Group models are a generic way of categorizing users
> so you can apply permissions, or some other label, to those
> users. A user can belong to any number of groups, and a user in
> a group automatically has the permissions granted to that group.
> For example, if the group 'Site editors' has the permission
> 'can_edit_home_page', any user in that group will have that
> permission."

**Implicaciones para IACT:**

- Django ya provee un modelo `Group` listo para usar.
- El concepto IACT de "AccessGroup" duplica conceptualmente
  `django.contrib.auth.models.Group`.
- La relación `user → groups → permissions` ya existe nativa.

### `Permission` — modelo nativo

> "The Permission model is rarely accessed directly. Four default
> permissions – add, change, delete, and view – are created for
> each Django model defined in one of your installed applications.
> These permissions will be created when you run manage.py
> migrate."

**Implicaciones para IACT:**

- Django crea automáticamente 4 permisos por Model: add, change,
  delete, view.
- IACT-docs ya **no** sigue esta convención: usa nombres
  descriptivos ("view_reports", "export_csv", "manage_users")
  en lugar de "{app}.{action}_{model}". Esto puede ser custom
  permissions definidas en `Meta.permissions` de cada Model, lo
  cual ES soportado nativamente.

### Relación User ↔ Groups ↔ Permissions

> "User objects have two many-to-many fields: groups and
> user_permissions. User objects can access their related objects
> through methods like myuser.groups.set(), myuser.groups.add(),
> and myuser.user_permissions.set()."

**Implicaciones:**

- `user.groups` y `user.user_permissions` son M2M nativas.
- `user.has_perm("app.codename")` usa la unión de permissions
  directas + las heredadas de groups.
- IACT-docs tiene M2M custom (`UserFunctionAssignment`,
  `UserFunctionGroupAssignment`) que **duplican** las nativas si
  no usan `auth.Group`.

## Sources

- [django.contrib.auth | Django documentation](https://docs.djangoproject.com/en/6.0/ref/contrib/auth/)
- [Using the Django authentication system | Django documentation](https://docs.djangoproject.com/en/6.0/topics/auth/default/)

## Veredicto preliminar Q1

Django **provee nativo** el patrón Group + Permission. El modelo
IACT (`AccessGroup`, `Function`) duplica conceptualmente lo que
ya existe. Pendiente: verificar si la duplicación se justifica
por features adicionales (SoD, `is_system`, custom assignment
metadata) o si conviene usar `auth.Group` directamente con
custom permissions.
