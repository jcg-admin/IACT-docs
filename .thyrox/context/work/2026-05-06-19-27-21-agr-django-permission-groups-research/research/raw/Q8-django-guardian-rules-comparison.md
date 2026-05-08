```yml
created_at: 2026-05-06 19:46:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 1 — DISCOVER (research)
author: NestorMonroy
status: Aprobado
version: 1.0.0
query_id: Q8
tier: 2 (paquetes establecidos)
```

# Q8 — django-guardian vs django-rules para object-level permissions

## Query ejecutado

```
django-guardian django-rules object level permissions comparison official
```

## Hallazgos verbatim

### `django-guardian`

> "Django-guardian is an implementation of object permissions
> for Django providing an extra authentication backend. It is
> an implementation of per-object permissions on top of Django's
> authorization backend."

> "Django-Guardian extends Django's permissions system to
> include object-level permissions and allows you to assign
> permissions to individual objects, enabling more granular
> access control. The package provides helper functions like
> `assign_perm()` to assign permissions and shortcuts like
> `get_perms()` and `get_objects_for_user()` to check
> permissions."

API canónica:
```python
from guardian.shortcuts import assign_perm, get_objects_for_user

assign_perm('view_report', user, report_instance)
reports = get_objects_for_user(user, 'reports.view_report')
```

### `django-rules`

> "Django-rules is another notable option for object-based
> permissions in Django. Django-Rules excels in scenarios where
> rules are based on logical conditions, however, it may fall
> short when you need to handle highly dynamic permissions
> based on object attributes."

> "Rules appears to be not so much a Django specific
> implementation as much as a way to implement rules +
> predicates to get things done."

### Comparación

| Aspecto | django-guardian | django-rules |
|---|---|---|
| Modelo | Per-object permissions tabla | Predicates en código |
| Storage | DB rows (`UserObjectPermission`) | Sin storage; eval en runtime |
| Performance | Index lookup | Eval Python |
| Backend nativo | Sí (extra ModelBackend) | Sí (rules backend) |
| DRF integration | `DjangoObjectPermissionsFilter` | `DRYPermissions` o custom |
| Compatibilidad con `auth.Group` | **Sí** (lo asume) | Sí (orthogonal) |

### Aplicabilidad a IACT

IACT no requiere **strict object-level permissions** (per-row).
El requisito es:

- "user con segmento Centro Norte solo ve usuarios del segmento
  Centro Norte" → esto se resuelve por **segment-bound queries**
  (filtering en queryset) declaradas en BR-012 + UC_INC_RPT_01,
  no por per-object permissions.
- "auditor solo ve audit log" → esto es **model-level** (DRF
  `DjangoModelPermissions` ya lo cubre).

**Por lo tanto:**

- `django-guardian`: **probablemente innecesario** para IACT.
- `django-rules`: aplicable si se quieren reglas complejas
  cross-object, pero IACT no las tiene declaradas.

## Veredicto preliminar Q8

IACT-docs **no necesita** ni `django-guardian` ni `django-rules`
para su scope actual. Las decisiones de acceso son model-level
+ segment-filter (queryset), ambas resolubles con
`django.contrib.auth` + DRF nativo.

Si en el futuro se agrega "user X solo ve sus reportes", ahí sí
django-guardian sería el camino canónico (ampliamente adoptado,
compatible con `auth.Group`).

## Sources

- [Django Guardian](https://django-guardian.readthedocs.io/)
- [django-guardian GitHub](https://github.com/django-guardian/django-guardian)
- [Permissions - Django REST framework](https://www.django-rest-framework.org/api-guide/permissions/)
- [Using django permissions with django guardian (object level) - Django Forum](https://forum.djangoproject.com/t/using-django-permissions-with-django-guardian-object-level-permissions/39243)
- [Wrapping my head around object level permissions with Django (Constantine Kokkinos)](https://constantinekokkinos.com/articles/454/wrapping-my-head-around-object-level-permissions-with-django)
