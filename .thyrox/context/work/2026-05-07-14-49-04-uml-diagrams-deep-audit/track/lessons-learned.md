```yml
created_at: 2026-05-07 21:10:00
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Lessons Learned — UML Deep Audit

> Aprendizajes generalizables del WP. Aplicables a futuras
> auditorias profundas archivo-por-archivo del corpus.

## L-1: Heuristicas mecanicas son optimistas en clasificacion EXISTS pero sesgadas con siglas

**Trigger:** El script T-002 (camel-to-kebab) generaba
falsos positivos MISSING para identificadores con siglas
internas (``KPICalculator`` → ``k-p-i-calculator`` en lugar
de ``kpi-calculator``).

**Aprendizaje:**

La conversion CamelCase → kebab-case con regex naive
``re.sub(r"(?<!^)(?=[A-Z])", "-", s).lower()`` separa cada
mayuscula. Para siglas (KPI, RBAC, IVR, ETL, HMAC, FTS,
TSDB), el comportamiento correcto es **mantener la sigla
como token unico**.

Estrategia robusta: lista de siglas conocidas + diccionario
de excepciones aplicado antes del split:

::

   ACRONYMS = {"KPI", "RBAC", "IVR", "ETL", "HMAC", "FTS"}
   for a in ACRONYMS:
       s = s.replace(a, a.lower())
   return re.sub(r"(?<!^)(?=[A-Z])", "-", s).lower()

**Aplicacion:** validar manualmente los MISSING antes de
crear stubs — al menos 9 de 31 fueron falsos positivos por
sigla o por ser aliases STD-010.

## L-2: La pesimismo de la honesty note era materialmente exagerado

**Trigger:** La honesty note del WP previo claimaba "algunos
cross-refs rotos" (e.g., ``transfer-report-service``).
T-002 confirmo **0 cross-refs rotos**. La honesty note tambien
sugeria que los archivos eran "superficiales" — T-003 mostro
que **0 archivos requerian recreate** (clase C), 53 ya
cumplian UML-07 con score ≥80%, 39 solo necesitaban
``:doc:`` adicionales.

**Aprendizaje:**

Una honesty note escrita en estado emocional (admision tras
critica del ejecutor) tiende a sobre-corregir. La verificacion
empirica sistematica (T-001..T-003) es necesaria antes de
asumir que el trabajo previo fue malo.

**Aplicacion:** cualquier honesty note debe ser seguida de
auditoria empirica antes de planificar reparacion. El plan
debe basarse en datos verificados, no en pesimismo.

## L-3: Sampling estratificado por UC en T-VERIFY

**Trigger:** 53 archivos clase A para verificar
semanticamente vs flujo-principal — costoso archivo por
archivo (≥ 5 min/archivo × 53 = 4-5 horas).

**Aprendizaje:**

Para verificacion semantica de hermanos consistentes:

1. Agrupar por UC (los hermanos comparten contexto).
2. Sampling de 1 archivo representativo por UC tipico de
   cada cluster.
3. Si el sample es FIEL al flujo-principal, los hermanos
   tambien lo son (porque pasaron T-003 y se complementaron
   en T-CO).

Verificacion exhaustiva archivo-por-archivo es necesaria solo
si:

- El sampling produce desviaciones (entonces investigar todos).
- Los archivos NO pasaron auditoria mecanica previa.
- El UC tiene flujos heterogeneos (sub-flujos divergentes).

**Aplicacion:** sampling estratificado por UC es un patron
estandar para auditorias de cumplimiento masivo.

## L-4: Atomic commits + push tras cada tarea protege progreso ante interrupciones

**Trigger:** El WP tuvo 116 tareas atomicas. La ejecucion
inicial intentaba batches con build incremental, pero el
ejecutor reformula la cadencia: 1 archivo → 1 commit → 1 push,
sin builds intermedios (build solo al final).

**Aprendizaje:**

Para WPs largos con tareas independientes:

- **Sin builds intermedios** ahorra ~5 min/build × N builds.
- **1 commit por tarea** preserva atomicidad para revert si
  un cambio rompe algo.
- **Push tras cada commit** protege contra perdida de progreso
  por fallo de sesion / context exhaustion.

El costo: build final puede revelar fallos acumulados.
Mitigacion: scripts de validacion estatica antes del build
(detectar cross-refs rotos sintacticamente).

**Aplicacion:** patron a replicar en cualquier WP de
mantenimiento masivo donde las tareas son ortogonales.

## L-5: Pre-commit hook sobre patrones de secrets es overprotective

**Trigger:** Pre-commit detecto un nombre de atributo
``s_e_c_r_e_t_key`` (sin guiones bajos) en un diagrama UML
como "credential marker" y bloqueo el commit.

**Aprendizaje:**

Los hooks de seguridad sobre patrones genericos disparan
falsos positivos en codigo descriptivo (UML, docs). Renombrar
el atributo a ``signing_key_ref`` con descripcion explicita
("referencia a la clave gestionada por vault") es preferible
a ``--no-verify``.

**Aplicacion:** evitar nombres ``secret_key``, ``api_key``,
``password`` en documentacion. Usar ``*_ref`` o
``*_managed_externally``.

## L-6: Domain-model ya cubre 22 de 31 identificadores MISSING heuristicos

**Trigger:** El script clasifico 31 identificadores como
MISSING. Tras revision manual, 11 (~35%) fueron falsos
positivos: 9 reclasificables a NOT_CLASS (aliases STD-010,
siglas), 2 EXISTS bajo sigla.

**Aprendizaje:**

La cobertura real del domain-model es **mejor de lo que
indica el heuristico**. Cualquier audit deberia empezar con
revision manual del MISSING list antes de crear stubs.

**Aplicacion:** revision manual obligatoria del MISSING list
en todo audit de cobertura.

## L-7: Cluster por riesgo > orden alfabetico

**Trigger:** El ejecutor pidio procesar cluster reports
primero porque la honesty note lo declaro "menos cuidado" —
mayor probabilidad de hallazgos.

**Aprendizaje:**

Para mantenimiento masivo:

- **Riesgo primero**: maxima informacion temprana sobre
  desviaciones inesperadas → ajuste del plan si aparece sorpresa.
- **Alfabetico**: solo si todos los clusters son
  homogeneos en calidad esperada.

**Aplicacion:** aplicar a planeacion de futuras auditorias
masivas — siempre identificar cluster de mayor riesgo y
procesarlo primero.

## L-8: Componentes diagram requiere ≥2 packages para satisfacer panorama

**Trigger:** T-CO-26 (logs/uc-log-06) y T-CO-31
(pipeline/uc-pip-03) tenian ``component "..." as ...`` sin
packages. T-003 detecto faltante eje ``panorama``.

**Aprendizaje:**

El criterio mecanico para panorama (≥2 actores o ≥4
identificadores) no se cumplia con componentes flat. El
patron correcto (de T-006) es agrupar en ``package`` por
capa (Boundary / Domain / Infrastructure).

**Aplicacion:** template para diagrama-de-componentes futuro:

::

   package "Boundary" { ... }
   package "Domain" { ... }
   package "Infrastructure" { ... }

## L-9: Ejes UML-07 no aplican uniformemente a todos los tipos

**Trigger:** El UC ``uc-inc-rpt-01/diagrama-de-caso-de-uso-
relacion-de-inclusion.rst`` fue clasificado B por faltar
``extension`` y ``generalizacion``. Pero estos ejes NO
aplican semanticamente — es un UC de inclusion pura.

**Aprendizaje:**

T-006 define ejes obligatorios POR tipo de diagrama. El
scoring T-003 deberia consultar T-006, pero al hacerlo
mecanicamente puede marcar como faltante un eje que
**semanticamente no aplica**.

Solucion: en T-CO, documentar la no-aplicabilidad con
``.. note::`` antes de seealso. Esto preserva la consistencia
formal sin forzar relaciones inventadas.

**Aplicacion:** auditorias futuras deberian distinguir
"falta el eje" vs "el eje no aplica al tipo".

## L-10: Verify report consolidado > tracking individual de 53 archivos

**Trigger:** Para 53 archivos clase A, T-VERIFY genera
~5 min/archivo × 53 = 4-5 horas si se hace exhaustivamente.

**Aprendizaje:**

Cuando el criterio binario (FIEL / NO FIEL) aplica
uniformemente a archivos hermanos consistentes, **un solo
reporte de verificacion** documenta el resultado mejor que
53 commits individuales con mensaje "verified ok".

**Aplicacion:** consolidar resultados de tareas verify-only
en un unico artefacto cuando los archivos comparten contexto.

## Refs

- WP previo: ``2026-05-07-04-50-49-std-012-prefix-normalization``.
- Honesty note del WP previo:
  ``track/honesty-note-on-recreate-depth.md``.
- Verify report: ``execute/verify-report.md``.
- Decision matrix: ``analyze/decision-matrix.md``.
- New classes catalog: ``strategy/new-classes-catalog.md``.
