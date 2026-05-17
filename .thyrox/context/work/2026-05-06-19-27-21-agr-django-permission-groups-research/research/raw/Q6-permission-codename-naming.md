```yml
created_at: 2026-05-06 19:44:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 1 — DISCOVER (research)
author: NestorMonroy
status: Aprobado
version: 1.0.0
query_id: Q6
tier: 1 (oficial)
```

# Q6 — Convención de naming de codenames de Permission

## Query ejecutado

```
Django Permission codename naming convention custom Meta permissions snake_case
```

`allowed_domains=["docs.djangoproject.com"]`

## Hallazgos verbatim (Tier 1)

### Definición de custom permissions

> "Custom permissions in Django are defined in a model's Meta
> class using a list of 2-tuples in the format
> (permission_code, human_readable_permission_name). For
> example: 'can_deliver_pizzas' is an example of a permission
> code."

### Ejemplo canónico oficial

```python
class Task(models.Model):
    ...
    class Meta:
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]
```

### Formato de uso en código

> "Permission format is '<app label>.<permission codename>' when
> used in code (e.g., `myapp.can_deliver_pizzas`)."

Ejemplo enforcement:
```python
user.has_perm("myapp.can_deliver_pizzas")
```

### Convención observada

> "The naming convention appears to follow Python's standard
> snake_case style, with permission codenames being lowercase
> and using underscores to separate words."

**Patrones comunes en docs Django:**

- `can_deliver_pizzas`, `can_publish` (con prefijo `can_`).
- `change_task_status`, `close_task` (sin prefijo, verbo
  imperativo).
- Default Django: `add_*`, `change_*`, `delete_*`, `view_*`
  (auto-generados).

## Comparación con IACT

IACT-docs usa codenames como:

- ✅ `view_reports`, `export_csv`, `manage_users` (snake_case +
  verbo imperativo) → coincide con docs Django.
- ✅ `view_own_sessions`, `close_user_session`, `reset_password`
  → idiomático.
- ⚠️ Algunos como `view_audit_log`, `generate_compliance_report`
  son largos pero válidos.

**No usa el prefijo `can_`** que aparece en algunos ejemplos
Django pero **no es obligatorio**. Django auto-genera
`add_*/change_*/delete_*/view_*` sin prefijo `can_`.

## Veredicto preliminar Q6

La convención IACT (`view_reports`, `export_csv`, `manage_users`)
**coincide con la convención canónica Django** para custom
permissions: snake_case + verbo imperativo + sin prefijo `can_`.

Esta es **la única decisión de IACT que está claramente
alineada con el idioma oficial Django**. No requiere cambios.

## Sources

- [Customizing authentication in Django](https://docs.djangoproject.com/en/6.0/topics/auth/customizing/)
- [Model Meta options | Django documentation](https://docs.djangoproject.com/en/6.0/ref/models/options/)
- [Coding style | Django documentation](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
- [Using the Django authentication system](https://docs.djangoproject.com/en/6.0/topics/auth/default/)
