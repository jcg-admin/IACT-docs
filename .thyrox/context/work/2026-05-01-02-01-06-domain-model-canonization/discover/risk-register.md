```yml
created_at: 2026-05-01 02:01:06
project: IACT-docs
work_package: 2026-05-01-02-01-06-domain-model-canonization
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
```

# Risk Register — Canonización del modelo de dominio

## R-01 — Elicitación adaptada sin stakeholders reales

- **Descripción:** El skill ``rm-elicitation`` exige
  confirmación con stakeholders reales. Este WP
  trabaja con el ejecutor como proxy y con el
  corpus existente como fuente. La adaptación
  puede ocultar gaps que sólo aparecerían en
  conversaciones con product / negocio reales.
- **Probabilidad:** Alta.
- **Impacto:** Medio — el modelo será suficiente
  para anclar UCs internamente, insuficiente
  para validar que el dominio refleje el negocio
  real del call center.
- **Mitigación:** Documentar la adaptación como
  deviation explícita en
  ``discover/domain-elicitation.md``. Marcar el
  modelo final como "validado contra corpus, no
  contra stakeholders externos" hasta que haya
  oportunidad de hacerlo.

## R-02 — Heredar errores del corpus existente

- **Descripción:** Si los 61 UCs del catálogo
  contienen errores semánticos (clases mal
  identificadas, responsabilidades en la entidad
  equivocada), el modelo de dominio extraído
  hereda esos errores.
- **Probabilidad:** Alta — H-07 (UC_USR_01
  referencia UC_ACC_07 inexistente) y H-09/H-10
  (mezcla de nomenclaturas) son evidencia
  observable del riesgo.
- **Impacto:** Alto — invalida el modelo como
  fuente de verdad.
- **Mitigación:** Cruzar el modelo extraído del
  corpus con
  ``analisis-dominio.rst § 7`` (que es un análisis
  metodológico independiente sobre el mismo
  dominio). Discrepancias se elevan como hallazgos.

## R-03 — Discrepancia 61 vs 97 UCs sin resolver

- **Descripción:** ``analisis-dominio.rst § 11``
  declara 97 UCs; el inventario verifica 61. Si
  los 36 faltantes existieron en una versión
  previa pero fueron consolidados, el conteo del
  cajón está obsoleto. Si nunca existieron y la
  cifra fue inventada, hay deuda metodológica.
- **Probabilidad:** Media.
- **Impacto:** Alto — bloquea exit condition.
- **Mitigación:** Stage 1 incluye análisis git
  log + lectura de ``index.rst`` por cluster +
  decisión por escrito.

## R-04 — Inflación de clases

- **Descripción:** Cada sustantivo del corpus
  podría convertirse en una clase, multiplicando
  el modelo a ~50 entidades sin valor analítico.
- **Probabilidad:** Media.
- **Impacto:** Medio — el modelo se vuelve
  ilegible y deja de ser útil como referencia
  compartida.
- **Mitigación:** Aplicar el filtro de Abbott
  (``analisis-dominio.rst § 12``): solo se
  promueven a clase los sustantivos que
  representan **conceptos persistentes con
  identidad propia y operaciones de negocio**.
  Atributos, relaciones y eventos transitorios
  no son clases.

## R-05 — Lenguaje ubicuo no consensuado

- **Descripción:** El glosario producido aquí
  podría chocar con vocabulario ya enraizado en
  el código de IACT (``auth_app``, ``audit_log``,
  ``rpt_app``).
- **Probabilidad:** Media.
- **Impacto:** Bajo — los nombres de módulos
  Python no tienen por qué coincidir con los
  nombres de clases del modelo conceptual.
- **Mitigación:** Glosario aclara explícitamente
  la diferencia entre
  ``módulo de implementación`` (``auth_app``) y
  ``clase del dominio`` (``Sesion``).

## R-06 — El diagrama crece más allá de lo
legible

- **Descripción:** 14+ clases con todas sus
  asociaciones en un solo PlantUML produce un
  diagrama no consumible.
- **Probabilidad:** Alta.
- **Impacto:** Medio.
- **Mitigación:** Descomponer por **bounded
  context** (DDD): Auth, RBAC,
  Reportes/Métricas, Pipeline ETL, Alertas,
  Auditoría, Logs. Un diagrama por contexto + un
  overview que sólo muestre los puentes
  inter-contexto.

## R-07 — Sub-modelado del estado dinámico

- **Descripción:** El diagrama de clases captura
  estructura, no transiciones de estado. Sesion,
  Alerta y EjecucionETL tienen estados con
  transiciones reglamentadas (CNST_*).
- **Probabilidad:** Alta — el diagrama de clases
  por definición no muestra estado dinámico.
- **Impacto:** Bajo aquí — los diagramas de
  estado son artefactos complementarios; este WP
  sólo produce el de clases.
- **Mitigación:** Documentar al cierre cuáles
  clases requieren un diagrama de estado en un
  WP posterior.

## R-08 — Reproducción de material externo

- **Descripción:** Las referencias a DDD (Evans
  2003) y a guías de modelado (Schmuller,
  *Aprendiendo UML en 24 horas*) podrían inducir
  copia de texto literal.
- **Probabilidad:** Media.
- **Impacto:** Alto — viola política del
  proyecto (cajón metodológico debe ser original,
  citando fuentes).
- **Mitigación:** Toda escritura es original.
  Las fuentes externas se citan por nombre y
  página, sin transcripción ni paráfrasis cercana.
