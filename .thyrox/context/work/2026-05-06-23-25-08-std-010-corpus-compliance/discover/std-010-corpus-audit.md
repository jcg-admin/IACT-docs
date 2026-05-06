```yml
created_at: 2026-05-06 23:30:00
project: IACT-docs
work_package: 2026-05-06-23-25-08-std-010-corpus-compliance
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# STD-010 — Auditoría exhaustiva del corpus

## Trigger

Continuación del audit
``2026-05-06-21-42-06-menu-rbac-user-scope-docs/discover/std-010-vocabulario-abstracto-audit.md``.
Ejecutor pidió: *"realiza todas las correcciones, pero
para ello, crea un nuevo wp, realizando un análisis"*.

## Sección 1 — Metodología

Comando canónico de STD-010 §6 + extensiones para términos
relevantes:

```bash
grep -rnE "bcrypt|React|MySQL|MariaDB|Celery|mod_wsgi|simplejwt|\
OperationalError|Pillow|Redis|Apache|nginx|gunicorn|Vagrant|\
PostgreSQL|RabbitMQ|APScheduler|argon2|PBKDF2|Redux|Vue\.js|\
openpyxl|xlrd|pandas|secrets\.token_urlsafe|IntegrityError" \
  source/requisitos/casos-uso/ \
  --include="*.rst" \
  --exclude="implementacion-tecnica.rst"
```

**17 hits brutos. Tras filtrar falsos positivos** ("Reactivar"
verbo español confundido con "React"), quedan **9 hits reales**
distribuidos en 7 archivos.

## Sección 2 — Interpretación de ámbito ambiguo

STD-010 §2 lista 9 archivos en ámbito y 2 fuera de ámbito.
**No menciona:**

- `testing.rst` (contiene código de tests).
- `diagramas-uml/diagrama-de-*.rst` (subdivisión de
  `diagramas-uml.rst` listado en §2).

### Decisión interpretativa

| Archivo | Decisión | Justificación |
|---|---|---|
| `testing.rst` | **Libre** (analogía con `implementacion-tecnica.rst`) | Contiene código de pytest/jest que requiere nombres de excepción reales (`IntegrityError`, `bcrypt.checkpw`). Aplicar STD-010 obligaría a re-escribir tests. |
| `diagramas-uml/diagrama-de-secuencia.rst` | **En ámbito** (extensión natural de `diagramas-uml.rst`) | STD-010 §4 da reglas explícitas sobre participantes; éstas se aplican a cualquier subarchivo que defina diagramas. |
| `diagramas-uml/diagrama-de-actividad.rst` | **En ámbito** (mismo motivo) | Idem. |

Esta decisión se documenta como **propuesta de aclaración
de STD-010** que el ejecutor puede aprobar o rechazar.
Si rechaza, los hits de `testing.rst` (5 ítems) entran en
scope y deben corregirse en una pasada futura.

## Sección 3 — Inventario de violaciones (Tier 1: clear)

Hits dentro de ámbito explícito o derivado, con término
canónico STD-010:

| # | Archivo | Línea | Encontrado | Canónico STD-010 §3 |
|---|---|---|---|---|
| H-1 | `auth/uc-auth-02/criterios-aceptacion.rst` | 156 | ``Redux state.auth.isAuthenticated == false`` | `Gestor de Estado refleja sesión no autenticada` |
| H-2 | `auth/uc-auth-02/flujo-principal.rst` | 219 | "limpia state de Redux" | "limpia state del Gestor de Estado" |
| H-3 | `auth/uc-auth-02/diagramas-uml/diagrama-de-secuencia.rst` | 36 | ``localStorage.clear\nRedux clear`` | "limpia almacenamiento local\nlimpia Gestor de Estado" |
| H-4 | `users/uc-usr-01/flujos-alternos.rst` | 55 | ``IntegrityError (UNIQUE violation...)`` | "error de integridad de datos (UNIQUE violation...)" |
| H-5 | `reports/uc-inc-rpt-01/datos-involucrados.rst` | 27 | ``(PostgreSQL — base operacional IACT)`` | "(repositorio operacional IACT)" |
| H-6 | `reports/uc-rpt-03/datos-involucrados.rst` | 48 | "(PostgreSQL — tablas de usuarios, RBAC)" | "(repositorio operacional — tablas de usuarios, RBAC)" |

## Sección 4 — Inventario fuera de ámbito (Tier 2)

Hits en `testing.rst` (libre por interpretación de §2):

| # | Archivo | Línea | Término | Acción |
|---|---|---|---|---|
| T-1 | `auth/uc-auth-01/testing.rst` | 237, 240 | `IntegrityError` (en `pytest.raises`) | Sin cambio |
| T-2 | `auth/uc-auth-04/testing.rst` | 55, 70 | `bcrypt.checkpw`, `import bcrypt` | Sin cambio |
| T-3 | `auth/uc-auth-03/testing.rst` | 63 | `import bcrypt` | Sin cambio |

## Sección 5 — Hits no listados como prohibidos por STD-010

Términos que aparecen en el corpus pero **no están en la
tabla §3 de STD-010**:

| Término | Apariciones | Status |
|---|---|---|
| `localStorage` | 21+ en uc-auth-01, uc-auth-02 | No prohibido literalmente; el ejecutor lo mencionó pero STD-010 no lo lista |
| `Frontend` (sin "(React)") | múltiples | Solo "Frontend (React)" está prohibido en §3.4 |
| `Backend` | múltiples | No listado |
| `API` | múltiples | No listado |
| `Django` (solo) | varios | No listado en STD-010; "Django API" sí (en §4 ejemplo) |

**Recomendación:** abrir un WP separado *std-010-extension*
para discutir si STD-010 §3 debe ampliarse con
`localStorage`, `Backend`, `API`, `Frontend` (alone), antes
de actuar sobre estos hits. NO los corregimos en este WP.

## Sección 6 — Violación adicional en WP padre

| # | Archivo | Línea | Encontrado | Acción |
|---|---|---|---|---|
| H-7 | `2026-05-06-21-42-06-menu-rbac-user-scope-docs/discover/final-decisions-p1-p4-and-pending-items.md` | 417, 492 | "Job Celery beat" + código `@celery_app.task` | Reformular como "Planificador de Tareas" + código en bloque marcado como "decisión técnica → arquitectura-tecnica/" |

**Justificación de la corrección a un artefacto WP:**
STD-010 §2 no incluye `.thyrox/context/work/`, pero la
decisión propaga a Phase 7 DESIGN. Corrigiendo la
formulación AHORA evita arrastrar el término prohibido a la
narrativa UC futura.

## Sección 7 — Plan de correcciones

| Paso | Acción | Archivos |
|---|---|---|
| C-1 | Aplicar H-1..H-3 en uc-auth-02 | criterios-aceptacion.rst, flujo-principal.rst, diagramas-uml/diagrama-de-secuencia.rst |
| C-2 | Aplicar H-4 en uc-usr-01 | flujos-alternos.rst |
| C-3 | Aplicar H-5..H-6 en reports | uc-inc-rpt-01/datos-involucrados.rst, uc-rpt-03/datos-involucrados.rst |
| C-4 | Aplicar H-7 en WP padre | final-decisions-p1-p4-and-pending-items.md |
| V-1 | Verificación post-fix con grep §6 | source/requisitos/casos-uso/ |
| V-2 | Build Sphinx strict (regresión) | make html SPHINXOPTS='-W -j auto' |

## Sección 8 — Acciones siguientes (post-WP)

1. **Cierre de este WP** (Phase 11 TRACK).
2. **Retomar WP padre `2026-05-06-21-42-06-menu-rbac-user-scope-docs`**
   en Phase 5 STRATEGY:
   produce `strategy/menu-rbac-user-scope-solution-strategy.md`
   con Key Ideas, Fundamental Decisions (P1-P4), Technology
   Stack, Architecture Patterns, Adherence to Constraints
   (BR-012, CNST-029, CNST-032, ADR-BACK-001/007),
   Traceability + evidence classification.

## Refs

- Audit padre: `2026-05-06-21-42-06-menu-rbac-user-scope-docs/discover/std-010-vocabulario-abstracto-audit.md`.
- STD-010: :doc:`/normativa/estandares/std-010-vocabulario-abstracto`.
- D-ETL-005 (origen "soda machine rule"): WP histórico
  ``source-corrections-pipeline``.
- D-KRUCHTEN-004 (Kruchten views): WP histórico
  ``kruchten-view-diagram-types``.
