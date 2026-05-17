```yml
created_at: 2026-05-04 21:00:00
project: THYROX
work_package: 2026-05-04-20-56-44-alias-catalog
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Alias Catalog — Phase 1 DISCOVER

## Solicitud

Crear un catálogo de aliases en los diagramas PlantUML de
`source/arquitectura-tecnica/*` y `source/requisitos/*`.
Referencia: diccionario de correcciones de otro proyecto (criterios
de tipo 1/2/3: módulo reservado, alias numerado, abreviatura arbitraria).

## Hallazgos (PROVEN)

**424 aliases únicos** encontrados en 496 archivos RST con bloques PlantUML.

| Tipo de violación | Aliases | Ocurrencias |
|-------------------|---------|-------------|
| Letra sola (A, B, C…) | 8 | 8 |
| Letra + dígito (A1, C01…) | 86 | 117 |
| 2 letras + número (UC01, AL03…) | 42 | 85 |
| Abreviatura + número (PERM01…) | 25 | 40 |
| Abreviatura corta sin _ (AUD, ETL…) | 76 | 198 |
| Prefijo UC_ (UC_AUTH, UC_RPT…) | 15 | 15 |
| F_ + abreviatura (F_VA, F_EL…) | 57 | 57 |
| Prefijo técnico + abbrev (NODE_PG…) | 60 | 61 |
| **Total violaciones** | **369** | **581** |
| Limpios (CLEAN) | 55 | 70 |
| **Total** | **424** | **651** |

## Distribución por corpus

| Corpus | Archivos | Aliases violación |
|--------|----------|-------------------|
| `arquitectura-tecnica/` | 87 | ~120 |
| `requisitos/casos-uso/` | 167 | ~160 |
| `requisitos/_metodologia-aplicacion/` | 123 | ~89 |

## Grupos para WPs correctivos

Dado el volumen (369 aliases × 581 ocurrencias), se recomienda
dividir en WPs por tipo de violación:

| WP sugerido | Scope | Aliases |
|-------------|-------|---------|
| WP-alias-single | SINGLE_LETTER + LETRA_NUMERO | 94 aliases |
| WP-alias-abbrev2num | ABBREV_2_NUMERO + ABBREV_NUMERO | 67 aliases |
| WP-alias-corta | ABREV_CORTA | 76 aliases |
| WP-alias-prefijos | UC_PREFIX + F_ABBREV + PREFIX_ABBREV | 132 aliases |

## Artefactos producidos

- `discover/alias-catalog-analysis.md` — catálogo completo con tabla
  de cada alias: tipo de violación, ocurrencias, labels, archivos fuente.

## Próxima fase sugerida

Phase 3 ANALYZE — profundizar en cada grupo para definir el
diccionario IACT equivalente al `DICCIONARIO` de referencia.
