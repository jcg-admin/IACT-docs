```yml
created_at: 2026-05-06 19:40:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 1 — DISCOVER (research)
author: NestorMonroy
status: Aprobado
version: 1.0.0
query_id: Q3
tier: 1+2 (oficial + comunidad)
```

# Q3 — Grupos inmutables del sistema (is_system pattern)

## Query ejecutado

```
Django predefined system groups immutable best practice fixture vs migration
```

Sin `allowed_domains` — para captar discusión comunitaria sobre
el patrón `is_system`.

## Hallazgos verbatim

### Migrations vs fixtures (Django Forum + docs)

> "To automatically load initial data for an app, create a data
> migration, as migrations are run when setting up the test
> database, making the data available there. In contrast,
> fixtures data isn't loaded automatically, except if you use
> TransactionTestCase.fixtures."

> "Since Django 1.7, automatic loading of fixtures is deprecated
> when applications use migrations, and if you want to load
> initial data for an app, consider doing it in a migration."

### Limitación de fixtures (docs.djangoproject.com)

> "When you run loaddata, the data will be read from the fixture
> and reloaded into the database, meaning that if you change one
> of the rows created by a fixture and then run loaddata again,
> you'll wipe out any changes you've made."

**Implicación:** fixtures son destructivos por re-load; data
migrations son aditivos (con `get_or_create` o checks).

### Natural keys para Groups (docs)

> "For Django's Group model specifically, using primary keys to
> reference objects in fixtures is not always a good idea, as
> the primary key of a group is an arbitrary identifier that the
> database assigns, and in another environment the group can
> have a different ID. To address this, Django defines natural
> keys as unique identifiers that are not necessarily the
> primary key, and in the case of groups, a natural key for the
> group can be its name since two groups can't have the same
> name."

**Implicación para IACT:** los códigos AGR-001..012 son una
forma de natural key — **bueno** para identificación
multi-entorno. Mejor que solo el nombre del grupo si el nombre
puede cambiar.

### Concepto "system groups inmutables" — patrón documentado?

**No hay documentación oficial Django** que defina explícitamente
"system groups inmutables" como patrón nativo. Lo que se
encuentra es:

1. **Recomendación implícita:** crear via data migration → grupo
   existe sin admin UI obvio para borrarlo.
2. **Patrón comunitario:** agregar campo `is_system` (bool) al
   modelo Group **subclassing** o **proxy model**, y bloquear
   delete/edit en admin via `ModelAdmin.has_delete_permission`.
3. **Alternativa señalada en discusiones del Forum:** usar
   `Meta.permissions` para declarar permisos custom + data
   migration para crear grupos predefinidos. No requiere campo
   `is_system` si la disciplina del equipo es "no tocar grupos
   del catálogo via admin".

## Veredicto preliminar Q3

El patrón **`is_system=True`** que usa IACT-docs **NO es un
patrón estándar Django** — es una invención del proyecto que
extiende el modelo Group para agregar inmutabilidad.

La recomendación oficial Django es crear los grupos vía data
migration, dejando que la disciplina (no editarlos via admin)
los mantenga inmutables. Si se necesita enforcement automático,
hay que custom — y `is_system=True` es una solución razonable
pero no idiomática.

**Trade-off:**

- Pro IACT: `is_system` da enforcement programático, no depende
  de disciplina humana.
- Contra IACT: requiere modelo custom (no `auth.Group` directo),
  agrega complejidad, no se beneficia de tooling estándar
  (Django admin maneja Group naturalmente).

## Sources

- [Providing initial Data fixtures vs datamigration - Django Forum](https://forum.djangoproject.com/t/providing-initial-data-fixtures-vs-datamigration/2644)
- [How to provide initial data for models | Django documentation](https://docs.djangoproject.com/en/6.0/howto/initial-data/)
- [Best Practices for migrations - Django Forum](https://forum.djangoproject.com/t/best-practices-for-migrations/11896)
- [Fixtures | Django documentation](https://docs.djangoproject.com/en/6.0/topics/db/fixtures/)
- [Migration Operations | Django documentation](https://docs.djangoproject.com/en/6.0/ref/migration-operations/)
