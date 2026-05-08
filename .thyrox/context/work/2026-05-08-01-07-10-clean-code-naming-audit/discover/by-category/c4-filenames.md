```yml
created_at: 2026-05-08 01:30:00
project: IACT-docs
work_package: 2026-05-08-01-07-10-clean-code-naming-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: Cat-4 Audit (Filenames)
```

# Cat-4 — Naming de archivos

> Norma: CLEAN_CODE_NAMING_PRINCIPLES §5 + §9 (kebab-case
> docs RST, snake_case Python).

## 1. Resumen

| Tipo de violacion | Hits |
|---|---|
| CamelCase en filename .rst | 0 ✅ |
| Underscore (_) en filename .rst | 0 ✅ |
| Acronimo `sod` en filename | **10** |
| Filename `factory-reportefactory.rst` (doble violacion) | **1** |
| Total | **11 archivos** |

## 2. Detalle

### 2.1 Filenames con `sod` (§8.2)

10 archivos detectados. Lista completa en
`c2-acronyms.md` §3.

Renombrar todos a `*-de-separacion-*.rst` o
`*-separacion-*.rst` por consistencia con WPs previos.

### 2.2 Archivo con sufijo Factory en filename

`source/requisitos/_metodologia-aplicacion/patrones-diseno/factory-reportefactory.rst`

**Doble violacion:**

1. Contiene `factory` en el filename (§5 + §1.2).
2. Contiene `Factory` (CamelCase como concepto) implicito.

**Renombre propuesto:**

`patron-factory-method-creacion-reportes.rst`

(El archivo documenta un PATRON de diseno, asi que el
nombre puede legitimamente referirse al patron — pero NO
debe nombrar una clase con sufijo Factory.)

### 2.3 Otros patrones a verificar

Sample search adicional:

```bash
find source/ -name "*Helper*" -o -name "*Utils*" -o -name "*Manager*"
```

Resultados: 0 archivos. ✅

## 3. Estado del audit

| Norma | Aplicacion | Cumplimiento |
|---|---|---|
| §5 kebab-case docs RST | 100% (0 violaciones) | ✅ |
| §5 sin underscores | 100% | ✅ |
| §8.2 sin acronimos | **falla 10 archivos** | ❌ |

## 4. Esfuerzo

| Tarea | Tiempo |
|---|---|
| Rename + update toctrees + cross-refs (10 sod files) | 4-6 h |
| Rename factory-reportefactory.rst | 30 min |
| **Total** | **~5-7 h** |

## Refs

- CLEAN_CODE_NAMING_PRINCIPLES §5, §8.2.
- STD-007 (convencion-naming general del proyecto).
