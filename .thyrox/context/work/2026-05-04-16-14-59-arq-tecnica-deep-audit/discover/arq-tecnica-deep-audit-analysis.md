```yml
created_at: 2026-05-04 16:14:59
project: THYROX
work_package: 2026-05-04-16-14-59-arq-tecnica-deep-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Análisis profundo — source/arquitectura-tecnica/ (post WPs 1-4)

Análisis adversarial de 6 capas sobre los 214 archivos RST de
`source/arquitectura-tecnica/` tras la ejecución de los WPs:

- WP `uml-coverage-housekeeping` — bc-*.rst eliminados, system-view/ renombrado, alias PlantUML corregidos
- WP `uml-coverage-context-view` — context-view/ creado
- WP `uml-coverage-operational-view` — operational-view/ creado
- WP `uml-coverage-perspectivas` — perspectivas/ creado

---

## Inventario verificado (PROVEN)

```
find source/arquitectura-tecnica -name "*.rst" | wc -l → 214 archivos RST
```

Subdirectorios principales:

| Directorio | Archivos RST |
|---|---|
| arquitectura-sistema/ | 3 |
| context-view/ | 4 |
| deploy-view/ | 4 |
| design-view/ | 13 |
| domain-model/ | 28 (index + overview + 26 clases) |
| implementation-view/ | 13 |
| modulos/ (11 subdirectorios) | ~80 |
| operational-view/ | 5 |
| perspectivas/ | 4 |
| process-view/ | 5 |
| rbac/ | 12 |
| system-view/ | 13 |
| use-case-view/ | 14 |
| raíz (*.rst sueltos) | 6 |

---

## F-01 — CRÍTICA · Naming inconsistente de módulos entre vistas

**Origen:** PROVEN — `ls` de los tres directorios comparados con `comm`

Los mismos módulos funcionales tienen nombres de archivo distintos en cada vista:

| Módulo canónico | use-case-view | design-view | implementation-view |
|---|---|---|---|
| MOD_Logs | `mod-logs.rst` | `mod-sys-logs.rst` | `mod-sys-logs.rst` |
| MOD_Operator | `mod-operator.rst` | `mod-operator-calls.rst` | `mod-operator-calls.rst` |
| MOD_Pipeline | `mod-pipeline.rst` | `mod-etl-monitoring.rst` | `mod-etl-monitoring.rst` |
| MOD_Reports | `mod-reports.rst` | `mod-vis-reports.rst` | `mod-vis-reports.rst` |
| MOD_Users | `mod-users.rst` | `mod-user-identity.rst` | `mod-users.rst` |

Adicionalmente, `implementation-view` usa `mod-users.rst` pero `design-view` usa
`mod-user-identity.rst` para el mismo módulo — inconsistencia entre las dos vistas
técnicas entre sí.

**Decisión pendiente:** el nombre canónico debe ser el de `use-case-view` (nombres
de negocio: `mod-logs`, `mod-operator`, `mod-pipeline`, `mod-reports`, `mod-users`)
ya que esa vista define el vocabulario funcional del sistema.

**Archivos afectados por renombre (design-view):**
- `design-view/mod-sys-logs.rst` → `design-view/mod-logs.rst`
- `design-view/mod-operator-calls.rst` → `design-view/mod-operator.rst`
- `design-view/mod-etl-monitoring.rst` → `design-view/mod-pipeline.rst`
- `design-view/mod-vis-reports.rst` → `design-view/mod-reports.rst`
- `design-view/mod-user-identity.rst` → `design-view/mod-users.rst`

**Archivos afectados por renombre (implementation-view):**
- `implementation-view/mod-sys-logs.rst` → `implementation-view/mod-logs.rst`
- `implementation-view/mod-operator-calls.rst` → `implementation-view/mod-operator.rst`
- `implementation-view/mod-etl-monitoring.rst` → `implementation-view/mod-pipeline.rst`
- `implementation-view/mod-vis-reports.rst` → `implementation-view/mod-reports.rst`

**Referencias que actualizan automáticamente:**
- `design-view/index.rst` toctree
- `implementation-view/index.rst` toctree
- Cualquier `:doc:` o `seealso` que apunte a los nombres anteriores

---

## F-02 — ALTA · `mod-caller` ausente en design-view e implementation-view

**Origen:** PROVEN — `ls design-view/mod-*.rst` + `ls implementation-view/mod-*.rst`

`use-case-view/mod-caller.rst` existe (MOD_Caller — Experiencia del Cliente IVR:
comportamiento del llamante externo en el flujo IVR). Ni `design-view/` ni
`implementation-view/` tienen el módulo equivalente.

`design-view/mod-operator-calls.rst` menciona "caller" en contexto del operador
pero describe la perspectiva del agente, no del caller externo. No es sustituto.

**Acción:** crear `design-view/mod-caller.rst` e `implementation-view/mod-caller.rst`
con el patrón canónico de secuencia/componentes para MOD_Caller.

---

## F-03 — ALTA · "Django" sin "REST Framework" en 6 archivos

**Origen:** PROVEN — `grep -rn "Django\b"` filtrado por ausencia de "REST Framework"

```
context-view/external-interfaces.rst:103
  → rectangle "IACT App\n(Django)" as App
  → CORREGIR: "IACT App\n(Django REST Framework)"

context-view/context-diagram.rst:28
  → "Aplicacion Django (12 modulos funcionales..."
  → CORREGIR: "Aplicacion Django REST Framework"

operational-view/system-configuration.rst:41
  → "Embebido en el proceso Django."
  → CORREGIR: "Embebido en el proceso Django REST Framework."

operational-view/system-support.rst:112
  → "Estado de servicios clave (Django app, ETL service..."
  → CORREGIR: "... (Django REST Framework app, ETL service..."

operational-view/index.rst:46
  → "migraciones Django"
  → CORREGIR: "migraciones Django REST Framework"

perspectivas/perspectiva-availability.rst:107,167
  → "proceso Django" / "Proceso Django caido"
  → CORREGIR: "proceso Django REST Framework" / "Proceso DRF caido"
```

---

## F-04 — ALTA · Conteo incorrecto de Bounded Contexts y clases

**Origen:** PROVEN — `grep "bounded\|siete\|26 clases"` en domain-model/index.rst
y modelo-dominio-iact.rst; conteo del toctree de domain-model/index.rst

El toctree real de `domain-model/index.rst` lista **8 BCs**:
Auth, RBAC, Calls, Reports, Pipeline ETL, Alerts, Audit, Logs.

Las clases reales en disco: **26** (verificado con `ls domain-model/*.rst | grep -v index|overview | wc -l`).

**Inconsistencias encontradas:**

| Archivo | Línea | Texto actual | Corrección |
|---|---|---|---|
| `domain-model/index.rst` | 20 | `"26 clases en 7 bounded contexts"` | `"26 clases en 8 bounded contexts"` |
| `modelo-dominio-iact.rst` | 39 | `"siete bounded contexts"` + `"25 clases"` | `"ocho bounded contexts"` + `"26 clases"` |
| `modelo-dominio-iact.rst` | 129 | `"26 clases en 8 bounded contexts"` | ✓ correcto |
| `domain-model/overview.rst` | (revisar) | posiblemente "7" o "25" | verificar y corregir |

---

## F-05 — MEDIA · Aliases cortos en perspectiva-regulation.rst

**Origen:** PROVEN — `grep " as API\| as BL\| as RBAC\| as AUDIT"` en perspectiva-regulation.rst:130-133

```plantuml
participant "DRF\nAPI"             as API    ← corto
participant "RBAC\nMiddleware"     as RBAC   ← corto
participant "Business\nLogic"      as BL     ← muy corto
participant "AuditEvent\n(append-only)" as AUDIT ← corto
```

Todos están declarados y usados sin rotura PlantUML. Sin embargo, el principio
establecido en la corrección de `system-administration.rst` (sesión anterior) exige
aliases SCREAMING_SNAKE_CASE auto-descriptivos.

**Corrección:**
```plantuml
participant "DRF\nAPI"             as DRF_API
participant "RBAC\nMiddleware"     as RBAC_MIDDLEWARE
participant "Business\nLogic"      as BUSINESS_LOGIC
participant "AuditEvent\n(append-only)" as AUDIT_EVENT
```

Y actualizar las flechas correspondientes.

---

## F-06 — MEDIA · Doble título idéntico en pipeline-datos-ivr-caller.rst

**Origen:** PROVEN — `grep -n "^Pipeline\|^===" pipeline-datos-ivr-caller.rst`

```
modulos/caller/diagramas/pipeline-datos-ivr-caller.rst:15-20

  ==========================================
  Pipeline de Datos IVR — Caller a Analitica   ← título h1 (overline+underline)
  ==========================================

  Pipeline de Datos IVR — Caller a Analitica   ← repetido como sección h2
  ============================================
```

El texto es idéntico. La segunda ocurrencia es redundante. Eliminar la sección h2
o reemplazarla por una descripción introductoria.

---

## F-07 — BAJA · system-view/ sin toctree principal (pre-existing)

**Origen:** PROVEN — `grep -rn "system-view"` + build warnings

`diagramas-uml-sistema.rst` incluye `system-view/` en su toctree, pero ese archivo
RST no está incluido en `arquitectura-tecnica/index.rst` ni en `vistas-kruchten.rst`.
Genera el `toc.not_included` WARNING pre-existente para `system-view/index.rst`.

**Nota:** este es un warning pre-existing (existía antes de los WPs 1-4). No introducido
por cambios recientes. Requiere decisión sobre si `system-view/` se mantiene como
sección independiente o se integra a `vistas-kruchten.rst`.

---

## Criterios de aceptación del WP correctivo

- [ ] F-01: 9 archivos renombrados en design-view e implementation-view, toctrees actualizados
- [ ] F-02: 2 archivos nuevos creados (design-view/mod-caller.rst, implementation-view/mod-caller.rst)
- [ ] F-03: 6 menciones "Django" corregidas a "Django REST Framework"
- [ ] F-04: 3 cifras corregidas en domain-model/index.rst y modelo-dominio-iact.rst
- [ ] F-05: 4 aliases renombrados en perspectiva-regulation.rst
- [ ] F-06: Doble título eliminado en pipeline-datos-ivr-caller.rst
- [ ] F-07: SPECULATIVE — fuera de scope de este WP (decisión de arquitectura)
- [ ] Build verde sin warnings nuevos tras todas las correcciones

## Orden de ejecución (DAG)

```
F-04 (texto) → inmediato, sin dependencias
F-06 (texto) → inmediato, sin dependencias
F-03 (texto) → inmediato, sin dependencias
F-05 (PlantUML) → inmediato, sin dependencias
F-01 (renombres) → requiere: git mv + actualizar toctrees
F-02 (archivos nuevos) → requiere: F-01 completado (nombres canónicos establecidos)
```
