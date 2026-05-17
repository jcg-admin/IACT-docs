```yml
created_at: 2026-05-07 23:38:00
project: IACT-docs
work_package: 2026-05-07-23-36-40-use-case-view-std-010-compliance
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: STD-010 Compliance Audit
```

# Audit STD-010 en use-case-view

## 1. Marco normativo

**STD-010 §2 (ambito):**

| Archivos | Aplica |
|---|---|
| `source/requisitos/casos-uso/`** | Si |
| `source/arquitectura-tecnica/**` | No — libre |

Sin embargo, STD-010 §4 (reglas de diagramas UML) establece
principios universales aplicables a cualquier diagrama UML
del proyecto:

- Participantes deben usar terminos canonicos (no
  tecnologia concreta).
- Actores deben usar codenames RBAC del catalogo (D-DIAG-001),
  no nombres institucionales.

Adicionalmente, **backend A-005** elimino el concepto `rol`
de `constants.py` y `models.py`. RBAC v5.6.x es
**function-based** (codename + AGR), no role-based.
Cualquier referencia a "el rol X" en docs esta desalineada
con el modelo actual.

## 2. Categorias de violacion

### Cat-A: Tecnologia de BD concreta (§3.2)

PostgreSQL, MariaDB, MySQL, Redis, Elasticsearch.
Vocabulario canonico: "Almacen de Datos", "el repositorio",
"la cache", "el motor de busqueda".

### Cat-B: Procesamiento asincrono concreto (§3.5)

Cron, APScheduler, Celery, RabbitMQ.
Vocabulario canonico: "Planificador de Tareas",
"Procesador Asincrono", "Broker de Mensajes".

### Cat-C: Concepto rol/role (post-A-005)

`rol`, `role`, `role_id`, "el rol X", "auto al rol Y".
Reemplazo: codename especifico (`view_reports`,
`manage_users`) o "AGR-NN" del catalogo, o "usuarios
autenticados" cuando el contexto es general.

### Cat-D: Actores genericos en diagrama UML (§4)

`actor "User"`, `actor "Admin"`, `actor "Operator"`.
Reemplazo: codename especifico que materializa el rol en
ese flujo concreto.

## 3. Violaciones detalladas

### Cat-A: PostgreSQL / Postgres (2 refs)

#### A-01: `audit/index.rst:20`

**Contexto:** descripcion del modulo audit.

```
audit_log (PostgreSQL). Cubre altas/bajas de usuarios,
```

**Cambio propuesto:**

```
audit_log (Almacen de Datos centralizado). Cubre
altas/bajas de usuarios,
```

#### A-02: `audit/uc-aud-02-buscar-auditoria.rst:20`

**Contexto:** descripcion del UC.

```
FTS bounded sobre payload indexado (Elasticsearch / Postgres FTS).
```

**Cambio propuesto:**

```
FTS bounded sobre payload indexado (motor de busqueda
full-text del Almacen de Datos).
```

### Cat-B: Cron / APScheduler (11 refs en 6 archivos)

#### B-01..B-02: `panorama-iact.rst:126` (1 ref)

```
- ``Scheduler`` — cron / APScheduler dispara el
```

**Cambio:**

```
- ``Scheduler`` — el Planificador de Tareas dispara el
```

#### B-03: `auth/uc-auth-02-cerrar-sesion.rst:60` (1 ref)

```
Cron purga BlacklistedToken
```

**Cambio:**

```
Planificador de Tareas purga BlacklistedToken
```

#### B-04..B-06: `access/uc-acc-08-permiso-temporal.rst:23,35,90` (3 refs)

```
:23: Cron de expiracion remueve permisos vencidos.
:35: actor "Cron expiracion" as Cron_expiracion <<sistema_externo>>
:90: (1h-30d). Cron consume
```

**Cambios:**

- L23: `Planificador de Tareas remueve permisos vencidos.`
- L35: `actor "Planificador expiracion" as Planificador_expiracion <<sistema>>`
- L90: `(1h-30d). Planificador consume`

#### B-07..B-09: `permissions/uc-perm-03-conceder-permiso-excepcional.rst:43,99` (3 refs, igual patron)

Mismo cambio que B-04..B-06.

#### B-10: `pipeline/index.rst:62` (1 ref)

```
Scheduler: actor sistema (cron / APScheduler).
```

**Cambio:**

```
Scheduler: actor sistema (Planificador de Tareas).
```

#### B-11: `reports/uc-rpt-07-programar-reporte.rst:32,47` (2 refs)

```
:32: actor "Cron expiracion" as Cron <<sistema_externo>>
:47: Cron --> RUN_CRON
```

**Cambios:**

- L32: `actor "Planificador" as Planificador <<sistema>>`
- L47: `Planificador --> RUN_CRON`

### Cat-C: Concepto rol (10 refs en 7 archivos)

#### C-01: `auth/uc-auth-05-gestionar-sesiones.rst:23`

```
``view_own_sessions`` + ``revoke_own_session`` (auto al rol User).
```

**Cambio:**

```
``view_own_sessions`` + ``revoke_own_session`` (auto-otorgadas
a usuarios autenticados).
```

#### C-02: `audit/index.rst:64`

```
- ``Auditor`` (AGR-008) es el único rol con acceso al
```

**Cambio:**

```
- ``Auditor`` (AGR-008) es el único AGR con acceso al
```

#### C-03: `reports/uc-rpt-09-configurar-filtros.rst:21`

```
implicita (auto al rol User).
```

**Cambio:**

```
implicita (auto-otorgada a usuarios autenticados).
```

#### C-04..C-05: `permissions/uc-perm-08-generar-menu-dinamico.rst:23,64`

```
:23: ``view_own_navigation`` (auto-otorgada al rol User).
:64: rol User).
```

**Cambios:**

- L23: `(auto-otorgada a usuarios autenticados).`
- L64: `usuarios autenticados).`

#### C-06..C-07: `users/index.rst:20,25`

```
:20: IACT. Solo el rol ``UserAdmin`` (AGR-006) modifica el catálogo
:25: cualquier rol autenticado consulta.
```

**Cambios:**

- L20: `IACT. Solo usuarios con ``UserAdmin`` (AGR-006) modifican el catalogo`
- L25: `cualquier usuario autenticado consulta.`

#### C-08..C-09: `operator/uc-opr-08-ver-propio-dashboard.rst:21,63`

```
:21: Sin RBAC adicional al rol User.
:63: al rol User. Diferencia con
```

**Cambios:**

- L21: `Sin RBAC adicional al usuario autenticado.`
- L63: `al usuario autenticado. Diferencia con`

#### C-10: `supervision/index.rst:33`

```
Requiere rol ``Supervisor`` (AGR-003 quality_supervisor).
```

**Cambio:**

```
Requiere AGR-003 ``quality_supervisor`` (Supervisor).
```

### Cat-D: Actor "User" generico (2 refs)

#### D-01: `reports/uc-inc-rpt-01-resolver-segmento.rst:35`

```
actor "User" as User <<sistema>>
```

**Contexto:** uc-inc-rpt-01 es UC de inclusion para
resolver segmento. El "User" aqui es usuario autenticado
generico que consume cualquier UC_RPT_*.

**Cambio:**

```
actor "view_reports" as view_reports
```

(Usar el codename mas comun consumidor — view_reports es
el codename base para vista de reports.)

#### D-02: `reports/uc-rpt-11-compartir-reporte.rst:38`

Similar a D-01.

```
actor "User" as User <<sistema>>
```

**Cambio:**

```
actor "share_reports" as share_reports
```

(Codename especifico de compartir reportes.)

## 4. Resumen de impacto

| Categoria | Refs | Archivos |
|---|---|---|
| Cat-A: BD | 2 | 2 |
| Cat-B: Cron | 11 | 6 |
| Cat-C: rol | 10 | 7 |
| Cat-D: actor User | 2 | 2 |
| **Total** | **25** | **~17 unicos** |

## 5. Tareas de execute (preview)

1 archivo = 1 commit. Total ~17 commits.

- T-001..T-002: Cat-A (audit/index, audit/uc-aud-02).
- T-003..T-008: Cat-B (panorama, auth/uc-auth-02, access/uc-acc-08, permissions/uc-perm-03, pipeline/index, reports/uc-rpt-07).
- T-009..T-015: Cat-C (auth/uc-auth-05, audit/index — ya tocado, reports/uc-rpt-09, permissions/uc-perm-08, users/index, operator/uc-opr-08, supervision/index).
- T-016..T-017: Cat-D (uc-inc-rpt-01, uc-rpt-11).

Algunos archivos aparecen en mas de una categoria
(audit/index, users/index) — se consolidan en un solo commit.

## 6. Validacion final

```bash
# Cat-A: cero hits esperados (excluir implementacion-tecnica.rst)
grep -rn "PostgreSQL\|MariaDB\|MySQL\|Redis\|Elasticsearch" \
  source/arquitectura-tecnica/use-case-view/

# Cat-B: cero hits esperados
grep -rn "Cron\|APScheduler\|Celery\|RabbitMQ" \
  source/arquitectura-tecnica/use-case-view/

# Cat-C: solo "AGR" o codenames, no "rol"
grep -rn "\brol\b\|\brole\b" \
  source/arquitectura-tecnica/use-case-view/

# Cat-D: cero "actor User"
grep -rn 'actor "User"' \
  source/arquitectura-tecnica/use-case-view/
```

## Refs

- STD-010: `source/normativa/estandares/std-010-vocabulario-abstracto.rst` v1.0.0.
- Backend A-005: rename concepto rol -> codenames RBAC.
- D-DIAG-001: convencion de codenames RBAC en diagramas.
