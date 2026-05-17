```yml
created_at: 2026-05-06 19:50:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 3 — ANALYZE (síntesis post-research)
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Análisis — ¿Es AGR-NNN idiomático en Django/DRF?

## Resumen ejecutivo

**Veredicto:** El modelo IACT (`AccessGroup` custom + `Function`
custom + `is_system=True` + `FunctionSeparationRule`) **NO es
estrictamente idiomático Django**, pero **es legítimo** porque
implementa requisitos que `django.contrib.auth` no provee
nativamente (SoD, immutabilidad enforced).

| Decisión IACT | Idiomatic Django | Veredicto |
|---|---|---|
| `Function` (custom) en lugar de `auth.Permission` | `auth.Permission` con custom codenames | ⚠️ Duplicación parcial |
| `AccessGroup` (custom) en lugar de `auth.Group` | `auth.Group` con data migration | ⚠️ Duplicación parcial |
| Naming `view_reports`, `export_csv` (snake_case verbo) | snake_case verbo (`change_task_status`) | ✅ **Idiomático** |
| Bootstrap via `manage.py initialize_permissions` | Data migration con `RunPython` | ⚠️ Funciona pero no canónico |
| Campo `is_system=True` para grupos predefinidos | No existe nativo | ⚠️ Custom razonable |
| `FunctionSeparationRule` para SoD | No existe nativo en Django | ✅ **Necesario custom** |
| 12 grupos AGR-001..012 con códigos como natural keys | Solo `name` como natural key | ✅ Mejor que solo nombre |

## Mapeo conceptual canónico Django ↔ IACT

```
       Django nativo               IACT-docs v5.6.0
       ──────────────              ────────────────
       auth.User              ←→   User (extiende AbstractUser?)
       auth.Group             ←→   AccessGroup (custom)
       auth.Permission        ←→   Function (custom)
       Group ⟷ Permission     ←→   function_group_membership (M2M)
       User.groups            ←→   user_function_group_assignments (M2M custom)
       User.user_permissions  ←→   user_function_assignments (M2M custom)
       (no nativo)            ←→   FunctionSeparationRule (3 reglas SoD)
       (no nativo)            ←→   AccessGroup.is_system (bool)
       (no nativo)            ←→   código AGR-001..012 (natural key)
```

## Análisis por dimensión

### Dimensión 1: Uso de `auth.Group` vs custom

**Lo que dice Django (Q5):**

> "Django's contrib.auth Group model is not customizable,
> forcing users to work around Django to customize it, and
> customization is necessary in any bigger project."

Hay **3 patrones documentados**:

1. **Custom Group con `AUTH_GROUP_MODEL`** — no oficial, ticket
   #29748 abierto desde 2018.
2. **OneToOneField wrapper** (Role → Group) — más usado en
   comunidad, mantiene compatibilidad.
3. **Custom independiente** (lo que hace IACT) — pierde
   compatibilidad con tooling tercero (django-guardian,
   django-admin native Group UI).

**IACT eligió #3.** Razones probables (inferidas del corpus):

- Necesita `is_system` y otros metadata que no caben en
  `auth.Group` sin extender.
- Quiere control total del lifecycle (UC_PERM_05 crea custom
  groups en runtime).

**Costo del #3:** la disciplina de no usar `auth.Group` requiere
documentación exhaustiva (que ahora tienen) y posibles
incompatibilidades futuras con packages tercero.

### Dimensión 2: `auth.Permission` vs `Function` custom

**Lo que dice Django (Q1):**

> "The Permission model is rarely accessed directly. Four
> default permissions – add, change, delete, and view – are
> created for each Django model. Custom permissions defined in
> Meta.permissions are also created when migrate runs."

**IACT podría usar `auth.Permission` con custom codenames** y
seguir teniendo `view_reports`, `export_csv`, etc. La pregunta
es: ¿qué metadata extra le pone IACT al `Function` que no cabe
en `auth.Permission`?

Per `catalogo-funciones.rst`, los attributes de `Function` son:

- nombre del codename (`view_reports`)
- capability (`reports:view_dashboard`)
- UC asociado
- descripción

Todo esto **cabe en `auth.Permission`** (que ya tiene
`codename`, `name`, y se asocia a `content_type` para el
modelo). El "capability" sería redundante con el codename si se
usara el formato `<app>.<codename>`.

### Dimensión 3: Bootstrap (`manage.py initialize_permissions`)

**Lo que dice Django (Q2):**

> "RunPython is generally the operation you would use to create
> data migrations, run custom data updates and alterations."

> "Since Django 1.7, automatic loading of fixtures is deprecated
> when applications use migrations, and if you want to load
> initial data for an app, consider doing it in a migration."

**IACT-docs usa management command** (`initialize_functions`,
`initialize_function_groups`, `initialize_separation_rules`).
Funciona pero **no es la forma idiomática Django**.

**Recomendación canónica:**

```python
# yourapp/migrations/0002_create_default_groups.py
def create_default_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')  # o AccessGroup si custom
    Permission = apps.get_model('auth', 'Permission')

    for code, name in PREDEFINED_GROUPS:
        group, _ = Group.objects.get_or_create(name=name)
        # ... attach permissions
```

Esto se ejecuta automáticamente al `migrate` (incluyendo en
test database setup) y es idempotente.

**Migrar IACT a data migration en lugar de management command**
es **una mejora idiomatic** que reduce setup steps (no más
"corre el management command tras migrar").

### Dimensión 4: SoD via `FunctionSeparationRule`

**Lo que dice la comunidad (Q7):**

Django **no provee SoD nativo**. Los packages tercero
(`django-rbac`, `django-prbac`) ofrecen scaffolding pero el
enforcement custom queda al proyecto.

**IACT implementa SoD con modelo propio.** Esto es **necesario
y correcto** — no hay forma idiomatic de hacerlo en Django sin
custom code.

**Recomendación:** mantener `FunctionSeparationRule` con ADR
explícito que justifique la decisión (Django no provee SoD;
este es el patrón mínimo para nuestro requirement).

### Dimensión 5: Naming convention

**Lo que dice Django (Q6):**

snake_case + verbo imperativo. Ejemplos: `change_task_status`,
`close_task`, `can_publish`.

**IACT cumple:** `view_reports`, `export_csv`, `manage_users`,
`view_own_sessions`, etc. ✅ Idiomático.

### Dimensión 6: DRF integration

**Lo que dice DRF (Q4):**

> "DjangoModelPermissions ties into Django's standard
> django.contrib.auth model permissions."

DRF asume `auth.Permission`. Si IACT usa `Function` custom,
necesita **custom permission class** que enforce vía
`Function` en lugar de `auth.Permission`. Esto agrega
complejidad pero es lo esperado con cualquier modelo custom.

## Recomendaciones

### Recomendación A — Mantener custom AccessGroup pero aplicar fixes idiomáticos

Si el costo de migrar a `auth.Group` es alto (refactor masivo,
ya hay implementación funcionando), **mantener** `AccessGroup`
custom **pero aplicar**:

1. **A.1** Migrar bootstrap de `manage.py initialize_permissions`
   a data migration (`RunPython`). Esto es idiomático y
   **automatiza** el setup.
2. **A.2** Documentar ADR formal explicando por qué no usar
   `auth.Group` (referencia a ticket Django #29748).
3. **A.3** Considerar wrapper `OneToOneField` (Role → Group)
   como alternativa que preservaría compatibilidad con
   django-admin Group management.
4. **A.4** Verificar que el código real implementa custom
   permission backend (`get_all_permissions()` que retorne
   `Function` codes vinculadas via `AccessGroup`).

### Recomendación B — Migrar a `auth.Group` (refactor mayor)

Si el proyecto está en etapa temprana o se quiere alineamiento
estricto con Django:

1. **B.1** Reemplazar `Function` con `auth.Permission` (custom
   codenames via `Meta.permissions` en cada Model).
2. **B.2** Reemplazar `AccessGroup` con `auth.Group` + data
   migration que crea AGR-001..012.
3. **B.3** Para `is_system`: usar **proxy model** o **Group
   subclass** o admin-level enforcement (no
   `has_delete_permission` para grupos del sistema).
4. **B.4** Mantener `FunctionSeparationRule` (no hay
   alternativa nativa).
5. **B.5** Usar DRF `DjangoModelPermissions` directamente —
   eliminar permission classes custom innecesarias.

### Recomendación C — Hibrido (OneToOneField wrapper)

1. **C.1** Modelo `Role(group: OneToOneField(Group),
   is_system: bool, ...)`.
2. **C.2** `Function` permanece o migra a `auth.Permission`.
3. **C.3** SoD permanece custom.

## Comparación de recomendaciones

| Criterio | A. Mantener custom | B. Migrar a auth.Group | C. Hibrido OneToOne |
|---|---|---|---|
| Esfuerzo refactor | Bajo | Alto | Medio |
| Compatibilidad packages tercero | Baja | Alta | Alta |
| Mantenibilidad código backend | Media | Alta | Media-Alta |
| Reutilización Django admin | Baja | Alta | Alta |
| Riesgo de regresión | Bajo | Alto | Medio |
| Idiomático Django | Bajo | Alto | Medio |

## Decisión recomendada

**Para IACT-docs en su estado actual: Recomendación A**
(mantener custom + aplicar fixes idiomáticos).

Justificación:

1. El modelo `AccessGroup` ya está implementado, documentado y
   referenciado en ~80 archivos del corpus.
2. Migrar a `auth.Group` (B) implicaría refactor masivo del
   backend Y de la documentación que recién se acaba de
   estabilizar (sesión 2026-05-06).
3. El hibrido (C) introduce dos capas (Role + Group) que
   pueden confundir al lector. El IACT actual ya tiene
   `AccessGroup` solo, conceptualmente más simple.
4. Los fixes idiomáticos (A.1 data migration, A.2 ADR, A.4
   verificar backend) son **bajo costo** y eliminan los gaps
   más visibles vs Django.

**Punto crítico de A.1:** mover bootstrap a data migration es
**la mejora más rentable** (cambio pequeño, alineación grande
con Django idiomatic, reduce setup manual).

## Próximos pasos

1. **Stage 5 STRATEGY** del WP: documentar la decisión A en un
   ADR formal: `adr-back-007-rbac-custom-vs-auth-group.md`.
2. **TD-RBAC-01** (deuda técnica nueva): migrar bootstrap a
   data migration `RunPython`. Estimar ~2h backend.
3. **STD-014** (estándar nuevo opcional): documentar la
   convención IACT vs Django para futura referencia.

## Conclusión

El modelo AGR-NNN de IACT **no es Django idiomatic**, pero
**es defendible** si se justifica con ADR explícito y se
aplican los fixes A.1-A.4. La decisión de mantener custom
es razonable dado el estado actual del proyecto.

La única **mejora rentable inmediata** es migrar el bootstrap
de management command a data migration.
