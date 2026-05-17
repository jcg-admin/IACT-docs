```yml
created_at: 2026-05-08 04:00:00
project: IACT-docs
work_package: 2026-05-08-03-08-21-wpg-std010-cleanup
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — WP-G (STD-010 vocabulario tecnico cleanup)

## [1.0.0] — 2026-05-08

### Changed (36 ediciones en 4 commits)

#### Bloque 1 — `gestion/evidencia/rbac-historia/**` (17 refs, 6 archivos)

| Sustitución | Conteo |
|---|---|
| `Modelos Django` → `Modelos del backend` | 3 |
| `Django Admin` / `Django Admin Integration` → `panel administrativo del backend` | 4 |
| `Django Management Commands` → `Comandos de gestión del backend` | 1 |
| `(Django builtin)` → `(builtin del Servicio de Aplicación)` | 1 |
| `(modelo Django)` / `(Django model)` / `(Django)` → `(modelo del backend)` | 3 |
| `8 modelos Django` / `3 migraciones Django` → `... del backend` | 4 |
| `no Redis` → `no en cache distribuido` | 1 |
| `(PostgreSQL):` → `(Almacén de Datos analítico):` | 1 |

#### Bloque 2 — `base-cognitiva/_fundamentos-conceptuales/**` (4 refs, 2 archivos)

| Sustitución | Archivo |
|---|---|
| `PostgreSQL Analytics (Sistema Analítico)` → `Almacén de Datos Analítico (Sistema IACT)` | fnd-00 |
| `Aplicación Web Django + React` → `Aplicación Web (Backend + Interfaz UI)` | fnd-00 |
| `MySQL IVR + PostgreSQL Analytics` → `MySQL IVR (externo) + Almacén Analítico IACT` | fnd-00 |
| `desde MySQL hacia PostgreSQL` → `desde el Repositorio operativo IVR hacia el Almacén de Datos analítico` | fnd-02 |

#### Bloque 3 — `base-cognitiva/_uml/**` (5 refs, 3 archivos)

| Sustitución | Archivo |
|---|---|
| `Apache + Django` → `Servidor de Aplicación` | cuando-usar/diagrama-de-distribucion |
| `database "MySQL"` → `database "Almacén de Datos"` | cuando-usar/diagrama-de-distribucion |
| `database "PostgreSQL"` → `database "Almacén de Datos"` | uml-01/diagrama-de-distribucion |
| `stack PostgreSQL + Node.js` → `stack del Almacén de Datos y del Servicio de Aplicación` | uml-14/concerns |
| `PostgreSQL para audit_log... Node.js para API` → `el Almacén de Datos... el Servicio de Aplicación para la API` | uml-14/concerns |
| `audit_log en PostgreSQL` → `audit_log en el Almacén de Datos` | uml-14/concerns |

#### Bloque 4 — admin/uc-adm-02 + reglas-negocio/rbac (3 refs, 2 archivos)

| Sustitución | Archivo |
|---|---|
| `via migraciones Django` → `via migraciones del backend` | uc-adm-02/informacion-general |
| `(modelo Django)` → `(modelo del backend)` | uc-adm-02/informacion-general |
| `via Django RunPython data migration` → `via data migration del backend` | rbac/catalogo-funciones |
| `Read-only en admin Django` → `Read-only en el panel administrativo del backend` | rbac/catalogo-funciones |

### Preserved (excepciones STD-010)

#### §2.4 — Sistemas externos (6 refs)

- `br-001-fuente-operacional-inmutable.rst:48,57` — "MySQL del sistema IVR" (sistema IVR es externo del cliente)
- `fnd-00-contexto-y-jerarquia.rst:126` — "MySQL IVR (Sistema Operacional)"
- `fnd-02-reglas-de-negocio.rst:693` — "BD MySQL operacional" (refiere a IVR)
- `fnd-03-casos-de-uso.rst:250` — "Sistema IVR MySQL"
- `fnd-05-jerarquia-4-niveles.rst:624` — "BD MySQL operacional"
- `_uml/cuando-usar/diagrama-de-distribucion.rst` — "Stripe API" (servicio externo)

#### Diferidos a TD-D5 — Project identity files (18 refs)

Los siguientes archivos contienen **declaración de identidad del
proyecto** o **arquitectura técnica de producto** y requieren
ampliar STD-010 §2.5 antes de ser tocados (paralelo a la exención
§2.3 de `_metodologia-aplicacion/`):

- `base-cognitiva/_metadata/meta-01-identidad-proyecto.rst` (9 refs):
  declaración formal del stack — Backend/Frontend/BD/Cache/Mensajería.
- `base-cognitiva/_metadata/meta-05-estructura-documental.rst` (3 refs):
  estructura documental con stack de referencia.
- `source/index.rst` (5 refs): landing page del proyecto con
  arquitectura introductoria.
- `requisitos/casos-uso/**/testing.rst` (3 archivos): documentación
  de infraestructura de tests; clasificación equivalente a
  `implementacion-tecnica.rst` (§5.1) pero no listada en §2.1.

Razón: aplicar STD-010 a "Backend: Django REST Framework" produce
"Backend: el Framework de Aplicación" (circular — el archivo
declara qué framework es el backend; abstraerlo elimina la
información). Mismo patrón que `normativa/procedimientos/` que ya
fue identificado como necesitar TD-D5.

### Verification

```bash
# Refs in-scope post-D2 + D4 + WP-G
$ grep -rEn '\b(PostgreSQL|MariaDB|MySQL|Redis|Celery|Django|React|Vue|Node\.js)\b' \
   source/requisitos/casos-uso source/requisitos/reglas-negocio \
   source/base-cognitiva source/gestion/evidencia/rbac-historia source/index.rst \
   2>&1 | grep -vE '/(implementacion-tecnica|testing)\.rst:' | wc -l
24

# Distribución de las 24 restantes:
#   6  §2.4 sistema IVR exempt (preservadas)
#   18 archivos de identidad de proyecto (diferidas a TD-D5)
```

## Commits del WP (5 commits)

1. `1d5c0f90` — Open WP-G STD-010 vocabulary cleanup (wp-state.md)
2. `1667aa34` — Apply STD-010 vocab to rbac-historia narrative (1/4)
3. `d2a73021` — Apply STD-010 vocab to fundamentos-conceptuales (2/4)
4. `eeeebe8f` — Apply STD-010 vocab to _uml pedagogical examples (3/4)
5. `7bda837e` — Apply STD-010 vocab to admin UC and RBAC catalog (4/4)

## Roadmap status

| WP | Estado |
|---|---|
| WP-A | ✅ Sprint 1 |
| WP-B | ✅ Sprint 2 |
| WP-C | ✅ Sprint 2 |
| WP-D | ✅ naming-rules-resolution |
| WP-E | ✅ Factory/Builder/Manager |
| WP-F (Serializer/ViewSet/View) | ⏳ pendiente — ejecutable en feature/cnst-033-uml-conformance |
| WP-G (STD-010 cleanup vocabulario) | ✅ **este WP** (clear in-scope) |
| WP-H | ✅ Sprint 1 |
| TD-D5 (STD-010 §2.5 — exenciones identity files + procedimientos + ADRs) | ⏳ siguiente |

## Refs

- WP `naming-rules-resolution` (D2 + D4 aplicadas en STD-010 v1.1.0).
- STD-010 v1.1.0 §2.1, §2.4, §3, §5.4, §5.5.
- TD-D5 propuesta: ampliar §2.5 con clausula de exención para
  identity files (`_metadata/`, `index.rst`), `normativa/procedimientos/`,
  `normativa/gobernanza/adr-*`, plantillas técnicas y testing.rst.
