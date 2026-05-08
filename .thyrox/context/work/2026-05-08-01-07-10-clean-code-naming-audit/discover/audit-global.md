```yml
created_at: 2026-05-08 01:40:00
project: IACT-docs
work_package: 2026-05-08-01-07-10-clean-code-naming-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
type: Reporte Global Consolidado
```

# Audit global CLEAN_CODE_NAMING_PRINCIPLES en source/

## 1. Resumen ejecutivo

`source/` contiene **2866 archivos `.rst`**. El audit cubre
6 categorias de la norma CLEAN_CODE_NAMING_PRINCIPLES v1.0.0.

### Resultado global

| Categoria | Severidad | Violaciones | Esfuerzo |
|---|---|---|---|
| **C1** Sufijos prohibidos en clases | Alta | **148 clases unicas** | 30-50 h |
| **C2** Acronimos en identificadores | Alta | **~700-800 ediciones** | 15-25 h |
| **C3** Vocabulario STD-010 fuera exempt | Alta | **~265 ediciones** | 11-16 h |
| **C4** Filenames con acronimos | Media | **11 archivos** | 5-7 h |
| **C5** Metodos/variables ambiguos | Baja | **0** (post-analisis con contexto) | — |
| **C6** Domain vs framework (subset C1) | Alta | **incluido en C1** | — |
| **Total** | | **~1100 ediciones** | **~60-100 h** |

## 2. Hallazgo CRITICO — conflicto normativo

### 2.1 Descripcion

El archivo `source/backend/conventions.rst` (lineas 27-39)
**prescribe explicitamente** los sufijos:

- `Serializer` → "**Serializers:** sufijo `Serializer`"
- `ViewSet` → "**ViewSets:** sufijo `ViewSet`"
- `View` → "**APIViews:** sufijo `View`"
- `Permission` → "**Permissions:** sufijo `Permission`"

Estos cuatro sufijos estan **prohibidos** por
CLEAN_CODE_NAMING_PRINCIPLES §6.2.

### 2.2 Consecuencia

Cualquier rename masivo de clases con estos sufijos
**genera otra contradiccion** mientras `backend/conventions.rst`
permanezca vigente.

### 2.3 Resolucion requerida (PRE-REQUISITO)

ADR explicito que defina:

- **Opcion A:** Actualizar `backend/conventions.rst` para
  alinear con CLEAN_CODE_NAMING_PRINCIPLES. Esto implica
  rename de 115+ clases en docs.
- **Opcion B:** Excepcion en CLEAN_CODE_NAMING_PRINCIPLES
  §6.2 para clases tecnicas DRF. Documentar en §8.3-equivalente.
- **Opcion C:** Mantener conflicto registrado como TD hasta
  decision organizacional posterior.

**Sin esta decision, los WPs de remediacion C1 quedan
bloqueados.**

## 3. Categorias por severidad

### 3.1 Severidad ALTA (bloquean alineamiento normativo)

#### C1 — Sufijos prohibidos (148 clases unicas)

| Sufijo | Clases | Severidad |
|---|---|---|
| Factory | 9 | Alta |
| Builder | 7 | Media-Alta |
| Manager | 4 | Alta |
| Serializer | 27 | Alta (CONFLICTO normativo) |
| ViewSet | 7 | Alta (CONFLICTO normativo) |
| View | 81 | Alta (CONFLICTO normativo) |
| Permission | 8 | Media (mezcla dominio) |
| Backend | 5 | Media (algunos legitimos) |

**Detalle:** `discover/by-category/c1-suffixes-prohibited.md`.

#### C2 — Acronimos `SOD/SoD/sod` (1225 refs totales)

- **637 en `requisitos/casos-uso/`** (excluyendo
  use-case-view ya limpiado).
- **58 en `reglas-negocio/`**.
- **44 en `backend/`**.
- **29 en `domain-model/`**.
- **10 archivos** con `sod` en filename.

**Detalle:** `discover/by-category/c2-acronyms.md`.

#### C3 — Vocabulario STD-010 (~265 ediciones)

- **210 PostgreSQL/MySQL/MariaDB**.
- **73 Redis**.
- **247 Django** (algunos legitimos en backend).
- **91 React/Vue**.

**Pre-requisito:** clarificar scope STD-010 §2 (¿es exempt
`requisitos/_metodologia-aplicacion/`? ¿el `index.rst` raiz?
¿como tratar referencias a sistemas externos del cliente?).

**Detalle:** `discover/by-category/c3-std010-vocabulary.md`.

### 3.2 Severidad MEDIA

#### C4 — Filenames (11 archivos)

10 con `sod`, 1 `factory-reportefactory.rst`.

Cada rename requiere git mv + update toctrees + cross-refs.

**Detalle:** `discover/by-category/c4-filenames.md`.

### 3.3 Severidad BAJA / sin violacion

#### C5 — Metodos y variables (0 violaciones)

Tras analisis con contexto, los 4 hits `def handle(` son
patrones legitimos (Command Handler en Larman + Django
management commands).

**Detalle:** `discover/by-category/c5-methods-variables.md`.

## 4. Distribucion por subdirectorio

| Subdirectorio | Violaciones C1 (cls) | C2 (sod refs) | C3 (tech terms) | Severidad subdirectorio |
|---|---|---|---|---|
| `requisitos/casos-uso/` | ~80% del total | 637 | varios | Critica |
| `requisitos/reglas-negocio/` | bajo | 58 | varios | Alta |
| `requisitos/_metodologia-aplicacion/` | medio | bajo | alto | Media |
| `arquitectura-tecnica/use-case-view/` | bajo | 2 (limpio) | (exempt) | Baja ✅ |
| `arquitectura-tecnica/domain-model/` | (clases) | 29 | (exempt) | Media |
| `backend/` | 100+ refs (CONFLICTO) | 44 | (exempt) | Critica |
| `normativa/` | bajo | filenames sod | varios | Media |
| `base-cognitiva/` | bajo | bajo | medio | Baja |

## 5. Excepciones documentadas (preservar)

Confirmadas como excepciones legitimas (norma §8.3):

1. Tokens RBAC opacos: `access:view_sod`,
   `access:update_sod`, `access:disable_sod`.
2. Codigos BD: `SOD-001..003`, `AGR-001..010`, etc.
3. Termino regulatorio en prosa larga: "Separation of
   Duties", "RBAC" como vocabulario disciplinar.
4. Sistemas EXTERNOS del cliente: "MySQL del IVR", "Sistema
   IVR" cuando son hechos factuales (NO comportamiento de
   IACT).
5. Clases base de librerias: `DjangoModelFactory`, `SubFactory`,
   `BasePermission`, `ModelBackend`, `ModelViewSet`,
   `APIView`.

## 6. Decisiones requeridas por el ejecutor

Antes de planear WPs de remediacion, se requieren:

1. **Conflicto `backend/conventions.rst`:** Opcion A/B/C.
2. **Scope STD-010:** clarificar exempt
   `_metodologia-aplicacion/`, `index.rst` raiz, sistemas
   externos.
3. **Builder en dominio:** ¿`ResumenSaludBuilder` viola
   §1.2 o es legitimo como rol de dominio?
4. **RBAC en prosa:** ¿es excepcion implicita por
   vocabulario disciplinar?

## 7. Plan de remediacion fragmentado

Ver `plan-execution/remediation-roadmap.md` para detalles.

WPs futuros priorizados:

| # | WP | Severidad | Esfuerzo | Pre-req |
|---|---|---|---|---|
| WP-A | Filenames sod (10 archivos + cross-refs) | Media | 5-7 h | — |
| WP-B | Refs SoD en casos-uso (637 refs) | Alta | 10-15 h | — |
| WP-C | Refs SoD en reglas-negocio (58) + domain-model (29) + backend (44) | Alta | 4-6 h | — |
| WP-D | Resolver conflicto backend/conventions.rst (ADR + decision) | Critica | 2-4 h | — |
| WP-E | Rename clases C1 (Factory + Builder + Manager) — 20 clases | Alta | 6-10 h | WP-D |
| WP-F | Rename clases C1 Serializer/ViewSet/View (115 clases) | Alta | 30-40 h | WP-D, WP-E |
| WP-G | Cleanup STD-010 fuera exempt (~265 ediciones) | Alta | 11-16 h | clarificar scope |
| WP-H | factory-reportefactory.rst rename | Baja | 30 min | — |

**Total estimado: ~70-100 h distribuidas en 8 WPs.**

## Refs

- CLEAN_CODE_NAMING_PRINCIPLES v1.0.0.
- STD-010 v1.0.0.
- backend/conventions.rst (CONFLICTO).
- WPs previos cerrados (5).
- discover/by-category/* (5 reportes detallados).
