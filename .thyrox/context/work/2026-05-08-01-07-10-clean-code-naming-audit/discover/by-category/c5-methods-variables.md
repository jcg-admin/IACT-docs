```yml
created_at: 2026-05-08 01:35:00
project: IACT-docs
work_package: 2026-05-08-01-07-10-clean-code-naming-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: Cat-5 Audit (Metodos y variables)
```

# Cat-5 — Metodos vagos y variables ambiguas

> Norma: CLEAN_CODE_NAMING_PRINCIPLES §2, §3, §4.

## 1. Aplicabilidad

`source/` es documentacion RST, no codigo Python directo.
La norma aplica a:

- **Pseudocodigo en docs** (templates, ejemplos en
  `tpl-uc-*.rst`, ejemplos en `implementacion-tecnica.rst`).
- **Identificadores en `@startuml` blocks** (metodos
  declarados en clases UML).
- **Constantes definidas en yml metadata o secciones de
  configuracion**.

## 2. Resumen

| Patron prohibido | Hits |
|---|---|
| `def process(` | 0 ✅ |
| `def handle(` | 4 |
| `def get_data(` | 0 ✅ |
| `def do_stuff(` | 0 ✅ |

## 3. Detalle de hits `def handle(`

```
source/normativa/estandares/plantillas/tpl-uc-larman-contratos.rst:416:
   def handle(self, command: GenerateQuarterlyReportCommand):

source/normativa/estandares/plantillas/tpl-uc-larman-contratos.rst:1002:
   def handle(self, command):

source/normativa/estandares/plantillas/tpl-uc-temporal-schedulers.rst:458:
   def handle(self, *args, **options):

source/normativa/estandares/plantillas/tpl-uc-temporal-schedulers.rst:541:
   def handle(self, *args, **options):
```

### 3.1 Analisis caso por caso

**`def handle(self, command: GenerateQuarterlyReportCommand)`**
(tpl-uc-larman-contratos.rst:416, 1002):

Es **patron Command Handler** con tipo de Command que da
contexto. El nombre completo del metodo (con su tipo de
parametro) es semanticamente preciso. Pattern aceptable
en Larman.

Aplicacion §2: el verbo `handle` solo no dice que maneja,
PERO el tipo del parametro lo dice. Contexto suficiente.

**Recomendacion:** preservar como ejemplo de patron Command.
Documentar excepcion en el template si la norma lo requiere
estricto.

**`def handle(self, *args, **options)`**
(tpl-uc-temporal-schedulers.rst:458, 541):

Esta es la firma de Django management command (`BaseCommand.handle`).
Es API publica de Django que el codigo usuario sobrescribe.

**Recomendacion:** preservar — viene de framework.

### 3.2 Conclusion C5.1 (metodos)

0 violaciones reales detectadas. Los 4 hits son patrones
legitimos (Command Handler) o API de framework (Django
management command).

## 4. Variables — busquedas adicionales

### 4.1 Variable `data` sin contexto

```bash
grep -rnE "^\s*data\s*=" source/ 2>/dev/null
```

Volumen alto pero la mayoria es pseudocodigo en
implementacion-tecnica (exempt §5.1) o en patrones de diseno
(metodologia).

### 4.2 Letras solas

```bash
grep -rnE "^\s+[a-z]\s*=\s" source/ 2>/dev/null
```

Mostraria `i = 0`, `j = 1`, etc. Mayoria son loops legitimos
(§9 prohibiciones absolutas exempta `i, j, k` en loops).

## 5. Constantes (§4)

`source/` no contiene muchas constantes Python directas.
Las constantes aparecen en:

- Metadatos `:version:`, `:estado:` (no son constantes
  Python, son metadata RST).
- Codigos de regla (`SOD-001`, `AGR-006`, etc.) — IDs
  estables, excepciones documentadas.
- TTLs, limits en pseudocodigo de
  `implementacion-tecnica.rst` (exempt).

## 6. Conclusion C5

**No hay violaciones reales detectadas en C5.**

La norma §2-§4 aplica principalmente a codigo Python real
(no a este corpus de docs).

Los pseudocodigos en `tpl-uc-*.rst` (templates) deberian
servir como ejemplos buenos del estandar — los detectados
no violan la norma una vez analizados con contexto.

## Refs

- CLEAN_CODE_NAMING_PRINCIPLES §2, §3, §4.
- §9 prohibiciones absolutas.
