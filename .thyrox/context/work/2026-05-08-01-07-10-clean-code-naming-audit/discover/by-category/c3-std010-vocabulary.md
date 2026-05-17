```yml
created_at: 2026-05-08 01:25:00
project: IACT-docs
work_package: 2026-05-08-01-07-10-clean-code-naming-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: Cat-3 Audit (STD-010 vocabulario canonico)
```

# Cat-3 — Vocabulario canonico STD-010

> Norma: CLEAN_CODE_NAMING_PRINCIPLES §7 + STD-010 v1.0.0.
>
> STD-010 §2 declara EXEMPT: `implementacion-tecnica.rst` y
> `source/arquitectura-tecnica/**`.

## 1. Resumen

Refs en archivos NO-exempt (excluyendo
`/implementacion-tecnica.rst:`, `/arquitectura-tecnica/`,
`/backend/`):

| Termino | Refs | Severidad |
|---|---|---|
| PostgreSQL/MariaDB/MySQL | **210** | Alta |
| Redis | **73** | Alta |
| Celery | **8** | Media |
| Django | **247** | Alta |
| React/Vue | **91** | Media |
| **Total** | **~629** | |

## 2. Concentracion por subdirectorio

### 2.1 `requisitos/_metodologia-aplicacion/` — gran fuente

Es metodologia interna del proyecto (no requisitos formales).
Contiene multiples archivos con violaciones:

- `plan-documentacion-uc.rst:627` — "MySQL + Redis"
- `diagramas-distribucion/*` — multiples menciones
  PostgreSQL/MySQL/Redis en diagramas C4
- `diagramas-colaboraciones/numeracion-anidada.rst` —
  `object ":Redis"` como nombre de objeto en plantuml

**Decision necesaria:** ¿`requisitos/_metodologia-aplicacion/`
debe estar exempt (es metodologia, no requisitos)? La norma
STD-010 §2 solo exempta `implementacion-tecnica.rst` y
`arquitectura-tecnica/**`. Estrictamente, este directorio
NO esta exempt.

### 2.2 `requisitos/reglas-negocio/`

- `br-001-fuente-operacional-inmutable.rst:48` — "La base
  de datos MySQL del sistema IVR..." — esto es una
  descripcion de un sistema EXTERNO (IVR del cliente), no
  del sistema IACT propio.
- Caso especial: el termino MySQL aqui describe un sistema
  externo del cual IACT consume datos. Renombrar a "el
  sistema operativo" oculta informacion factual relevante.

**Recomendacion:** preservar referencias a sistemas externos
SI son factuales del entorno del cliente.

### 2.3 `requisitos/casos-uso/` — refs en flujo-principal y otros

- `requisitos/casos-uso/*/flujo-principal.rst` — algunos
  mencionan tecnologia. Por STD-010 §2 SI aplica (no son
  implementacion-tecnica).
- Volumen estimado: ~50% de los 210 hits PostgreSQL/MySQL.

### 2.4 `index.rst` (raiz)

```
source/index.rst:18: datos operativos (origen MySQL, modo solo-lectura) con necesidades de
source/index.rst:19: análisis de negocio (destino PostgreSQL, optimizado) mediante un proceso
source/index.rst:40:    - MySQL (operativa, RO) + PostgreSQL (analítica)
```

Este es el resumen ejecutivo del proyecto. Menciona MySQL
y PostgreSQL como hechos arquitectonicos del cliente.

**Decision necesaria:** ¿el index.rst es narrativa de
requisitos (debe aplicar STD-010) o presentacion arquitectonica
(exempt)? El archivo describe la arquitectura del sistema —
posiblemente debe estar en `arquitectura-tecnica/` o
declararse exempt explicitamente.

### 2.5 `base-cognitiva/` — refs en metamodelos

`fnd-*.rst` y `mtm-*.rst` mencionan tecnologias. STD-010 §2
NO los exempta. Volumen menor.

## 3. Observaciones de scope STD-010

STD-010 §2 declara solo 2 archivos/directorios exempt. Esto
deja en aplicacion:

- ✗ `requisitos/_metodologia-aplicacion/` (no exempt)
- ✗ `requisitos/reglas-negocio/` (no exempt)
- ✗ `requisitos/casos-uso/*/{actores,flujo-principal,...}` (aplica explicitamente)
- ✗ `requisitos/casos-uso/*/index.rst` (aplica)
- ✗ `index.rst` raiz
- ✗ `base-cognitiva/`
- ✓ `arquitectura-tecnica/` (exempt)
- ✓ `requisitos/casos-uso/*/implementacion-tecnica.rst` (exempt)
- ⚠ `backend/` (no listado explicitamente, pero documenta
  implementacion — interpretacion ambigua)

**Recomendacion:** ampliar STD-010 §2 con una lista
explicita de directorios exempt vs no-exempt para resolver
la ambiguedad.

## 4. Casos especiales — sistemas externos vs sistema IACT

Distincion semantica importante:

- "Sistema IVR del cliente usa MySQL" → describe sistema
  externo (informacion factual). **Preservar.**
- "El servicio de cache" en flujo del UC → vocabulario
  canonico aplicable (es comportamiento de IACT, no del
  externo). **Aplicar STD-010.**

Esta distincion no esta resuelta en STD-010. Requiere
clarificacion normativa.

## 5. Esfuerzo estimado

| Bloque | Ediciones aprox | Archivos | Estimado |
|---|---|---|---|
| Resolver ambiguedad scope STD-010 | (norma) | 1 (std-010.rst) | 0.5 h |
| Cleanup `_metodologia-aplicacion/` | ~80 | ~10 | 3-4 h |
| Cleanup `reglas-negocio/` | ~30 | ~5 | 1-2 h |
| Cleanup `casos-uso/*/{flujo,actores,...}` | ~100 | ~30 | 4-6 h |
| Cleanup `index.rst` | ~5 | 1 | 0.5 h |
| Cleanup `base-cognitiva/` | ~50 | ~10 | 2-3 h |
| **Total** | **~265 ediciones** | **~57 archivos** | **~11-16 h** |

## 6. Pre-requisito

**Resolver con ejecutor:**

1. ¿`_metodologia-aplicacion/` esta exempt o no?
2. ¿Como tratar referencias a sistemas externos del cliente
   (MySQL del IVR, etc.)?
3. ¿`index.rst` raiz debe aplicar STD-010 o esta exempt
   como portada arquitectonica?

Sin estas decisiones, el alcance del WP de cleanup STD-010
es ambiguo.

## Refs

- CLEAN_CODE_NAMING_PRINCIPLES §7.
- STD-010 v1.0.0 §2.
- WP `std-010-compliance` (cerrado, scope use-case-view solamente).
