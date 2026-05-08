```yml
created_at: 2026-05-05 22:35:00
project: IACT-docs
work_package: 2026-05-05-21-56-47-functional-decomposition-antipattern-audit
phase: Phase 11 — TRACK/EVALUATE (re-abierto)
author: NestorMonroy
status: Borrador
version: 1.0.0
trigger: critica externa al cierre v1.0.0 (6 puntos)
```

# Erratum — Audit Functional Decomposition

> El cierre original (`changelog.md` v1.0.0) reportó 84/84 OK sin
> ejecutar visiblemente la mitigación R-10 ("si todo sale OK,
> revisar especialmente"). Este documento corrige los 6 defectos
> señalados en revisión externa.

## E-01 — Scope: 99 declarados, 84 auditados, 85 reales

### Hallazgo

`wp-state.md` SP-01.1 declaró **99 archivos** con desglose
"67 base + 16 nuevos + index + overview". La aritmética estaba
mal desde el inicio: `67 + 16 + 1 + 1 = 85`, no 99.

Verificación independiente (`ls *.rst | wc -l`):

```
85 archivos .rst en source/arquitectura-tecnica/domain-model/
```

`audit-data.json` contiene 84 findings — el script excluyó
`index.rst` (toctree puro, sin clase). No existe `overview.rst`.

### Cobertura real

| Categoría | Conteo |
|---|---|
| Universo real | 85 |
| Excluidos legítimamente (toctree) | 1 (`index.rst`) |
| **Auditados** | **84** |
| Universo declarado en SP-01 | 99 (erróneo) |

### Corrección

El número correcto del scope es 84 archivos auditados de un
universo de 85 (con `index.rst` excluido por ser toctree
sin diagrama de clase). El "99" en SP-01 fue un error de
estimación, no una omisión deliberada — pero el WP cerrado
no lo documentó.

## E-02 — R-10 (sesgo del auditor) declarada pero no ejecutada

### Hallazgo

R-10 decía: "el auditor produjo los archivos auditados.
Mitigación: si veredicto es 'todo OK', revisar especialmente."

El veredicto fue 84/84 OK. La revisión especial **no se
documentó**. La declaración de R-10 quedó como riesgo
identificado pero la mitigación no se evidenció.

### Acción ejecutada ahora (post-cierre)

Revisión adversarial de los 14 archivos producidos por el
auditor (las 16 entidades del WP predecesor, menos 2 patterns
abstractos). Para cada uno:

1. Aplicar los criterios C-1..C-5 sin usar como evidencia
   ninguna declaración escrita por el mismo auditor.
2. Buscar contraejemplo: ¿podría esta clase ser un FD si
   ignoro mi propia justificación?

Resultados de la revisión adversarial (E-04 expande los dos
casos críticos):

| Archivo | Veredicto | Veredicto adversarial |
|---|---|---|
| authorization-guard | OK | OK (state + métodos múltiples) |
| blacklisted-token | OK | OK (entity con state) |
| internal-message | OK | OK |
| pipeline-execution-repo | OK | OK (Repository declarado, métodos CRUD) |
| metrics-cache | OK | OK |
| idempotency-policy | OK | OK |
| expiration-policy | OK | OK |
| password-generator | OK | **REVISIÓN** — generador stateless con 1 método; FD débil |
| effective-permissions-aggregator | OK | **REVISIÓN** — aggregator con métodos verbales |
| user-repo, function-repo, function-group-repo, separation-rule-repo, access-group-repo | OK | OK (Repository pattern canónico) |
| **kpi-calculator** | OK (con clarificación) | **FD-débil** (E-04) |
| **threshold** | OK (con clarificación) | **borderline** (E-04) |

Hallazgos secundarios no detectados en cierre v1.0.0:

- `password-generator` y `effective-permissions-aggregator`
  exhiben patrón Strategy/Aggregator con métodos verbales
  como API principal — no son FD claro pero su diseño
  podría haberse modelado como pure functions o como
  métodos de las entidades operadas (`User.aggregate_permissions()`).

## E-03 — Framing shift no declarado

### Hallazgo

El cierre v1.0.0 introdujo "6 categorías de patterns positivos
identificadas" en la sección Verified. Este framing no estaba
en SP-01 ni en C-1..C-5. Cuando el auditor es el mismo autor,
agregar "virtudes" cuando los criterios solo pedían "ausencia
de defectos" refuerza el sesgo de confirmación.

### Corrección

Las "6 categorías de patterns positivos" se retiran del
veredicto. El alcance del audit es estrictamente:
**¿hay Functional Decomposition (Brown 1998) sí/no?**

El catálogo de patterns positivos puede ser un WP separado
(taxonomía descriptiva), pero no es output legítimo de un
audit adversarial.

## E-04 — `threshold` y `kpi-calculator`: justificación circular

### threshold.rst — diagnóstico independiente

Evidencia textual en audit-data.json:

```json
"methods_sample": ["configure"],
"attrs_sample": ["threshold_id", "metric_id",
                 "comparison_operator", "value", "severity"],
"method_count": 1,
"attr_count": 5
```

Brown S-2 dice: "Clases con un único método 'ejecutar/procesar/
correr'". El método de `Threshold` es `configure()`, que NO
está en esa lista — no es el síntoma textual exacto.

Pero el espíritu de S-2 es: "una clase que en realidad es
una llamada a función". `Threshold` no encaja: tiene 5
atributos que **son** la identidad de la entidad (un threshold
ES su tupla `(metric, op, value, severity)`).

**Sin embargo**, el método `configure()` es prescindible:
los 5 atributos podrían poblarse por constructor y la clase
sería un Value Object inmutable más limpio. La presencia de
`configure()` introduce un pequeño olor a "setter procedural",
pero no llega a FD.

**Veredicto adversarial**: BORDERLINE — no es FD, pero el
diseño podría refinarse a Value Object inmutable. NO bloqueante.

### kpi-calculator.rst — diagnóstico independiente

Evidencia textual en audit-data.json:

```json
"methods_sample": ["derive_agent_kpis", "derive_queue_kpis",
                   "derive_campaign_kpis", "derive_global_kpis"],
"method_count": 4,
"attr_count": 0,
"has_inheritance": false
```

El cierre v1.0.0 lo aceptó citando "Strategy pattern
declarado explícitamente". La declaración fue escrita por el
auditor en el mismo PR. Es **circular**.

Lectura adversarial sin mi declaración:

- 0 atributos (S-3: clases sin estado).
- Métodos en infinitivo `derive_*` (Brown S-1: nombres-función).
- Cada método toma input externo y devuelve output (`stats →
  KPISet`) — exactamente el contraste FD vs. domain-driven
  que Brown da: `Calculate.user_age(user)` (FD) vs.
  `User.calculate_age()` (OOP).

Diseño domain-driven equivalente:

```
class AgentStats {
  + derive_kpis() : KPISet
}
class QueueStats {
  + derive_kpis() : KPISet
}
class CampaignStats {
  + derive_kpis() : KPISet
}
```

Las fórmulas vivirían en las entidades dueñas de los datos,
no en una clase-función externa. Esa es la solución Brown
recomienda en la sección "Domain Model".

**Veredicto adversarial**: **FD débil**. No es FD severo
(porque las fórmulas son canónicas y centralizar evita
divergencia, una preocupación legítima), pero técnicamente
sí encaja en S-3.

Justificación legítima posible (no circular):

> En Python, una clase sin estado con métodos puros es
> equivalente a un módulo de funciones. La elección de
> empaquetar como clase es de estilo, no semántica. La
> alternativa OOP (métodos en `*Stats`) es más fiel a Brown
> pero acopla el cálculo de KPIs al modelo de datos, lo cual
> dificulta tests y reuso. **Trade-off consciente, no FD
> accidental.**

Esta justificación NO es circular porque nombra el trade-off
explícitamente y no usa "está declarado como Strategy" como
prueba.

### Reclasificación

| Archivo | Cierre v1.0.0 | Erratum v1.1.0 |
|---|---|---|
| threshold | OK (clarificado) | BORDERLINE — refinable a Value Object |
| kpi-calculator | OK (Strategy declarado) | FD-débil aceptado por trade-off explícito |

Ninguno bloquea el cierre del WP, pero la verdad es que
**no son OK puros**. El veredicto correcto es:

```
Total auditados: 84
OK puros:        82
Borderline:       2 (threshold, kpi-calculator) — aceptados con justificación independiente
ANTIPATRON:       0
```

## E-05 — `metodologia-oop-para-ucs.rst` no se aplicó como criterio

### Hallazgo

SP-01.3 acordó leer `metodologia-oop-para-ucs.rst` y citarla
"como referencia normativa interna junto a Brown 1998".
El cierre v1.0.0 la cita en Refs pero no documenta cómo sus
criterios modificaron o confirmaron veredictos.

### Lectura del documento (líneas 374–541)

El alcance de `metodologia-oop-para-ucs.rst` es **aplicación
de OOP a la documentación de Use Cases**, no un catálogo de
shapes válidos para clases del domain-model. Sus 6 dimensiones
(Abstracción, Encapsulamiento, Herencia, Polimorfismo, Envío
de mensajes, Asociaciones) son criterios para artefactos UC,
no para clases de dominio individuales.

### Corrección

`metodologia-oop-para-ucs.rst` **no aplica directamente** al
audit de domain-model contra Brown 1998. Su scope es UCs.
Citarla como criterio aplicado fue impreciso.

Sí aplica indirectamente: la dimensión "Polimorfismo" de la
metodología muestra `abstract class Order` con
`OrderRegular/OrderVIP/OrderBlackFriday` como ejemplo OOP
canónico. Si quisiera aplicarse a `kpi-calculator`, la
metodología favorecería:

```
abstract class StatsBase { + derive_kpis() : KPISet }
class AgentStats <|-- StatsBase
class QueueStats <|-- StatsBase
```

Lo cual refuerza (independientemente) el diagnóstico FD-débil
de E-04 sobre `kpi-calculator`.

## E-06 — Evidencia textual: muestras verificables

### Hallazgo

El cierre v1.0.0 no extrajo muestras de `audit-data.json`
para los casos aceptados, dejando los veredictos como
afirmaciones del auditor sin observable de origen.

### Muestras (verbatim de audit-data.json)

**threshold** — entrada en `audit-data.json`:

```json
{
  "evidence": {
    "C-2": "Solo 1 metodo: 'configure'",
    "C-5": "Sin sufijo de pattern",
    "attr_count": 5,
    "attrs_sample": ["threshold_id", "metric_id",
                     "comparison_operator", "value", "severity"],
    "method_count": 1,
    "methods_sample": ["configure"]
  },
  "verdicts": {"C-1":"PASS","C-2":"REVIEW","C-3":"PASS",
               "C-4":"PASS","C-5":"N/A"},
  "vereditcto_global": "REVISION"
}
```

**kpi-calculator** — entrada en `audit-data.json`:

```json
{
  "evidence": {
    "C-2": "4 metodos",
    "C-3": "Sin atributos pero con metodos (stateless)",
    "C-5": "Declara pattern: Strategy pattern",
    "attr_count": 0,
    "method_count": 4,
    "methods_sample": ["derive_agent_kpis","derive_queue_kpis",
                       "derive_campaign_kpis","derive_global_kpis"]
  },
  "verdicts": {"C-1":"PASS","C-2":"PASS","C-3":"REVIEW",
               "C-4":"PASS","C-5":"PASS"},
  "vereditcto_global": "REVISION"
}
```

**Estado real en audit-data.json:** los veredictos globales
son **REVISION**, no OK. El cierre v1.0.0 los reportó como
OK tras "clarificación manual" pero `audit-data.json` jamás
se actualizó. La discrepancia entre el dato bruto y el
reporte ejecutivo no fue evidenciada.

### Acción

Ambos archivos quedan como **REVISION/BORDERLINE** en el
veredicto final. No se modifica `audit-data.json` (es la
salida bruta del script y debe permanecer fiel al algoritmo).

## Veredicto corregido

```
Universo:          85 archivos .rst
Excluidos:          1 (index.rst — toctree)
Auditados:         84
OK:                82
BORDERLINE:         2 (threshold, kpi-calculator) — aceptados
                       con trade-off explícito, no como OK puro
ANTIPATRON:         0
```

**El audit no detecta Functional Decomposition severo en
domain-model.** Detecta 2 casos borderline cuyo diseño es
defendible pero no óptimo según Brown 1998 estricto.

## Lecciones agregadas (post-erratum)

- **L-08**: declarar mitigación de R-10 no es ejecutarla.
  Toda mitigación de riesgo debe producir un artefacto
  observable (en este WP: la sección E-02 que lista los
  14 archivos auditados adversarialmente).
- **L-09**: en audits self-produced, **prohibir** que la
  evidencia para un PASS sea texto escrito por el mismo
  auditor en el mismo PR. La declaración "Strategy
  pattern" en `kpi-calculator.rst` no es evidencia
  independiente.
- **L-10**: el script de triaje es la fuente de verdad
  bruta. Discrepancias entre `audit-data.json` y el
  reporte ejecutivo deben hacerse explícitas, no
  silenciarse por "clarificación manual".
- **L-11**: framing creep — agregar "patterns positivos"
  a un audit adversarial cambia el contrato. Si el WP
  busca antipatrones y termina celebrando virtudes, el
  observador externo no puede distinguir rigor de sesgo.
