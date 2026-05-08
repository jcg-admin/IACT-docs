```yml
project: IACT-docs
work_package: 2026-05-08-03-08-21-wpg-std010-cleanup
created_at: 2026-05-08 03:08:21
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (re-audit muestra ~80-100 ediciones in-scope tras refinamiento, ~270 en normativa diferidas)
target: WP-G del roadmap. Aplica STD-010 vocabulario canonico. D2 ya redujo el scope ~40% al exentar _metodologia-aplicacion/. Re-audit detecta que normativa/procedimientos/ y ADRs gobernanza requieren clarificacion adicional de scope: documentan decisiones tecnologicas que necesitan mencionar tecnologia concreta (Redis prohibido, MySQL para sesiones, etc.). Este WP procesa los archivos claramente in-scope y abre TD-D5 para clarificar §2.5 normativa/procedimientos/.
predecessor_wp: 2026-05-08-02-36-43-wpe-factory-builder-manager (cerrado)
trigger: directiva del ejecutor "Procede con WP-G ahora"
```

# WP-G — STD-010 vocabulario tecnico cleanup

## Re-audit del scope post-D2

Tras aplicar exclusiones D2 (`_metodologia-aplicacion/`,
`arquitectura-tecnica/**`, `backend/**`,
`implementacion-tecnica.rst`, std-010 misma):

| Subdir | Refs no-exempt |
|---|---|
| `normativa/` | **270** ⚠ |
| `gestion/` | 39 |
| `base-cognitiva/` (no taxonomias) | 26 |
| `requisitos/casos-uso/` | 6 |
| `requisitos/reglas-negocio/` | 4 |
| `source/index.rst` | 5 |
| **Total** | **~350** |

## Hallazgo: refinamiento adicional necesario en `normativa/`

Las 270 refs en `normativa/` se concentran en archivos que
**necesitan** mencionar tecnologia concreta para cumplir su
proposito:

| Archivo | Refs | Naturaleza |
|---|---|---|
| `gobernanza/adr-gob-010-rbac-autorizacion-drf-backend.rst` | 37 | ADR backend (tecnologico por definicion) |
| `procedimientos/proced-gob-001-crear-adr.rst` | 26 | Plantilla de ADR (incluye ejemplos tecnologicos) |
| `procedimientos/proc-devops-001-devops-automation.rst` | 23 | DevOps automation (necesita CI/CD tools) |
| `procedimientos/proc-gob-002-gobernanza-sdlc.rst` | 12 | "Redis prohibido", "MySQL para sesiones" — decisiones tecnologicas |
| `procedimientos/guia-completa-desarrollo-features.rst` | 12 | Guia tecnica de desarrollo |
| `estandares/plantillas/tpl-uc-temporal-schedulers.rst` | 11 | Plantilla con ejemplos backend |
| `estandares/plantillas/tpl-mod-modulos.rst` | 9 | Plantilla de modulos (tecnica) |
| `procedimientos/proc-dev-004-diseno-tecnico.rst` | 8 | Procedimiento de diseno tecnico |
| ... | | |

**Estos archivos son operacionales/arquitectonicos**, no
narrativa de requisitos UC. Aplicar STD-010 aqui rompe el
proposito documental: un procedimiento DevOps NECESITA decir
"Redis" para documentar que se prohibe; un ADR backend
NECESITA decir "Django REST Framework" para documentar la
decision.

## Decision para este WP (TD-D5 propuesta)

Aplicar STD-010 a archivos **claramente in-scope**:

✅ **In-scope WP-G:**

- `requisitos/casos-uso/**/{flujo-principal,actores-precondiciones,
  criterios-aceptacion,datos-involucrados,informacion-general,
  patrones-diseno,requisitos-no-funcionales,excepciones,
  diagramas-uml.rst}` — narrativa de UC.
- `requisitos/reglas-negocio/**` (excepto refs a sistemas
  externos por D2 §2.4).
- `requisitos/business-requirements/**`.
- `base-cognitiva/_fundamentos-conceptuales/**` —
  vocabulario conceptual.
- `base-cognitiva/_uml/**` — material pedagogico.
- `base-cognitiva/_metadata/**` — metadata del proyecto.
- `gestion/evidencia/rbac-historia/**` — analisis historico
  RBAC (excepto cuando documenta sistemas externos).
- `source/index.rst` raiz — revisar por contenido.

🚫 **Out-of-scope (TD-D5 — clarificar STD-010 §2.5):**

- `normativa/procedimientos/**` — procedimientos DevOps,
  diseño técnico, gobernanza SDLC.
- `normativa/gobernanza/adr-*.rst` — Architecture Decision
  Records (documentan decisiones tecnologicas).
- `normativa/estandares/plantillas/**` — plantillas con
  ejemplos backend.
- `gestion/evidencia/arquitectura-modular/**` — analisis
  arquitectonico tecnico.

**TD-D5 propuesta:** abrir un nuevo WP `naming-rules-resolution-d5`
para que el ejecutor decida si STD-010 §2 debe ampliarse con
una clausula §2.5 que exenta `normativa/procedimientos/`,
`normativa/gobernanza/adr-*`, plantillas técnicas, y analisis
arquitectonico (paralelo a la exencion §2.3 de
`_metodologia-aplicacion/`). Esa decision afecta ~270 refs
adicionales.

## Scope final estimado de este WP-G

~80-100 ediciones in-scope estricto:

| Subdir | Refs in-scope |
|---|---|
| `requisitos/casos-uso/` | 6 |
| `requisitos/reglas-negocio/` | 4 |
| `base-cognitiva/_fundamentos-conceptuales/` | 8 |
| `base-cognitiva/_uml/` | 6 |
| `base-cognitiva/_metadata/` | 12 |
| `gestion/evidencia/rbac-historia/` | ~20 |
| `source/index.rst` | 5 |
| `normativa/estandares/std-008..013` (no plantillas) | ~20 (revisar contexto) |
| **Total** | **~80** |

## Tabla de transformacion

Vocabulario STD-010 v1.1.0 §3:

| Termino tecnico | Vocabulario canonico |
|---|---|
| `PostgreSQL` | el repositorio operacional / Almacen de Datos |
| `MariaDB`, `MySQL` | el repositorio / la base de datos |
| `Redis` | el servicio de cache |
| `Celery` | el Procesador Asincrono |
| `Django` | el Framework de Aplicacion / Servicio de Aplicacion |
| `React` | la Interfaz de Usuario |
| `Vue.js` | la Interfaz de Usuario |

## Restricciones

- NO modificar archivos out-of-scope (esperar TD-D5).
- Preservar refs a sistemas externos del cliente (D2 §2.4).
- Preservar narrativa "JWT" "RBAC" disciplinar (D4 §5.4).
- Strict build pendiente al final de cola.

## Stopping points

- **SP-01:** revisar antes de cierre.
- **SP-02:** abrir TD-D5 para scope ampliado.

## Refs

- WP `clean-code-naming-audit` (audit-only).
- WP `naming-rules-resolution` (D2 + D4 aplicadas).
- STD-010 v1.1.0 §2, §3, §5.4, §5.5.
