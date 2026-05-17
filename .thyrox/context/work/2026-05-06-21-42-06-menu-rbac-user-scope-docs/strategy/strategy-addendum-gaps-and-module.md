```yml
created_at: 2026-05-06 23:55:00
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
phase: Phase 5 — STRATEGY
author: NestorMonroy
status: Borrador
version: 1.0.0
parent: strategy/menu-rbac-user-scope-solution-strategy.md
```

# Strategy Addendum — Gap resolution + D-MOD-001

> Adenda al `solution-strategy.md` que resuelve los 5 gaps
> identificados en review pre-gate Stage 5 → Stage 7 más
> la pregunta sobre necesidad de un módulo nuevo.

## Sección 1 — Decisión D-MOD-001: NO nuevo módulo MOD_MEN

**Decisión:** UC_ADM_04 y UC_ADM_05 viven en **MOD_Admin**.
Endpoint `GET /api/v1/menu/` permanece en **MOD_PERM**
(extensión de UC_PERM_08). No se crea MOD_MEN.

### Razonamiento

| Criterio | Resultado |
|---|---|
| Volumen | 2 UCs admin + 1 endpoint — bajo |
| Función de MOD_Admin v5.6.0 | "catch-all administrativo cross-module" — diseñado para esto |
| Slot reservado AGR-011/012 | Conservar para casos de mayor escala |
| CNST-029 (modelo plano) | Preservado sin presión |

### Trigger de revisión futura

Carving out a MOD_MEN solo si surge **una** de:

- i18n del catálogo con flujo editorial (>3 UCs).
- A/B testing o variantes por segmento.
- Auditoría de uso del menú como producto.
- Menu marketplace / customización por tenant.

### Localización canónica

| Artefacto | Módulo / app |
|---|---|
| `manage_menu_catalog` (UC_ADM_04) | MOD_Admin |
| `manage_menu_lifecycle` (UC_ADM_05) | MOD_Admin |
| `GET /api/v1/menu/` (UC_PERM_08 ext.) | MOD_PERM |
| Modelo `MenuItem` | `apps/access/` (mismo app que `Function`/`AccessGroup`) |

## Sección 2 — Gap #1: Renumeración P1-P4 inconsistente

### Tabla de correspondencia

| ID DISCOVER (final-decisions) | ID STRATEGY (solution-strategy) | Concepto |
|---|---|---|
| P1 | P1 | Diseño del modelo (wrapper UX, OneToOne, PROTECT, lifecycle) |
| P2 (cantidad de UCs) | — (resuelto en §6 STRATEGY como 2 UCs en MOD_Admin) | Cantidad de UCs |
| P3 (multi-tenancy) | — (resuelto en §6 STRATEGY como segment_id permanente, BR-012) | Multi-tenancy |
| P4 (cantidad de estados) | — (resuelto en §3 STRATEGY como 4 estados) | Estados del lifecycle |
| — | P2 | Contrato del endpoint flat |
| — | P3 | UserCapabilityResolver (P95 ≤ 20ms) |
| — | P4 | Política de cache (TTL 300s + invalidación explícita) |

**Convención adoptada:** la numeración P1-P4 de
`solution-strategy.md` es la canónica para Phase 7 en
adelante. Las P2/P3/P4 originales de DISCOVER ya fueron
absorbidas en otras secciones de STRATEGY.

## Sección 3 — Gap #2: Filtro STD-010 ampliado

**Reemplaza** el grep de `solution-strategy.md` §7:

```bash
grep -rE "bcrypt|\bReact\b|MySQL|MariaDB|Celery|mod_wsgi|simplejwt|\
OperationalError|IntegrityError|Pillow|Redis|PostgreSQL|\
\bDjango\b|DRF|\bJWT\b|\bPython\b|RabbitMQ|APScheduler|argon2|\
PBKDF2|Redux|Vue\.js|openpyxl|xlrd|pandas|nginx|gunicorn|Apache|\
secrets\.token_urlsafe" \
  source/requisitos/casos-uso/menu/ \
  --include="*.rst" \
  --exclude="implementacion-tecnica.rst" \
  --exclude="testing.rst"
```

Resultado vacío = conforme STD-010 §3.

**Nota:** el filtro corre por UC nuevo en Phase 7, NO sobre
todo el corpus (eso ya está cubierto por el WP hermano
`std-010-corpus-compliance`).

## Sección 4 — Gap #3: Política DEPRECATED — Auto-archive con opt-out

### Decisión

**Opción b — auto-archive con opt-out**, con condiciones
adicionales del ejecutor:

1. Pasados **90 días** en DEPRECATED, el Planificador de
   Tareas archiva automáticamente (transición DEPRECATED →
   ARCHIVED).
2. Para mantener el item en DEPRECATED indefinidamente, el
   `system_admin` (AGR-010) debe poner el flag
   `block_auto_archive=True` con un `block_reason` (CharField,
   obligatorio, ≥ 20 caracteres).
3. Cada cambio del flag genera entrada en audit log con
   `actor_id`, `block_reason`, `timestamp`.
4. Notificación previa: a los **80 días** el sistema envía
   warning "auto-archive en 10 días" al system_admin para
   permitir intervención.

### Modelo (extensión)

```python
class MenuItem(models.Model):
    # ... campos existentes ...
    block_auto_archive = models.BooleanField(default=False)
    block_reason = models.CharField(max_length=500, blank=True, default="")
    block_set_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.PROTECT,
        related_name="menu_items_archive_blocked",
    )
    block_set_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.block_auto_archive:
            if not self.block_reason or len(self.block_reason) < 20:
                raise ValidationError(
                    "block_reason obligatorio (≥ 20 chars) cuando "
                    "block_auto_archive=True"
                )
            if not self.block_set_by:
                raise ValidationError("block_set_by obligatorio")
```

### Job del Planificador de Tareas (lógica)

```
- Day 30:  warning a system_admin (>30d en DEPRECATED).
- Day 80:  pre-archive notification (auto-archive en 10 días).
- Day 90:  auto-archive si NOT block_auto_archive → ARCHIVED + audit.
- Day 90+: critical alert si block_auto_archive=True (visibilidad).
```

### Trade-off aceptado

Un admin puede mantener un item bloqueado para siempre, pero
ahora con responsabilidad trazable (audit log + block_reason
+ block_set_by). El sistema no decide políticamente; trazabilidad
sí garantiza.

## Sección 5 — Gap #4: AP-2 diferenciado (read vs critical write)

Reemplaza la tabla AP-2 de `solution-strategy.md` §5 con
**dos sub-patrones**:

### AP-2a — Read endpoints (eventual consistency)

| Capa | Verifica | Consistency |
|---|---|---|
| Frontend | Capabilities del token | Eventual (TTL 300s) |
| Endpoint backend | `UserCapabilityResolver` cached | Eventual (TTL 300s) |
| DB | — | — |

Todas las read capabilities (`view_*`, `list_*`, `get_*`)
usan AP-2a.

### AP-2b — Critical capability endpoints (cache bypass)

| Capa | Verifica | Consistency |
|---|---|---|
| Frontend | Capabilities del token | Eventual (UI puede mostrar) |
| Endpoint backend | `UserCapabilityResolver.resolve_uncached(user)` | **Strong (DB directo)** |
| DB | FK + check + audit | Strong |

**Trigger de AP-2b:** la `Function` consultada tiene
`is_critical=True` en el catálogo.

### Modelo Function (extensión)

```python
class Function(models.Model):
    codename = models.CharField(...)
    module = models.CharField(...)
    is_active = models.BooleanField(default=True)
    is_critical = models.BooleanField(
        default=False,
        help_text=(
            "Si True, la verificación de capability bypassa el "
            "cache y consulta DB en cada request. Reservado para "
            "capabilities de modificación de permisos o cambios "
            "estructurales irreversibles."
        ),
    )
```

### UserCapabilityResolver (dos métodos)

```python
class UserCapabilityResolver:
    @staticmethod
    def resolve(user) -> set[str]:
        """Cache-first. Para reads."""
        cached = cache.get(f"caps:user:{user.id}")
        if cached is not None:
            return cached
        codenames = UserCapabilityResolver._query_db(user)
        cache.set(f"caps:user:{user.id}", codenames, timeout=300)
        return codenames

    @staticmethod
    def resolve_uncached(user) -> set[str]:
        """DB-first. Para critical writes."""
        return UserCapabilityResolver._query_db(user)

    @staticmethod
    def has_capability(user, codename: str) -> bool:
        """Decide via is_critical del catálogo."""
        is_critical = Function.objects.filter(
            codename=codename, is_critical=True,
        ).exists()
        if is_critical:
            return codename in UserCapabilityResolver.resolve_uncached(user)
        return codename in UserCapabilityResolver.resolve(user)
```

### Catálogo inicial de `is_critical=True`

Capabilities que requieren bypass desde el día 1:

- `assign_functions` (modifica permisos de otros)
- `revoke_function_group` (modifica permisos de otros)
- `manage_menu_catalog` (modifica catálogo UX que afecta a todos)
- `manage_menu_lifecycle` (idem)
- `manage_function_catalog` (modifica el catálogo RBAC mismo)
- `manage_access_groups` (modifica composición AGR)
- Cualquier `delete_*` sobre entidades de RBAC.

> El catálogo definitivo se produce en Phase 7 al especificar
> UC_ADM_04 y la extensión de UC_PERM_08.

### Restricción de governance sobre `is_critical`

**Condición del ejecutor:** `is_critical` NO debe ser editable
por el mismo rol que gestiona el catálogo de funciones. De lo
contrario, un atacante con `manage_function_catalog`
comprometido podría marcar su propia capability como
`is_critical=False` antes de ser revocado.

**Mecanismo:** el flag `is_critical` se trata como una
constraint normativa — su modificación requiere:

1. Pull request al repositorio de migrations RBAC con review
   obligatoria (≥ 2 aprobaciones).
2. Aplicación vía Django RunPython data migration (canónica),
   no vía endpoint admin.
3. La interfaz admin de `Function` muestra `is_critical` como
   read-only.
4. Capability dedicada `manage_critical_function_flag`
   restringida a un AGR especial (e.g., AGR-013 reservado para
   "RBAC governance" — usa uno de los slots reservados
   AGR-011/012 si se aprueba; alternativa: hardcoded a un
   superuser específico).

> Decisión sobre AGR-013 vs hardcoded: pendiente para Phase 7
> (ADR-BACK-010 nuevo). Mientras tanto, en Phase 7 se documenta
> como "ningún rol del catálogo v5.6.0 tiene
> `manage_critical_function_flag`; cambios solo via migration".

## Sección 6 — Gap #5: DAG de paralelismo Phase 7

```
                                                ┌──── (8) cache-strategy.rst
                                                │
                          ┌─── (2) ADR-BACK-009 ─┘
                          │
[paralelo desde inicio]   ├─── (10) ADR-BACK-010 (is_critical governance)
                          │
                          └─── (1) ADR-BACK-008 ─┬──── (3) CNST-032 v2.0.0
                                                  │
                                                  ├──── (4) rbac-impl-guide §Q9 ext
                                                  │      │
                                                  │      └──── (5) UC_ADM_04 ─── (6) UC_ADM_05 ──── (9) scheduled-tasks.rst
                                                  │                │
                                                  └──── (7) UC_PERM_08 ext (necesita AP-2b decisión: ya cerrada en §5 de este addendum)
```

### Lotes de ejecución

| Lote | Artefactos | Bloqueantes |
|---|---|---|
| L1 (paralelo) | (1) ADR-BACK-008, (2) ADR-BACK-009, (10) ADR-BACK-010 | Ninguno |
| L2 (paralelo) | (3) CNST-032 v2.0.0, (4) rbac-impl-guide §Q9 ext, (8) cache-strategy.rst | L1 |
| L3 | (5) UC_ADM_04, (7) UC_PERM_08 ext | L2 |
| L4 | (6) UC_ADM_05 | L3 (solo (5)) |
| L5 | (9) scheduled-tasks.rst | L4 |

10 artefactos en lugar de 9 (se agrega ADR-BACK-010 por
gap #4 sub-decisión).

### Estimación

Con paralelismo: 5 lotes en serie. Sin paralelismo: 10 commits
secuenciales. Reducción aproximada del 50% en tiempo de Phase 7
si los lotes paralelos efectivamente se ejecutan concurrentes.

## Sección 7 — Resumen de los 5 gaps + módulo

| Gap / Pregunta | Resolución | Sección |
|---|---|---|
| ¿MOD_MEN nuevo? | NO — D-MOD-001 (UC_ADM_04/05 en MOD_Admin) | §1 |
| #1 Renumeración P1-P4 | Tabla de correspondencia + convención canónica STRATEGY | §2 |
| #2 Filtro STD-010 incompleto | Grep ampliado con PostgreSQL/Django/DRF/JWT/Python + más | §3 |
| #3 DEPRECATED authority | Auto-archive con opt-out + `block_auto_archive` con `block_reason` obligatorio + audit log + warning a 80d | §4 |
| #4 Cache writes/critical | AP-2a (reads, eventual) + AP-2b (critical, bypass DB) + `Function.is_critical` con governance especial | §5 |
| #5 Paralelismo Phase 7 | DAG de 10 artefactos en 5 lotes | §6 |

## Sección 8 — ADRs adicionales para Phase 7

Por las decisiones de gap #3 y gap #4, se agrega **ADR-BACK-010**
al roadmap original de 9 artefactos:

| ADR | Tema | Fuente |
|---|---|---|
| ADR-BACK-008 | MenuItem wrapper UX | KI-1 + P1 |
| ADR-BACK-009 | Cache degraded mode | P4 |
| **ADR-BACK-010** (nuevo) | `Function.is_critical` + AP-2b + governance del flag | gap #4 |

## Sección 9 — Constraints actualizadas

Esta adenda agrega evidencias de cumplimiento adicionales:

| Constraint | Evidencia adicional en este addendum |
|---|---|
| CNST-029 (modelo plano) | D-MOD-001 confirma sin nuevos módulos sin justificación |
| BR-010 (audit) | gap #3 — block_set_by + block_set_at + audit log |
| ADR-BACK-007 (custom RBAC) | gap #4 — `Function.is_critical` extiende modelo custom, no `auth.Permission` |
| STD-010 | gap #2 — filtro pre-commit ampliado |

## Sección 10 — Exit criteria — actualización

`solution-strategy.md` §12 sigue válido + estos checks:

- [x] D-MOD-001 documentada (no MOD_MEN).
- [x] Correspondencia P1-P4 DISCOVER ↔ STRATEGY explícita.
- [x] Filtro STD-010 ampliado.
- [x] Política DEPRECATED resuelta con opt-out trazable.
- [x] AP-2 diferenciado (a/b) con catálogo inicial de
  `is_critical=True`.
- [x] DAG Phase 7 con paralelismo en 5 lotes.

**Phase 5 STRATEGY cerrada.** Listo para gate Stage 5 → Stage 7.

## Refs

- `strategy/menu-rbac-user-scope-solution-strategy.md` (parent).
- Review pre-gate del ejecutor (mensaje 2026-05-06 23:50).
- WP hermano `2026-05-06-23-25-08-std-010-corpus-compliance`.
- Catálogo de Function v5.6.0 (capabilities críticas iniciales).
