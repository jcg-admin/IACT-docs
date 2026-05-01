```yml
created_at: 2026-05-01 02:01:06
project: IACT-docs
work_package: 2026-05-01-02-01-06-domain-model-canonization
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
```

# Exit Conditions — Canonización del modelo de dominio

Condiciones formales para cerrar este WP. Solo el
ejecutor ordena cierre (I-011); estas condiciones
son los pre-requisitos verificables.

## Entregables publicados

- [ ] ``discover/domain-elicitation.md`` — plan de
  elicitación adaptada con deviation explícita
  del skill ``rm-elicitation``.
- [ ] ``discover/risk-register.md`` (R-01..R-08).
- [ ] ``discover/exit-conditions.md`` (este
  archivo).
- [ ] ``analyze/domain-class-candidates.md`` —
  sustantivos candidatos a clase + IEEE 830 +
  resolución de conflictos.
- [ ] ``design/iact-domain-model.md`` con el
  PlantUML canónico promovido a artefacto del
  proyecto bajo ``source/requisitos/`` (path final
  a decidir en Stage 6).
- [ ] ``pilot/uc-vs-domain-validation.md`` —
  matriz UC × clase + huérfanos.
- [ ] ``track/lessons-learned.md`` al cierre.

## Calidad del modelo de clases

- [ ] Cada clase tiene: nombre canónico, ≥1
  atributo, ≥1 operación, ≥1 asociación con otra
  clase del modelo o nota explícita "isla
  intencional".
- [ ] Cada clase está agrupada en un **bounded
  context** del modelo (Auth, RBAC,
  Reportes/Métricas, Pipeline ETL, Alertas,
  Auditoría, Logs — los 7 contextos derivados de
  los 9 clusters de UC).
- [ ] Asociaciones tienen cardinalidad explícita
  (``1``, ``0..1``, ``*``, ``1..*``).
- [ ] Restricciones canónicas (CNST_*) y reglas
  de negocio (BR_*) aparecen como notas en las
  clases / asociaciones que las llevan.

## Reconciliación 61 vs 97 UCs

- [ ] Causa raíz documentada por escrito en
  ``analyze/domain-class-candidates.md`` § 1.
- [ ] Si la cifra "97" del cajón pedagógico está
  obsoleta, ``analisis-dominio.rst § 11`` se
  actualiza con la cifra real (PR aparte o en este
  WP).
- [ ] Si los 36 UCs faltantes deben crearse, se
  documentan como deuda separada (no se crean en
  este WP).

## Cobertura UC × clase

- [ ] **100%** de los UCs del inventario apuntan
  a ≥1 clase del modelo (ninguna acción opera
  fuera del modelo).
- [ ] **100%** de las clases del modelo aparecen
  como sujeto / objeto en ≥1 UC (ninguna clase
  huérfana — si la hay, se justifica o se elimina).
- [ ] La matriz se presenta en
  ``pilot/uc-vs-domain-validation.md``.

## Lenguaje ubicuo

- [ ] Glosario publicado con ≥20 términos,
  cubriendo: entidades del dominio, módulos de
  implementación (Python apps), constraintes
  (CNST_*), agrupadores (AGR-*).
- [ ] Cada término distingue **concepto del
  dominio** vs **módulo de implementación**
  cuando aplique (e.g. ``Sesion`` clase vs
  ``auth_app`` módulo).

## Calidad del diagrama

- [ ] PlantUML descompuesto por bounded context
  (≤7 sub-diagramas) más un overview cross-context.
- [ ] ``make html`` con 0 warnings, 0 errors
  (gate I-015).
- [ ] Sintaxis PlantUML valida con render local.

## Gates THYROX

- [ ] I-011 — cierre solo por orden explícita.
- [ ] I-012 — ningún hallazgo SPECULATIVE en
  conclusiones.
- [ ] I-013 — claims heredados del WP previo
  (uc-inventory) re-verificados contra el modelo
  antes de propagarse.
- [ ] I-015 — script
  ``validate-phase-completion.sh`` exit 0 antes
  de cerrar.

## Dependencias hacia el WP previo

- [ ] El WP
  ``2026-04-30-22-45-55-rm-uc-relationships-analysis``
  permanece **abierto** durante este trabajo.
- [ ] Al cerrar este WP, se anota en el WP
  previo (en su track/) que ahora puede
  retomarse el análisis de relaciones sobre base
  validada.
