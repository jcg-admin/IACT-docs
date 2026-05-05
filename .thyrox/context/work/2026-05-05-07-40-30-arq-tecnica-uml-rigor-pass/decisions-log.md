```yml
created_at: 2026-05-05 07:45:00
updated_at: 2026-05-05 07:45:00
project: IACT-docs
work_package: 2026-05-05-07-40-30-arq-tecnica-uml-rigor-pass
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Decisions Log — Domain Model UML Rigor Pass

Cada decisión D-NN va aquí. Las convenciones se derivan de
``source/base-cognitiva/_uml/uml-04-uso-relaciones/`` para
mantener coherencia con los ejemplos canónicos del proyecto.

----

## D-01 — Inventario corregido: 68 archivos canónicos (no 37)

**Contexto:** el WP predecesor habló de "37 archivos" pero
``ls source/arquitectura-tecnica/domain-model/*.rst`` (excluyendo
``index`` y ``README``) arroja **68** archivos.

**Decisión:** trabajar sobre los 68. La estimación original
era incorrecta — combinaba archivos que ya existían antes
del WP predecesor con los 41 stubs nuevos.

**Justificación:** sin esto la matriz de progreso no cierra.

----

## D-02 — Convención de multiplicidad PlantUML

**Contexto:** ``uml-04/multiplicidad.rst`` muestra
``Equipo "1" -- "5..*" Jugador : tiene``.

**Decisión:** toda relación ``--``, ``o--``, ``*--``,
``-->`` lleva multiplicidad en **comillas dobles** en cada
extremo. El orden de los extremos respeta la dirección
semántica (clase fuente a la izquierda).

**Sintaxis canónica:**

.. code-block:: text

   ServiceA "1" *-- "1" KPICalculator : composes
   ServiceA "1" o-- "0..*" StatRepo : reads

**Multiplicidades del catálogo:**

- ``"1"`` — exactamente uno (composición típica).
- ``"0..1"`` — opcional (cache miss permitido).
- ``"*"`` o ``"0..*"`` — muchos (colecciones).
- ``"1..*"`` — uno o más (no-vacío garantizado).

----

## D-03 — Roles en extremos de asociación

**Contexto:** ``uml-04/asociaciones-reflexivas.rst`` usa
``"1\nconductor"`` y ``"0..*\npasajero"`` para roles.

**Decisión:** colocar el rol en el extremo cuando el
extremo tiene **valor semántico distinto del nombre de
clase**. Sintaxis: ``"<mult>\n<rol>"``. Si el rol coincide
con el nombre de la propiedad privada de la clase fuente,
usar ese nombre (ej: ``stat_repo``).

**Cuándo NO poner rol:** cuando el rol es trivial (idem
nombre clase). No saturar el diagrama.

----

## D-04 — Restricciones {ordered}, {unique}, {readOnly}

**Contexto:** ``uml-04/restricciones-en-las-asociaciones.rst``
usa ``{ordered}`` en una nota junto a la clase.

**Decisión:** aplicar restricciones en **nota inferior** a
la clase del extremo "muchos":

- ``{ordered}`` → colecciones temporales (``buckets``,
  ``daily_breakdown``, ``audit_events``, ``alert_history``).
- ``{readOnly}`` → catálogos inmutables tras seed
  (``column_catalog``, ``action`` enum-like, ``section``).
- ``{unique}`` → conjuntos sin duplicados
  (``access_group.users``).

**Sintaxis canónica:**

.. code-block:: text

   note bottom of Bucket
     {ordered}
   end note

----

## D-05 — Asociaciones calificadas

**Contexto:** ``uml-04/asociaciones-calificadas.rst``
muestra ``Recepcionista "1" -[#black]- "(numeroConfirmacion)" Reservacion``.

**Decisión:** usar la sintaxis con calificador entre
paréntesis en el extremo del que hace búsqueda. Aplicar a:

- ``PermissionCache`` resuelve por ``(user_id)``.
- ``RBACRepo`` resuelve permisos por ``(user_id, function_id)``.
- ``AssignmentRepo`` resuelve por ``(user_id, role_id)``.
- ``MenuIvrReportService.by_option`` no es calificada — es
  agrupación, distinto concepto.

**Sintaxis canónica:**

.. code-block:: text

   PermissionCache "1" -- "(user_id)" Permission : resolves

----

## D-06 — Clases de asociación

**Contexto:** ``uml-04/clases-de-asociacion.rst`` muestra
``(Jugador, Equipo) .. Contrato``.

**Decisión:** ``AccessGroupFunction`` ES una clase de
asociación entre ``AccessGroup`` y ``Function`` — es el
ejemplo más claro del modelo. Re-modelar usando la
notación oficial. Otros candidatos a revisar:

- ``Assignment`` — asociación ``User`` ↔ ``Role``.
- ``ExceptionalPermission`` — asociación ``User`` ↔
  ``Function``.
- ``Subscription`` — asociación ``User`` ↔ ``Report``.
- ``Session`` — NO es clase de asociación: tiene ciclo
  de vida propio independiente del ``User`` (puede
  expirar sin destruir al user).

**Sintaxis canónica:**

.. code-block:: text

   AccessGroup "1" -- "1..*" Function : grants
   (AccessGroup, Function) .. AccessGroupFunction

----

## D-07 — Generalización: BaseReportService abstracto

**Contexto:** los 6 servicios ``XxxReportService``
(Agent, Abandono, Clientes, MenuIvr, Transferencias,
ScheduledReportList) repiten:

- atributos: ``stat_repo``, ``kpi_calculator``,
  ``segment_resolver``
- métodos: ``get(invoker, period, filters)``,
  ``apply_segment_filter(filters, segment)``

**Decisión:** introducir clase abstracta
``BaseReportService`` con:

- atributos comunes (los 3 inyectados)
- método abstracto ``get(...)``
- método concreto ``apply_segment_filter(...)`` (template
  method — comportamiento compartido)

Cada ``XxxReportService`` extiende ``BaseReportService`` y
agrega sus métodos especializados (``by_queue``,
``retention_curve``, ``origin_destination_matrix``, etc.).

Crear archivo nuevo
``source/arquitectura-tecnica/domain-model/base-report-service.rst``.

**Justificación:**

- DRY — elimina 6×3 atributos repetidos en diagramas.
- Documenta el patrón template-method explícitamente.
- Sustituibilidad LSP: donde se espera ``BaseReportService``
  cualquier subclase encaja.

**Anti-patrón evitado:** no introducir ``BaseRepository``
porque los repos del modelo (``AgentDailyStatRepo``,
``QueueDailyStatRepo``, etc.) tienen interfaces
heterogéneas. Forzar herencia ahí sería herencia por
implementación, no por contrato. Usar el patrón a nivel
conceptual sin clase abstracta explícita.

----

## D-08 — Asociaciones reflexivas

**Contexto:** ``uml-04/asociaciones-reflexivas.rst`` usa
``"1\n<<boss>>" -- "0..*\n<<subordinate>>"``.

**Decisión:** aplicar reflexiva con roles en:

- ``Menu`` — jerarquía padre/hijo del árbol IVR. Roles:
  ``parent`` / ``children``. Multiplicidad ``"0..1"`` ↔
  ``"0..*"`` (raíz no tiene padre).
- ``NavDomain`` — jerarquía de dominios de navegación
  RBAC. Roles análogos.
- ``Function`` — ``parent_function`` / ``sub_functions``
  si existe jerarquía (verificar en spec).

**Sintaxis canónica:**

.. code-block:: text

   Menu "0..1\nparent" -- "0..*\nchildren" Menu : contains

----

## D-09 — Distinción de tipos de dependencia

**Contexto:** ``uml-04/dependencias.rst`` usa ``..>`` con
estereotipos como ``<<usa>>`` para clarificar.

**Decisión:** distinguir tres usos de ``..>``:

- ``<<returns>>`` — dependencia por valor de retorno (DTOs).
- ``<<uses>>`` — dependencia por parámetro o variable local.
- ``<<creates>>`` — dependencia por instanciación interna
  (factory).

**Sintaxis canónica:**

.. code-block:: text

   AbandonoReportService ..> AbandonReport : <<returns>>
   AuditService ..> AuditEvent : <<creates>>

----

## D-10 — Orden de aplicación por bounded context

**Decisión:** secuencia de la pasada para minimizar
re-trabajo:

1. **RBAC primero** (10 archivos) — es donde están los
   conceptos más ricos: clase de asociación
   (``AccessGroupFunction``), reflexiva (``Menu``,
   ``NavDomain``), calificada (``PermissionCache``,
   ``RBACRepo``). Validar la convención aquí.

2. **Reports** (17 archivos) — introducir
   ``BaseReportService`` y refactorizar las 6 subclases
   en cascada. Aplicar ``{ordered}`` a buckets.

3. **Audit** (9 archivos) — patrón conceptual Repository,
   ``{ordered}`` en eventos, ``<<creates>>`` en
   ``AuditService → AuditEvent``.

4. **Alerts** (5 archivos) — reflexiva si aplica en reglas
   compuestas, ``{ordered}`` en histórico.

5. **Resto** (Auth, Calls, Pipeline ETL, Logs, etc. —
   ~27 archivos) — aplicar multiplicidades y dependencias
   con estereotipo. Cambios menores.

**Justificación:** RBAC concentra los conceptos UML más
delicados; validarlos primero permite ajustar la
convención antes de aplicarla en escala.

----

## D-13 — ScheduledReportListService NO hereda BaseReportService

**Contexto:** durante la aplicación de D-07 se descubrió
que ``ScheduledReportListService`` no comparte la
estructura del resto de XxxReportService:

- No tiene ``stat_repo`` (usa ``ScheduledReportRepo``).
- No tiene ``kpi_calculator`` (no agrega métricas).
- No tiene ``segment_resolver`` (filtra por ownership,
  no por segmento CNST-008).
- Usa ``PermissionService`` para autorización.

**Decisión:** **excluir** ``ScheduledReportListService``
de la jerarquía ``BaseReportService``. Es un servicio
CRUD de metadata, no un servicio de agregación.

**Resultado:** ``BaseReportService`` tiene **5 subclases**
concretas (no 6): Agent, Abandono, Clientes, MenuIvr,
Transferencias.

**Justificación:** forzar la herencia rompería LSP — los
métodos heredados no aplicarían y se introduciría
abstracción incorrecta.

----

## Pendientes de decisión

- D-14 (futuro): si crear archivo separado para enums
  cuando un enum es reutilizado entre BCs (ej:
  ``AuditOutcome`` usado en Audit y RBAC).
- D-15 (futuro): si las asociaciones de tipo "delegation"
  de ``ServicioReportes`` deben dibujarse como
  composición (la facade es dueña de las instancias) o
  agregación (las instancias se inyectan). Inclinación
  inicial: composición.
