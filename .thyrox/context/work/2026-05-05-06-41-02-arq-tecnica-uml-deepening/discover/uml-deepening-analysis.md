```yml
created_at: 2026-05-05 06:43:00
project: IACT-docs
work_package: 2026-05-05-06-41-02-arq-tecnica-uml-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# UML deepening — discover analysis

## Resumen ejecutivo

Dos sub-árboles de `arquitectura-tecnica/` requieren
profundización:

| Bloque | Estado actual | Gap | Esfuerzo |
|--------|--------------|-----|----------|
| use-case-view | 13 archivos planos (1/módulo) | restructurar a `casos-uso/`-mirror con 1 diag/file | medio |
| domain-model | 67 clases archivadas, **41 stubs** (61%) | completar atributos + métodos + diagramas + aliases STD_011 | alto |

Recomendación: **abordar Bloque B primero** (mayor
impacto técnico y dependencia para resto del proyecto),
Bloque A después (presentación arquitectónica).

## Bloque B — Domain Model (67 clases)

### Distribución por bounded context

| Bounded Context | Total | Vigente | Pendiente | % gap |
|-----------------|-------|---------|-----------|-------|
| Auth | 3 | 3 | 0 | 0% |
| RBAC | 16 | 6 | 10 | 63% |
| Calls | 2 | 2 | 0 | 0% |
| Reports & Metrics | 22 | 5 | 17 | **77%** |
| Pipeline ETL | 1 | 1 | 0 | 0% |
| Alerts | 8 | 3 | 5 | 63% |
| Audit | 10 | 1 | 9 | **90%** |
| Logs | 5 | 5 | 0 | 0% |
| **Total** | **67** | **26** | **41** | **61%** |

Verificación (`grep -lE "estado: Pendiente|version: 0"`):
**41 stubs** confirmado.

(El conteo total 67 es de clases con `bounded_context:`.
`index.rst` y `overview.rst` no son clases.)

### Bounded contexts críticos a completar

**1. Audit (90% gap, 9 stubs)**

Audit es el bounded context más impactado por el
patrón P-09 audit-or-abort que aparece en 14+ UCs.
Stubs aquí afectan toda la documentación de
auditoría:

```
audit-validator.rst
audit-query-service.rst
audit-event-repo.rst (nombre estimado)
... 6 más
```

**2. Reports (77% gap, 17 stubs)**

Reports tiene el mayor número absoluto de stubs.
La mayoría son `*-report-service` y `*-repo` — el
patrón de servicios y repositorios por dimensión
de reporte (agentes, colas, campañas, etc.):

```
abandono-report-service.rst
agent-daily-stat-repo.rst
agent-report-service.rst
clientes-report-service.rst
... 13 más
```

**3. RBAC (63% gap, 10 stubs)**

RBAC stubs:

```
action.rst                         (item del menu nav)
access-group-function.rst          (tabla pivote)
assignment-repo.rst
exceptional-permission-repo.rst
... 6 más
```

**4. Alerts (63% gap, 5 stubs)**

```
alert-rule.rst
alert-hook.rst
alert-repo.rst (?)
... 2 más
```

### Plantilla canónica detectada

Análisis de `user.rst` (vigente, version 1.3.0)
revela la estructura canónica esperada:

```
.. meta::
 :artefacto: AT_DM_CLASS_{NAME}
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: {Auth|RBAC|Calls|Reports|...}
 :estado: Vigente
 :version: 1.x.x
 ...

.. _dm_class_{name}:

====
{Name}
====

(prosa: descripción de 2-4 párrafos del rol de la clase
en el bounded context)

.. uml::
 :caption: Clase {Name} — descripción.

 @startuml

 class {Name} {
   atributos canónicos con tipo
   ──────────
   métodos / operaciones
 }

 (relaciones con otras clases del bounded context)
 (notes sobre BR/CNST aplicables)

 @enduml

(secciones adicionales: ciclo de vida, restricciones,
trazabilidad UCs)
```

### Auditoría STD_011 sobre clases vigentes

Pendiente de spot-check en stage 2 MEASURE. La
hipótesis: STD_011 ya se aplicó en las 26 vigentes
(commit `Fix cryptic PlantUML aliases in UC and
architecture files (STD_011)` del PR #12). Verificar.

### Priorización de los 41 stubs

Criterio: **# de UCs que usan la clase** (más usado
= más prioritario).

Top tentativo (a verificar con grep en casos-uso/):

1. Audit/audit-validator (P-09 cross-cutting)
2. Audit/audit-query-service (UC_PERM_10, UC_AUD_01..04)
3. Reports/agent-daily-stat-repo (UC_OPR_08, UC_RPT_12)
4. Reports/queue-daily-stat-repo (?)
5. RBAC/action (UC_PERM_08 menu items)
6. RBAC/exceptional-permission-repo (UC_PERM_07)
7. Reports/agent-report-service (UC_RPT_12)
8. ... (resto pendiente de mapeo)

### Plan tentativo Bloque B

DAG: stub aislado primero (sin dependencia inversa),
luego servicios que dependen de repos primero.

```
Phase 1 — entidades (no service): action, access-group-
          function, exceptional-permission-repo
Phase 2 — repos: *-repo files
Phase 3 — services: *-service files (dependen de repos)
Phase 4 — orchestrators: alert-hook, audit-validator
```

Esfuerzo estimado: 41 stubs × ~30 min/clase = **~20 h
de trabajo activo**. Realista en 3-4 sesiones.

## Bloque A — use-case-view (13 → ~83 archivos)

### Estado actual

13 archivos `uc-{module}.rst` con varios diagramas
embebidos cada uno. Patrón:

```rst
=== uc-access.rst ===
1 diagrama caso-uso del módulo (UCs ACC dentro de
rectangle MOD_Access).
0 diagramas de secuencia / actividad / estados.
```

Sólo el **diagrama caso-uso del módulo entero** — no
hay diagramas por UC individual.

### Restructura propuesta

Espejo de `casos-uso/`:

```
source/arquitectura-tecnica/use-case-view/
├── index.rst
├── auth/
│   ├── index.rst                       (overview Auth)
│   ├── uc-mod-overview.rst             (diag módulo)
│   ├── uc-auth-01/
│   │   ├── index.rst                   (overview UC)
│   │   ├── caso-de-uso.rst             (1 diagrama)
│   │   ├── secuencia.rst
│   │   └── actividad.rst
│   ├── uc-auth-02/...
├── users/...
├── access/...
├── permissions/...
├── admin/...
├── reports/...
├── alerts/...
├── pipeline/...
├── audit/...
├── logs/...
├── operator/...
├── supervision/...
└── caller/...
```

**Política:** un diagrama por archivo (uml-07).
Excepción documentada caso a caso si son variantes
del mismo escenario.

**Total estimado de archivos:**

- 1 root index
- 13 module dirs × 1 index + 1 mod-overview = 26
- ~83 UCs × 1 index + ~3 diagramas avg = ~330
- **~360 archivos totales** (vs 13 actuales)

### Política referencia vs duplicación

`casos-uso/{cluster}/{uc}/diagramas-uml/` ya tiene
TODOS los diagramas (caso-de-uso, secuencia,
actividad, estados, etc.) por cada UC.

**Decisión recomendada:** la vista arquitectónica
**referencia** los archivos de spec via `:doc:`. NO
duplica. Aporta:

- Contexto arquitectónico (bounded context donde vive
  el UC)
- Actores externos al sistema (vs internos)
- Vista módulo (UCs agrupados por MOD_)
- Trazabilidad a clases del domain-model

Esto reduce drásticamente el número de archivos nuevos
a crear (no se copian diagramas, solo se referencian +
prosa contextual breve).

**Conteo revisado:** ~14 module index + ~83 UC index =
~97 archivos nuevos. Resto se reusa.

### Plan tentativo Bloque A

Esfuerzo: **~97 archivos × ~10 min/archivo = ~16 h**.
Pero altamente paralelizable y mecánico (template +
referencias).

## Plan integrado A + B

### Stage 5 STRATEGY (próximo)

Decisión clave a tomar:

- **Opción 1 (paralela):** abordar A y B en paralelo,
  WPs separados.
- **Opción 2 (secuencial B→A):** completar domain-model
  primero, luego use-case-view (porque la vista UC
  referencia clases del domain).
- **Opción 3 (secuencial A→B):** restructurar use-case-view
  primero, luego completar clases (visualizar UC ↔ clase
  helps clase design).

**Recomendación:** Opción 2 (B → A). Razones:

- Las clases son fundamento; los UCs las usan.
- Spec de clase clara → diagrama arquitectónico claro.
- Los stubs ya marcan deuda visible; resolverlos
  primero da valor inmediato.

### Output del WP discover

Este archivo + `wp-state.md` ya capturan el análisis.

Próximo paso: aprobación de Opción 2 → abrir 2 WPs
secuenciales:

- WP-A: domain-model-stubs-completion (priorizado por
  # UCs)
- WP-B: use-case-view-restructure (depende de A)

## Bloqueo

WP predecesor plantuml-svg-prerender está en EXECUTE
(T-009 corriendo: 968 SVGs renderizados de 1007 al
06:43, ~96%). Este WP es independiente y puede
proceder en paralelo.

## Veredicto

✅ Análisis completo. Aprobar Opción 2 (B antes de A)
y abrir WPs hijos para implementación.
