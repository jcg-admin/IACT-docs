```yml
created_at: 2026-05-05 06:43:00
updated_at: 2026-05-05 07:00:00
project: IACT-docs
work_package: 2026-05-05-06-41-02-arq-tecnica-uml-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Decisions log — arq-tecnica-uml-deepening

Registro de decisiones tomadas durante la ejecución del WP.
Cada decisión incluye: contexto, opciones consideradas,
opción elegida, justificación, fecha, refs.

----

## D-01 — Distinción clase vs. objeto formalizada en STD-012

**Fecha:** 2026-05-05

**Contexto:** El ejecutor preguntó la diferencia entre
``domain-model`` y ``diagrama-de-objetos`` antes de
arrancar la implementación de stubs.

**Opciones consideradas:**

1. Documentar inline en cada archivo de domain-model.
2. Crear nuevo standard.
3. Asumir convención sin documentar.

**Opción elegida:** 2. Crear ``STD-012: Tipos de Diagramas
UML — Cuándo y Dónde Usar Cada Uno``.

**Justificación:**

- Distinción es transversal (afecta todo el proyecto).
- Anti-patrones identificados: clase con valores, objeto
  sin clase, múltiples clases en un archivo.
- Inline duplica conocimiento; estándar centraliza.

**Refs:**
``source/normativa/estandares/std-012-tipos-de-diagramas-uml.rst``,
commit ``298f43d6``.

----

## D-02 — Orden de bounded contexts: Audit → Alerts → RBAC → Reports

**Fecha:** 2026-05-05

**Contexto:** 41 stubs distribuidos en 4 bounded contexts:
Audit (9), Reports (17), RBAC (10), Alerts (5).

**Opciones consideradas:**

1. Por % de gap descendente (Audit 90 → Reports 77 → RBAC 63
   → Alerts 63).
2. Por # absoluto descendente (Reports 17 → RBAC 10 → Audit 9
   → Alerts 5).
3. Por dependencia técnica (cluster con menos dependencias
   primero).

**Opción elegida:** 1 con ajuste — Audit primero (mayor %),
luego Alerts (más pequeño = momentum), luego RBAC, luego
Reports (más grande, repetitivo, al final).

**Justificación:**

- Audit es transversal (P-09 audit-or-abort cross-cutting).
  Resolverlo desbloquea claridad para los demás.
- Alerts es pequeño pero el ``AlertHook`` ya quedó
  documentado en Audit como bridge — ergonomico continuar.
- Reports es repetitivo (``*-report-service``,
  ``*-repo``) — al final aprovecha plantilla establecida.

**Refs:** análisis ``discover/uml-deepening-analysis.md``
sección "Plan integrado A + B".

----

## D-03 — Identificadores en inglés, prosa en español

**Fecha:** 2026-05-05

**Contexto:** El ejecutor recordó que clases, atributos,
funciones y firmas van en inglés.

**Opciones consideradas:**

1. Todo en español (rompe convención).
2. Mixto (clases inglés, atributos español).
3. Estricto inglés para identificadores (alineado con
   STD-008 y modelo RBAC v5.5.0).

**Opción elegida:** 3.

**Justificación:**

- STD-008 ``naming-identificadores`` ya lo establece.
- Consistencia con el modelo RBAC v5.5.0 que ya usa inglés.
- Diff cognitivo entre prosa y código bajo: prosa explica
  el qué/por qué, código define el cómo.

**Refs:** STD-008, modelo-rbac-iact v5.5.0.

----

## D-04 — Notación de relaciones UML aplicada uniformemente

**Fecha:** 2026-05-05

**Contexto:** Cada bounded context tiene clases que se
relacionan vía composición, agregación, dependencia,
asociación.

**Opciones consideradas:**

1. Solo flechas simples (``-->``).
2. Notación completa UML (``*--``, ``o--``, ``..>``,
   ``-->``).
3. Texto descriptivo en notas.

**Opción elegida:** 2 con consistencia:

- ``*--`` composición fuerte (parte constitutiva, sin
  vida propia)
- ``o--`` agregación (parte con vida propia)
- ``..>`` dependencia (usa, sin poseer)
- ``-->`` asociación direccional simple
- ``--`` asociación bidireccional simple

**Justificación:**

- Per uml-04 ``uso-relaciones`` y uml-02 OO concepts.
- Permite comprender ciclos de vida sin leer prosa.
- Distinción crítica para diseño: composición ↔ agregación
  cambia el contrato de cleanup / cascade.

**Refs:** uml-02-orientacion-objetos/composicion.rst,
uml-02/agregacion.rst, uml-02/asociaciones.rst.

----

## D-05 — Aliases auto-documentados en class diagrams

**Fecha:** 2026-05-05

**Contexto:** STD-011 establece aliases auto-documentados
en diagramas de secuencia, comunicación, actividad.
Pregunta tácita: ¿aplica también en class diagrams?

**Decisión:** sí, se aplica de forma natural.

**Justificación:**

- En class diagrams el "alias" típicamente coincide con el
  nombre de la clase (``class User`` ya es
  auto-documentado).
- Cuando hay enums o subclases, se usa el nombre completo
  (``enum AlertState``, ``enum Severity``) en lugar de
  abreviaciones.
- No se introducen aliases crípticos como ``A``, ``U``.

**Refs:** STD-011.

----

## D-06 — Trazabilidad UC → clase via ``:doc:`` (no duplicar)

**Fecha:** 2026-05-05

**Contexto:** STD-012 §4 establece la política. Aplicada en
cada clase del domain-model: la sección "Trazabilidad a
UCs" cita los UCs que la usan.

**Justificación:**

- DRY: la spec del UC ya documenta el flujo.
- Cuando cambia un UC, no hay que actualizar 5 archivos
  de domain-model también; el :doc: link sigue válido.
- Facilita navegación bidireccional UC ↔ clase.

----

## D-07 — Encapsulamiento explícito (- privados, + públicos)

**Fecha:** 2026-05-05

**Contexto:** uml-02 ``encapsulamiento`` enseña ocultar
implementación detrás de interfaz pública. ¿Aplicar en
diagramas?

**Decisión:** sí. Atributos privados con ``-``, públicos
con ``+``. Operaciones todas expuestas (``+``) salvo helpers
internos (``-``).

**Justificación:**

- Comunica el contrato: qué pueden tocar otras clases vs.
  qué es interno.
- Anti-patrón frecuente: diagramas con todos los atributos
  ``+`` permiten cualquier uso, viola encapsulamiento.
- Consistente con patrón de ``User`` (clase canónica
  vigente).

**Refs:** uml-02/encapsulamiento.rst.

----

## D-08 — Una clase por archivo en domain-model (estricto)

**Fecha:** 2026-05-05

**Contexto:** STD-012 §3.2 lo establece. Aplicado en todos
los stubs completados.

**Decisión:** sin excepciones en domain-model.

**Justificación:**

- Filenamesreflejan el catálogo: navegar el directorio =
  navegar el dominio.
- Diff de un solo concepto por commit; revisión más fácil.
- Refactor de una clase no genera ruido en diff de otra.

----

## D-09 — Build logs convention (timestamp ISO en WP)

**Fecha:** 2026-05-05

**Contexto:** El ejecutor estableció la regla. Implementada
con ``scripts/build-with-log.sh``.

**Decisión:** todo ``make`` o ``sphinx-build`` durante WPs
debe pasar por el wrapper.

**Justificación:**

- Auditabilidad de cuándo y con qué resultado se ha
  construido.
- Trazabilidad de fallos a estados específicos del repo
  (HEAD + branch + sphinx version).

**Refs:** ``scripts/build-with-log.sh``,
``.thyrox/context/work/{wp}/build-logs/README.md``.

----

## D-10 — Documentar en este log toda decisión de diseño del WP

**Fecha:** 2026-05-05

**Contexto:** El ejecutor pidió documentar todas las
decisiones en el WP actual.

**Decisión:** este archivo es el ``decisions-log.md``
canónico del WP. Cada decisión D-NN va aquí; el wp-state.md
solo refiere a este log.

**Justificación:**

- Centraliza decisiones; evita dispersión en commits y
  prosa de archivos individuales.
- Permite auditoría rápida del razonamiento.
- Plantilla replicable a otros WPs.

----

## D-11 — Excepción STD-008 para ``ServicioReportes`` (facade legacy)

**Contexto:** ``ServicioReportes`` es la facade histórica
del sistema y expone métodos en castellano
(``llamadas_abandonadas``, ``menu_redirigidos``,
``clientes``, ``centros_transferencia``).

**Decisión:** mantener el nombre y métodos en castellano
como **excepción documentada** a STD-008. Marcar como
*deprecated* para clientes nuevos. Los servicios delegados
(``AbandonoReportService``, etc.) usan inglés.

**Justificación:**

- Romper la API legada implicaría migrar consumidores
  externos fuera del scope del WP.
- La facade no contiene lógica — solo delega.
- La excepción queda contenida en un único archivo y
  documentada inline.

----

## D-12 — Gap de rigor UML reconocido (uml-04 no aplicado)

**Contexto:** durante la completación de los 41 stubs se
priorizó velocidad sobre rigor UML. Los 37 archivos
escritos NO aplican consistentemente los conceptos de
``source/base-cognitiva/_uml/uml-04-uso-relaciones/``:

1. Multiplicidades (``1``, ``0..1``, ``*``, ``1..*``).
2. Roles en extremos de asociación.
3. Restricciones (``{ordered}``, ``{unique}``, ``{readOnly}``).
4. Asociaciones calificadas (``[key]``).
5. Clases de asociación (``AccessGroupFunction`` mal
   modelada como clase suelta).
6. Generalización / clases abstractas
   (``BaseReportService``, ``Repository`` patrón).
7. Asociaciones reflexivas (``Menu`` jerárquico,
   ``NavDomain``).
8. Distinción dependencia por uso vs por retorno.

**Decisión:** completar los 4 stubs pendientes con el
patrón actual (no bloquear merge), luego abrir un WP
dedicado ``arq-tecnica-uml-rigor-pass`` que recorra los
~37 archivos finales aplicando los 8 puntos.

**Justificación:**

- Cerrar el alcance original (41 stubs Vigentes) sin
  arrastrar el rigor pendiente al WP en curso.
- Trazabilidad limpia: un WP = un objetivo.
- El nuevo WP puede usar el catálogo
  ``uml-04-uso-relaciones/`` como checklist por archivo.

----

## Pendientes de decisión

- D-13 (futuro): si crear sub-bounded-contexts cuando
  Reports tiene 22 clases (¿AgentReports vs QueueReports?).
- D-14 (futuro): cómo manejar clases con dependencias
  cíclicas si aparecen en el rigor-pass.
