```yml
project: IACT-docs
work_package: 2026-05-05-21-56-47-functional-decomposition-antipattern-audit
created_at: 2026-05-05 21:56:47
closed_at: 2026-05-05 22:15:00
current_phase: Phase 11 — TRACK/EVALUATE
status: Cerrado
audit_result: clean — 84/84 OK, 0 antipatrones detectados
author: NestorMonroy
flow: rm
methodology_step: rm-analysis
sp01_approved_at: 2026-05-05 22:05:00
sp01_decisions:
  - scope: 99 archivos domain-model (67 base + 16 nuevos + index + overview)
  - profundidad: nombres de clase Y nombres de metodos
  - referencia_normativa: leer metodologia-oop-para-ucs.rst y citar junto a Brown 1998
predecessor_wp: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
target: Auditar el modelo de dominio (source/arquitectura-tecnica/domain-model/* y use-case-view/*) contra el antipatron Functional Decomposition de William Brown. Detectar y reportar sintomas; proponer fixes para los hallazgos confirmados.
related_normativa: source/normativa/estandares/metodologia-oop-para-ucs.rst (si existe)
```

# WP — Functional Decomposition Antipattern Audit

## Trigger

El predecesor (`use-case-view-uml07-standalone-pass`) entrego 16 archivos
nuevos en `domain-model/` + 83 uml-07 standalone que referencian entidades
del dominio. El ejecutor pide auditar que esos artefactos NO incurran en
el antipatron **Functional Decomposition** descrito por William Brown
(*AntiPatterns: Refactoring Software, Architectures, and Projects in
Crisis*).

## Definicion del antipatron (William Brown)

> *"La Descomposición Funcional es un antipatrón donde el desarrollador
> estructura un sistema orientado a objetos como si fuera un programa
> procedural tradicional, ignorando los beneficios y principios
> fundamentales de la orientación a objetos."*

## Sintomas a detectar (del enunciado)

### S-1 — Nombres de clases reflejan funciones, no entidades del dominio

| Antipatron | Domain-driven |
|---|---|
| ❌ `CalcularImpuestos` | ✓ `Impuesto` |
| ❌ `ProcesarDatos` | ✓ `Cliente` |
| ❌ `ValidarEntrada` | ✓ `Factura` |
| ❌ `RealizarLlamada` | ✓ `Call` |
| ❌ `EjecutarReporte` | ✓ `Report` |

**Heuristica:** nombre que empieza con verbo en infinitivo
(`Calcular`, `Procesar`, `Validar`, `Ejecutar`, `Generar`, `Realizar`,
`Crear`, `Obtener`, `Computar`) o termina en gerundio.

### S-2 — Clases con un unico metodo "ejecutar"/"procesar"/"correr"

> *"Esto indica que la clase está actuando más como una función que como
> una abstracción de un concepto del dominio."*

**Heuristica:** clase con UN solo metodo, especialmente si el metodo es
`execute()`, `process()`, `run()`, `ejecutar()`, `procesar()`, `correr()`,
`handle()`, `apply()`, `compute()`, `calculate()`.

### S-3 — Uso excesivo de miembros estaticos (static)

> *"Demuestra un pensamiento procedural, ya que se utilizan las clases
> como simples agrupaciones de funciones en lugar de plantillas para
> crear objetos."*

**Heuristica:** clases con metodos mayoritariamente `static` o sin estado
(sin atributos de instancia). En PlantUML class diagrams, miembros con
prefijo `{static}` o `+ {static}`.

### S-4 — Ausencia de principios OOP fundamentales

- **Herencia** para jerarquias "es-un" — ¿hay clases que serian utiles
  como abstractas/base con subclases?
- **Polimorfismo** para variaciones de comportamiento — ¿hay if-cadenas
  enmascaradas como switches sobre tipo?
- **Encapsulamiento** — ¿hay atributos publicos que deberian ser privados
  con metodos accessors?

## Justificacion de Brown

El antipatron hace el software:

- **Imposible de comprender** — logica dispersa, no refleja el dominio.
- **Dificil de reutilizar** — funcionalidades estrechamente acopladas.
- **Complicado de probar** — falta encapsulamiento + alta dependencia.

## Solucion propuesta por Brown

Modelo del Dominio Orientado a Objetos (Domain Model):

1. Identificar entidades reales del dominio del problema.
2. Modelar entidades como clases con responsabilidades bien definidas.
3. Establecer relaciones naturales entre clases.
4. Utilizar patrones de diseno apropiados.

## Alcance del audit (in-scope)

### Artefactos auditados

1. `source/arquitectura-tecnica/domain-model/*.rst` (67 base + 16 nuevos
   = 83 archivos).
2. `source/arquitectura-tecnica/use-case-view/*/uc-XXX-NN-<slug>.rst`
   (83 archivos).
3. **Particularmente** los 16 archivos nuevos del WP predecesor:
   - 9 clases nuevas: AuthorizationGuard, BlacklistedToken,
     InternalMessage, PipelineExecutionRepo, MetricsCache,
     IdempotencyPolicy, ExpirationPolicy, PasswordGenerator,
     EffectivePermissionsAggregator
   - 5 repos: UserRepo, FunctionRepo, FunctionGroupRepo,
     SeparationRuleRepo, AccessGroupRepo
   - 2 patterns: specification-pattern, strategy-pattern

### Por que esos primero

Los repos (XxxRepo) son sospechosos por nombre — terminan en "Repo",
podrian ser legitimas (Repository Pattern) o caer en S-1 (nombre
funcional). El audit clarificara si son repositorios canonicos
(domain-driven) o agrupaciones de funciones (antipatron).

Las "Policy", "Guard", "Aggregator", "Generator", "Validator" son
sospechosas por sufijo — pueden ser legitimas (Strategy/Validator
patterns) o caer en S-2 (single-method "execute"). El audit
distingue.

### Areas NO incluidas

- ❌ `source/requisitos/casos-uso/` (12 partes textuales) — no son
  diagramas de clase, no aplica el antipatron directamente.
- ❌ `source/databases/` (esquemas SQL) — no son OOP per se.
- ❌ Codigo Python del backend — no esta en este repo de docs.

## Criterios de evaluacion

Para cada artefacto auditado, evaluar:

| Criterio | Evidencia | Veredicto |
|---|---|---|
| **C-1** Nombre denota entidad de dominio (no funcion) | nombre del archivo, `class XxxName` en PlantUML | ✓ entity / ❌ function |
| **C-2** Clase tiene multiples responsabilidades (≥2 metodos relevantes, no contadores triviales) | bloque `class { ... }` en PlantUML | ✓ multi-resp / ⚠ single-method / ❌ single-action |
| **C-3** Atributos de instancia presentes (no solo metodos) | atributos con `+ campo : Tipo` | ✓ stateful / ❌ stateless |
| **C-4** Si hay relaciones, usa herencia/composicion donde aplica | relaciones `--\|>`, `o-->`, `*-->` en PlantUML | ✓ usa / ⚠ no aplicable / ❌ falta donde aplicaria |
| **C-5** Si es patron (Repo/Policy/Strategy), declara serlo y respeta el patron | nota o seccion explicando el rol | ✓ explicito / ⚠ implicito / ❌ no declarado |

**Veredicto agregado por archivo:**
- ✅ **OK** — todos los criterios ✓.
- ⚠ **Revision** — algun criterio ⚠ o falta evidencia clara.
- ❌ **Antipatron** — uno o mas criterios ❌ confirmados.

## Output esperado

1. `analyze/functional-decomposition-audit.md` — reporte por archivo
   con veredicto + evidencia + recomendacion.
2. `analyze/audit-summary.md` — resumen agregado:
   - Total auditados / OK / Revision / Antipatron.
   - Patrones recurrentes detectados.
   - Top recomendaciones priorizadas.
3. `track/{wp}-changelog.md` y `track/{wp}-lessons-learned.md` —
   cierre formal.
4. (Si hay hallazgos): un task plan con T-NNN para corregir cada uno.

## No-fixes en este WP

Este WP **AUDITA, NO CORRIGE**. Si se detectan ❌ Antipatron, se
documentan + se crea un WP separado de remediacion. La razon: la
auditoria debe ser objetiva — corregir y auditar en mismo WP introduce
sesgo (confirmation bias).

**Excepcion:** typos triviales o renombres mecanicos (e.g. `XxxRepository`
legacy → `XxxRepo`) si ya existe consenso normativo (CNST, STD).

## Riesgos

| ID | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Falsos positivos por sufijos sospechosos (Validator, Generator) que SI son patterns legitimos | Aplicar C-5 antes de C-1: si la clase declara ser pattern, evaluar contra la spec del pattern, no contra heuristica de nombres |
| R-02 | El antipatron tiene matices culturales (ingles vs espanol). Brown habla de codigo, no de docs | Adaptar heuristica a IACT: nombres en ingles para identifiers tecnicos, espanol para descripciones (STD-008) |
| R-03 | Audit puede revelar que la mayoria de los 16 nuevos del predecesor caen en antipatron | Si pasa, documentar hallazgo honesto. WP separado de remediacion. NO esconder. |
| R-04 | William Brown publico en 1998 — algunas heuristicas estan datadas (e.g. static excessive era marker en Java de los 90s) | Adaptar al contexto Python/Django moderno donde dataclasses + utility modules son legitimos |

## Stopping points

- **SP-01** Phase 1 → 3: ejecutor aprueba scope + criterios.
- **SP-02** Phase 3 sample (5 archivos auditados): valida que la
  metodologia detecta correctamente.
- **SP-03** Phase 3 completo: revisar audit-summary antes de cerrar.

## Decisiones pendientes para SP-01

1. ¿Auditar SOLO los 16 nuevos del predecesor, los 99 totales
   (16 nuevos + 83 originales del domain-model), o tambien los 83 uml-07
   standalone?
2. ¿Aplicar el antipatron tambien a metodos individuales dentro de
   clases (e.g. `User.calculate_age()` es OOP correcto, mientras
   `Calculate.user_age()` seria antipatron)?
3. ¿Buscar el archivo de Brown en `source/base-cognitiva/` o reglas
   internas? Si existe `metodologia-oop-para-ucs.rst`, citarlo.

## Anatomia esperada del WP

```
2026-05-05-21-56-47-functional-decomposition-antipattern-audit/
├── wp-state.md
├── functional-decomposition-antipattern-audit-risk-register.md
├── discover/
│   └── functional-decomposition-antipattern-audit-analysis.md
├── analyze/
│   ├── functional-decomposition-audit.md       (reporte por archivo)
│   ├── audit-summary.md                         (resumen agregado)
│   └── audit-data.json                          (machine-readable)
└── track/
    ├── functional-decomposition-antipattern-audit-changelog.md
    └── functional-decomposition-antipattern-audit-lessons-learned.md
```
