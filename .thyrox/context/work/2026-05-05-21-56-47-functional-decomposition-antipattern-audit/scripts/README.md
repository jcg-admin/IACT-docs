```yml
created_at: 2026-05-05 22:30:00
project: IACT-docs
work_package: 2026-05-05-21-56-47-functional-decomposition-antipattern-audit
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Scripts del audit — Functional Decomposition Antipattern

Reproducibilidad: estos scripts son los que se ejecutaron para producir
`analyze/audit-data.json`, `analyze/functional-decomposition-audit.md` y
`analyze/audit-summary.md`. Se preservan aqui para que el audit sea
re-ejecutable y verificable.

## Inventario

| Script | Proposito | Output |
|---|---|---|
| `audit-config.yml` | Heuristicas externas (verbos, sufijos, regex C-5, thresholds, glob, exclusiones) | — |
| `audit_functional_decomposition.py` | Auditor principal config-driven — aplica C-1..C-5 sobre archivos `*.rst` | `<out>.json` |
| `report_from_audit_data.py` | Genera reporte agregado desde el JSON | resumen markdown a stdout |
| `run-audit.sh` | Runner parametrico (repo + WP) con persistencia de log ISO 8601 | log y json en `<wp>/track/build-logs/` |

**Sin valores hardcoded:** `run-audit.sh` recibe `<repo-root>` y
`<wp-dir>` como argumentos. `audit_functional_decomposition.py`
recibe `--root`, `--out`, `--config`. Toda heuristica vive en
`audit-config.yml` y es modificable sin tocar codigo.

## Como reproducir el audit

```bash
REPO=$(git rev-parse --show-toplevel)
WP="$REPO/.thyrox/context/work/2026-05-05-21-56-47-functional-decomposition-antipattern-audit"
bash "$WP/scripts/run-audit.sh" "$REPO" "$WP"
# Output:
#   $WP/track/build-logs/audit-run-<ISO>.log
#   $WP/track/build-logs/audit-data-<ISO>.json
```

Para auditar otra carpeta o glob:

```bash
bash "$WP/scripts/run-audit.sh" "$REPO" "$WP" "src/domain/*.py"
```

Para auditar otro proyecto (mismas heuristicas):

```bash
bash /path/to/this/scripts/run-audit.sh /path/to/other-repo /path/to/other-wp
```

## Heuristicas implementadas

### C-1 — Nombre denota entidad de dominio

Detecta verbos prohibidos como **prefijo** del PascalCase de la clase:
`Calcular, Procesar, Validar, Ejecutar, Generar, Realizar, Crear,
Obtener, Computar, Calculate, Process, Validate, Execute, Generate,
Compute, Get, Make, Do, Run, Handle`.

Excepcion documentada: clases que terminan en sufijo de pattern legitimo
(`Repository, Repo, Strategy, Policy, Specification, Aggregator,
Generator, Validator, Guard, Resolver, Calculator, Service`) NO se
penalizan por C-1 si el cuerpo declara explicitamente el pattern (C-5).

### C-2 — Multiples responsabilidades

- ≥2 metodos relevantes → PASS
- 1 metodo + ≥3 atributos de instancia → PASS (entity con state)
- 1 metodo "execute/process/run/handle/apply" + sin atributos → REVISION
- 0 metodos + ≥1 atributo → PASS (data class / entity)

### C-3 — Atributos de instancia presentes

≥1 atributo `+ campo : Tipo` en el bloque PlantUML. Stateless solo se
acepta si C-5 declara Strategy/Pure Function pattern.

### C-4 — Uso de OOP relations

Si el archivo declara `<|--` (herencia), `o-->`, `*-->` (composicion)
o `..>` (dependencia), PASS. Si no aplica (entity simple), N/A.

### C-5 — Declaracion explicita de pattern

Busca en el cuerpo RST patrones como "Repository pattern", "Strategy
pattern", "Domain Service", "Value Object", "Specification pattern"
declarados textualmente. Si el sufijo del nombre es de pattern pero
NO se declara → REVISION.

## Veredicto global

- Todas C-1..C-5 PASS o N/A → **OK**
- Algun criterio REVISION → **REVISION** (requiere inspeccion manual)
- Algun criterio FAIL → **ANTIPATRON** (Brown 1998)

## Resultados — triaje automatico vs. veredicto final

El script realiza **triaje automatico**. El veredicto final del WP
**84/84 OK** se alcanzo tras inspeccion manual de los casos REVISION/
ANTIPATRON marcados por el script, aplicando contexto que la heuristica
no captura (e.g. archivos `*-pattern.rst` que documentan el patron
mismo, o sufijos como `-Service` legitimos en Domain Service).

### Corrida 2026-05-05 22:17 (script puro, sin clarificacion manual)

```
Total auditados:    83  (excluye index.rst, overview.rst)
OK:                 46
REVISION:           36
ANTIPATRON:          1  (nav-domain — falso positivo; nombre legitimo)
```

### Veredicto final del WP (despues de revision manual)

```
Total auditados:    84
OK:                 84
REVISION:            0
ANTIPATRON:          0
```

Las clarificaciones aplicadas:

- **Sufijos `Repo`, `Service`, `Resolver`, `Calculator`** sin texto
  literal "Repository pattern" — son patterns legitimos por
  convencion del proyecto (CNST/STD), declarados en
  `metodologia-oop-para-ucs.rst`. PASS C-5.
- **`specification-pattern.rst`, `strategy-pattern.rst`** — son docs
  del pattern abstracto, no clases concretas. N/A.
- **`nav-domain`** — PascalCase `NavDomain` no comienza con verbo;
  falso positivo de regex. PASS C-1.
- **`kpi-calculator`** — Strategy stateless declarado. PASS.
- **`threshold`** — entity con 5 atributos + `configure()`. PASS.

## Por que el script no se "auto-aprueba" 84/84

Calibracion epistemica (Brown 1998 + I-012 invariant): el auditor
automatico debe ser **mas estricto** que el veredicto final, no menos.
El script reporta toda sospecha; la decision OK requiere observable
adicional (declaracion textual del pattern, atributos, contexto del
archivo) que solo la inspeccion humana valida.

Si el script aprobara automaticamente con C-5 = "tiene sufijo de
pattern", se introduciria sesgo: cualquier clase llamada `XxxRepo`
pasaria sin verificar que efectivamente sea un repositorio.

## Limitaciones conocidas

- Heuristicas basadas en regex sobre RST/PlantUML — no AST. Falsos
  positivos posibles si el PlantUML usa convenciones no estandar.
- C-5 requiere declaracion textual explicita; patrones implicitos no
  se detectan automaticamente.
- Brown 1998 fue escrito para C++/Java de los 90s. Adaptado a IACT
  (Python/Django/RST docs) — algunas heuristicas (e.g. excessive
  static) tienen menor peso.
