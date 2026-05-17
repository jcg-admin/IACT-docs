```yml
created_at: 2026-05-06 19:43:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 1 — DISCOVER (research)
author: NestorMonroy
status: Aprobado
version: 1.0.0
query_id: Q5
tier: 1+2 (oficial Django + comunidad)
```

# Q5 — Custom Group model vs extender auth.Group

## Query ejecutado

```
Django custom Group model vs extend auth Group RBAC project pattern
```

## Hallazgos verbatim

### Limitación oficial de `auth.Group` (Django Forum + ticket)

> "Django's contrib.auth Group model is not customizable, forcing
> users to work around Django to customize it, and customization
> is necessary in any bigger project."

> "When projects want to relate group permissions to custom
> entities (like teams), they must create a custom backend that
> extends django.contrib.auth.ModelBackend."

**Ticket Django #29748** propone agregar `AUTH_GROUP_MODEL`
setting para swappear el modelo Group (paralelo a
`AUTH_USER_MODEL`). **No mergeado aún** — es un proyecto open
issue.

### Aproximaciones documentadas

**Aproximación 1 — Custom Group con `AUTH_GROUP_MODEL` (no oficial):**

> "In a custom User model, you can set a field to point to your
> custom Group model, where users get all permissions granted to
> each of their groups. You must set this model as the
> AUTH_GROUP_MODEL in settings.py."

Requiere parche en Django o paquete tercero
(`django-group-model`).

**Aproximación 2 — Wrapper `OneToOneField`:**

> "A common pattern uses a custom Role model with a
> OneToOneField relationship to the built-in Group model,
> allowing you to add extra fields and methods without fully
> replacing the Group model."

```python
class Role(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    is_system = models.BooleanField(default=False)
    description = models.TextField()
```

Ventaja: compatible con `django-guardian` y otros packages que
asumen `auth.Group`.

**Aproximación 3 — Custom model independiente (estilo IACT):**

Modelo `AccessGroup` separado que **no extiende ni envuelve**
`auth.Group`. Es lo que hace IACT-docs.

> "The design limitation restricts other app development, as
> many Django permission packages only support group permissions
> based on django.contrib.auth.models.Group, like django-guardian."

**Costo:** pierde compatibilidad con tooling estándar Django
(admin's Group management, django-guardian per-object
permissions, packages tercero).

## Veredicto preliminar Q5

El patrón IACT (`AccessGroup` independiente) es **comunidad-
documentado pero no oficial**. Es legítimo para proyectos con
features que `auth.Group` no soporta (campo `is_system`,
metadata custom, audit), **pero pierde compatibilidad** con
ecosistema Django (admin UI, django-guardian, packages tercero).

**Recomendación de la comunidad:**

- Para casos pequeños/medianos: **OneToOneField wrapper** (Role
  → Group). Simple, mantiene compatibilidad.
- Para casos grandes: custom model independiente con backend
  custom que extienda `ModelBackend.get_all_permissions()`.

**Para IACT específicamente** (pendiente decision Phase 5):

- Si el modelo actual (`AccessGroup` custom) ya está implementado
  y funcional → mantener + documentar el ADR de la decisión.
- Si está en diseño → considerar el wrapper OneToOneField como
  punto medio.

## Sources

- [Custom Group model - Django Internals - Django Forum](https://forum.djangoproject.com/t/custom-group-model/30070)
- [django-group-model on GitHub](https://github.com/ankitchhatbar/django-group-model)
- [Django Ticket #29748 — Add AUTH_GROUP_MODEL setting](https://code.djangoproject.com/ticket/29748)
- [Managing User Permissions and Groups in Django (Medium)](https://medium.com/django-unleashed/managing-user-permissions-and-groups-in-django-b8ab674314f5)
- [Role-Based Access Control in Django (DEV.to)](https://dev.to/yokwejuste/role-based-access-control-in-django-4j1d)
- [Implementing RBAC in Django (Permify)](https://permify.co/post/rbac-in-django/)
