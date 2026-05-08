```yml
project: IACT-docs
work_package: 2026-05-05-06-41-02-arq-tecnica-uml-deepening
created_at: 2026-05-05 06:41:02
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: thyrox
methodology_step: thyrox:discover
predecessor_wp: 2026-05-05-05-44-25-plantuml-svg-prerender
target: Profundizar arquitectura-tecnica/use-case-view + domain-model
```

# WP — arquitectura-tecnica UML deepening

## Trigger

El ejecutor solicita análisis para profundizar dos
sub-árboles de `source/arquitectura-tecnica/`:

### Bloque A — use-case-view

Estado actual: 13 archivos (1 index + 12 módulos
``uc-{module}.rst``), cada uno con varios diagramas
embebidos del módulo entero.

**Objetivo:** restructurar para que **espeje
`source/requisitos/casos-uso/`** (un directorio por
módulo, y dentro un archivo por UC, y dentro de cada UC
**un archivo por diagrama** — mismo principio que ya se
aplicó en casos-uso/).

**Referencia metodológica:**
``source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/``
(11 archivos: el panorama, comprension dominio /
casos / usuarios, representacion modelo, inclusion,
extension, generalizacion, profundizacion, etc.).

**Criterio de excepción** (uml-07 admite múltiples
diagramas por archivo cuando son variantes de un mismo
escenario): aceptado caso a caso, documentado en el
archivo.

**Propósito:** la vista arquitectónica de UCs es
**solo diagramas** (sin prosa de spec). Compara con la
vista de requisitos (12-part spec) que ya existe.

### Bloque B — domain-model

Estado actual: 69 archivos en
`source/arquitectura-tecnica/domain-model/` (uno por
clase). De estos:

- **28 clases canónicas completas** (estado
  ``Vigente``, version ``1.x.x``)
- **41 clases stub** (estado ``Pendiente``, version
  ``0.0.1`` o ``0.1.0``), con TODO marker

**Objetivo:** completar los 41 stubs con:

- Atributos canónicos (tipo + descripción)
- Métodos / operaciones de negocio
- Firmas de funciones (parámetros + retorno)
- Diagrama PlantUML de la clase con
  ALIASES STD_011-compliant
- Relaciones con otras clases del bounded context
- Trazabilidad a UCs que la usan
- Restricciones (BR / CNST aplicables)

**Normativa de aliases:**
``source/normativa/estandares/std-011-alias-diagramas-uml.rst``

Resumen: aliases deben ser **auto-documentados** —
"Un alias por sí mismo debe revelar el rol o nombre del
participante". Prohibido: 1-letra, 2-letras, acrónimos.
Permitido: nombre de función RBAC, nombre de clase
PascalCase, rol completo.

## Inventario actual

### Bloque A — use-case-view actual

```
source/arquitectura-tecnica/use-case-view/
├── index.rst
├── uc-access.rst
├── uc-admin.rst
├── uc-alerts.rst
├── uc-audit.rst
├── uc-auth.rst
├── uc-caller.rst
├── uc-logs.rst
├── uc-operator.rst
├── uc-permissions.rst
├── uc-pipeline.rst
├── uc-reports.rst
├── uc-supervision.rst
└── uc-users.rst   (13 files total)
```

Cada archivo contiene `.. uml::` directives con uno o
más diagramas (caso de uso del módulo + opcionales
secuencia / actividad).

### Bloque B — domain-model actual

69 archivos. Distribución por bounded context:

| Bounded Context | Total | Vigente | Pendiente |
|-----------------|-------|---------|-----------|
| Auth | ? | ? | ? |
| RBAC | ? | ? | ? |
| Calls | ? | ? | ? |
| Reports & Metrics | ? | ? | ? |
| Pipeline ETL | ? | ? | ? |
| Alerts | ? | ? | ? |
| Audit | ? | ? | ? |
| Logs | ? | ? | ? |

Distribución exacta a calcular en discover. 41 stubs
identificados por:

```bash
grep -lE "estado: Pendiente|version: 0\.[01]" \
  source/arquitectura-tecnica/domain-model/*.rst | wc -l
# = 41
```

Spot check muestra clases stub:
- `action.rst` (RBAC) — solo el shell, atributos pendientes
- `abandono-report-service.rst` (Reports) — sin
  operaciones definidas
- `agent-daily-stat-repo.rst` — sin métodos repo
- `alert-rule.rst` — atributos parciales
- ...

## Áreas a revisar (por dominio del WP)

### A1 — Espejo de estructura de casos-uso

Validar correspondencia 1:1 entre clusters:

| casos-uso/ | use-case-view/ | Acción |
|-----------|----------------|--------|
| auth/ (uc-auth-01..05) | uc-auth.rst | descomponer |
| users/ (uc-usr-01..04) | uc-users.rst | descomponer |
| access/ (uc-acc-01..05,08,09) | uc-access.rst | descomponer |
| permissions/ (uc-perm-01..10) | uc-permissions.rst | descomponer |
| admin/ (uc-adm-01..03) | uc-admin.rst | descomponer |
| reports/ (uc-rpt-01..04,07..17) | uc-reports.rst | descomponer |
| alerts/ (uc-alr-01..05) | uc-alerts.rst | descomponer |
| pipeline/ (uc-pip-01..04) | uc-pipeline.rst | descomponer |
| audit/ (uc-aud-01..04) | uc-audit.rst | descomponer |
| logs/ (uc-log-01..07) | uc-logs.rst | descomponer |
| operator/ (uc-opr-01..10) | uc-operator.rst | descomponer |
| supervision/ (uc-sup-01..03) | uc-supervision.rst | descomponer |
| caller/ (uc-cli-01..05) | uc-caller.rst | descomponer |

**Restructura propuesta:**

```
source/arquitectura-tecnica/use-case-view/
├── index.rst
├── auth/
│   ├── index.rst                    (overview Module)
│   ├── uc-auth-01/
│   │   ├── index.rst                (overview UC)
│   │   ├── caso-de-uso.puml/.rst   (un diagrama)
│   │   ├── secuencia.rst
│   │   ├── actividad.rst
│   │   └── estados.rst
│   ├── uc-auth-02/...
├── users/...
├── access/...
└── ...
```

**Política:** un diagrama por archivo. Excepción
documentada cuando son variantes del mismo escenario
(ej. "actividad — flujo principal" + "actividad — flujo
alterno" en mismo archivo si están relacionados).

### A2 — Tipos de diagramas por UC (uml-07)

Tipos aplicables del catálogo uml-07:

- **Caso de uso** (siempre): actor + relaciones
  include/extend.
- **Secuencia**: cuando hay interacción entre múltiples
  componentes.
- **Actividad**: flujo de control.
- **Estados**: cuando la entidad tiene state machine.
- **Comunicación** (raro): variante de secuencia.

Los diagramas spec ya viven en
`source/requisitos/casos-uso/{cluster}/{uc}/diagramas-uml/`.
La pregunta arquitectónica: **¿se duplican o se
referencian?**

**Decisión sugerida:** la vista arquitectónica
**referencia** los archivos de spec (via `:doc:`) y
agrega contexto arquitectónico (bounded context,
sistema actores externos). No duplica.

### B1 — Catálogo de las 28 clases vigentes

Verificar que las 28 clases con estado ``Vigente``
cumplen STD_011 en sus aliases. Spot-check al menos
5 por bounded context.

### B2 — 41 stubs a completar

Para cada uno determinar:

- ¿Qué UC(s) la usan? (referencia inversa desde
  casos-uso/)
- ¿Qué atributos canónicos infieren los UCs?
- ¿Qué métodos / operaciones invocan los UCs?
- ¿Qué relaciones tiene con otras clases?
- ¿Qué BR/CNST aplican?

**Salidas esperadas:**

- Lista priorizada de stubs (por número de UCs que la
  usan)
- Plantilla canónica de archivo de clase
- DAG de dependencias entre clases stub

### B3 — Aliases STD_011 en domain-model

Verificar que los diagramas PlantUML de las 28 clases
vigentes ya cumplen STD_011. Si no, listar violaciones.

## Riesgos identificados

| ID | Riesgo | Severidad | Mitigación |
|----|--------|-----------|-----------|
| R-01 | Duplicación de diagramas entre vista
      requisitos y vista arquitectura | medio | usar
      `:doc:` references desde la vista
      arquitectónica |
| R-02 | use-case-view restructure rompe links
      existentes | medio | grep para detectar enlaces
      a `uc-{module}.rst` antes de eliminar |
| R-03 | 41 stubs requieren conocimiento de cada UC
      ↔ clase | alto | priorizar por # de UCs que
      usan; comenzar por más usadas |
| R-04 | Aliases STD_011 no se aplicaron consistentemente
      en clases vigentes | medio | spot-check antes
      de propagar |
| R-05 | use-case-view actual tiene calidad estética
      a preservar | bajo | spot-check vs nueva |
| R-06 | Esto pisa estructura del PR #12 si todavía
      no se mergeó | medio | trabajar en branch
      `claude/wp-merge-pr-review` extendiendo, no
      sobreescribiendo |

## Plan de output (Phase 1 DISCOVER)

`discover/uml-deepening-analysis.md` con:

- Inventario completo (28 vigentes + 41 stub) por
  bounded context y UC mapping
- Auditoría STD_011 sobre las 28 clases vigentes
- Auditoría de la estructura actual de use-case-view
- Restructura propuesta para use-case-view
- Plan priorizado para los 41 stubs (DAG)
- Plantilla canónica de archivo de clase de dominio
- Plantilla canónica de archivo de diagrama
  arquitectónico

Próximas fases: STRATEGY (cómo abordar el orden) →
PLAN → DESIGN/SPECIFY (templates) → DECOMPOSE
(T-NNN tasks) → EXECUTE.

## Bloqueo

WP predecesor `plantuml-svg-prerender` está en
EXECUTE (T-009 corriendo en background). Este WP
es independiente y se puede analizar en paralelo.
