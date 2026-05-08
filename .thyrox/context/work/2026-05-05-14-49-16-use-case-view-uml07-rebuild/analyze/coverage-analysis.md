```yml
created_at: 2026-05-05 15:00:00
project: IACT-docs
work_package: 2026-05-05-14-49-16-use-case-view-uml07-rebuild
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Análisis de cobertura — UCs ↔ domain-model + uml-06

Resuelve las 5 preguntas del ejecutor antes de la
generación masiva.

## Q1 — ¿Cuáles son los 83 UCs? ¿Cómo se llamarán?

Lista completa en ``analyze/uc-list-full.md`` (con
target file por UC). Resumen distribución por módulo:

| Módulo | UCs | Naming pattern |
|--------|-----|----------------|
| auth | 5 | ``uc-auth-NN-<slug>.rst`` |
| users | 4 | ``uc-usr-NN-<slug>.rst`` |
| access | 7 | ``uc-acc-NN-<slug>.rst`` |
| permissions | 10 | ``uc-perm-NN-<slug>.rst`` |
| reports | 16 | ``uc-rpt-NN-<slug>.rst`` (más uc-inc-rpt-01) |
| alerts | 5 | ``uc-alr-NN-<slug>.rst`` |
| pipeline | 4 | ``uc-pip-NN-<slug>.rst`` |
| audit | 4 | ``uc-aud-NN-<slug>.rst`` |
| logs | 7 | ``uc-log-NN-<slug>.rst`` |
| operator | 10 | ``uc-opr-NN-<slug>.rst`` |
| supervision | 3 | ``uc-sup-NN-<slug>.rst`` |
| caller | 5 | ``uc-cli-NN-<slug>.rst`` |
| admin | 3 | ``uc-adm-NN-<slug>.rst`` |
| **TOTAL** | **83** | |

Ejemplos de slugs descriptivos:

```
uc-auth-01-iniciar-sesion.rst
uc-acc-01-asignar-funciones.rst
uc-rpt-04-exportar-reporte.rst
uc-aud-04-generar-reporte-de-compliance.rst
uc-cli-04-solicitar-callback.rst
uc-opr-05-transferir-llamada.rst
```

## Q2 — ¿Los diagramas usarán domain-model?

**Sí, vía `:doc:` cross-references** (no vía elementos
`class` dentro de `@startuml` — eso violaría R-12 uml-07).

Cada archivo per-UC tendrá la sección:

```rst
Implementación en domain-model
==============================

- :doc:`/arquitectura-tecnica/domain-model/<class-X>` — rol en este UC.
- :doc:`/arquitectura-tecnica/domain-model/<class-Y>` — rol en este UC.
```

**Mapeo agregado actual** (39 de 67 clases canónicas
referenciadas a través de los 83 UCs en sus specs
existentes en casos-uso):

Las clases más referenciadas:

- ``PermissionService``, ``AuditEvent``, ``AssignmentRepo``,
  ``RbacRepo``, ``Function``, ``FunctionGroup``,
  ``AuditService``, ``Session``, ``User``,
  ``ExceptionalPermissionRepo``, ``Assignment``,
  ``SeparationRule``, ``PermissionCache``,
  ``AccessGroup``, ``Action``.

## Q3 — ¿Qué pasa si faltan clases en domain-model?

**Sí faltan clases.** Análisis del cruce entre referencias
de UCs y catálogo domain-model:

### Clases REALMENTE faltantes (top 20 por uso)

| Clase referenciada | UCs que la usan | ¿Qué es? | Veredicto |
|--------------------|-----------------|----------|-----------|
| ``AuthorizationGuard`` | 53 | Componente de autorización HTTP | **CREAR** |
| ``AuditLog`` | 18 | Tabla/concepto append-only | Alias de ``AuditEvent`` table |
| ``AuditEmitter`` | 16 | Emisor de auditoría | Alias de ``AuditService`` |
| ``AuthenticationGuard`` | 16 | Guard middleware HTTP | **CREAR** |
| ``ThrottlePolicy`` | 16 | Rate limiting | **CREAR** |
| ``TransactionManager`` | 16 | Gestor transaccional DB | **CREAR** |
| ``ValidationError`` | 16 | Excepción genérica | Tipo común (no entity) |
| ``InternalMessage`` | 14 | Mensaje del mailbox | **CREAR** |
| ``UserRepository`` | 11 | Repo de User | **CREAR** (UserRepo) |
| ``MetricsCache`` | 11 | Cache de métricas tiempo real | **CREAR** |
| ``AccessService`` | 10 | Servicio aplicación access | **CREAR** |
| ``RequestContext`` | 10 | Contexto HTTP | DTO/value object |
| ``MailboxService`` | 9 | Servicio mailbox | **CREAR** |
| ``AnalyticsRepo`` | 9 | Repo de stats | Posible merge con ``AgentDailyStatRepo`` |
| ``AntiSelfActionPolicy`` | 8 | Policy contra auto-ataque | **CREAR** |
| ``BlacklistedToken`` | 7 | Token revocado JWT | **CREAR** |
| ``CallSession`` | 7 | Sesión de llamada activa | **CREAR** (distinto de Session) |
| ``TelephonyClient`` | 7 | Cliente PBX externo | **CREAR** |

### Clases que existen pero con nombre variante (7)

Variants detectados que se mapean a canónicos:

| Referencia | → | Canónico |
|------------|---|----------|
| ``AuditEvents`` (plural) | → | ``AuditEvent`` |
| ``AssignmentRepository`` | → | ``AssignmentRepo`` |
| ``AuditSvc`` (abbrev) | → | ``AuditService`` |
| ``ExceptionalPermissionRepository`` | → | ``ExceptionalPermissionRepo`` |
| ``ExceptionalPermissions`` (plural) | → | ``ExceptionalPermission`` |
| ``AccessGroups`` (plural) | → | ``AccessGroup`` |
| ``FunctionGroups`` (plural) | → | ``FunctionGroup`` |

**Plan de remediación:**

- **Para los aliases (variants):** normalizar al
  nombre canónico durante la generación de los
  diagramas use-case-view (sin tocar domain-model).
- **Para las clases REALMENTE faltantes (top 18):**
  registrar como hallazgo para WP futuro
  ``domain-model-completion-pass`` que cree los
  ~18 archivos canónicos faltantes. NO bloquea
  este WP — los diagramas use-case-view pueden
  referirse a las clases faltantes vía nota
  ("``AuthorizationGuard`` — pendiente, ver WP
  domain-model-completion") y crear los archivos
  cuando exista la clase.

## Q4 — ¿Las clases existentes requieren más atributos / firmas?

**Análisis spot-check** sobre las 39 clases canónicas
usadas. Los UCs en sus ``flujo-principal`` y
``implementacion-tecnica`` mencionan operaciones
específicas que algunas clases canónicas NO documentan.

### Clases con métodos faltantes detectados

| Clase canónica | Métodos referenciados en UCs pero NO documentados |
|----------------|----------------------------------------------------|
| ``PermissionService`` | ``check_bulk_with_cache``, ``warm_user_cache``, ``invalidate_for_function`` |
| ``AssignmentRepo`` | ``find_by_function_id``, ``count_active_globally``, ``find_expiring_in_window`` |
| ``AuditService`` | ``emit_async``, ``flush_pending``, ``correlate_events`` |
| ``RbacRepo`` | ``get_assignments_changed_since``, ``snapshot_effective_set`` |
| ``Session`` | ``rotate_token``, ``mark_compromised``, ``link_to_call`` |
| ``User`` | ``record_login_attempt``, ``increment_failed_attempts``, ``check_password_age`` |
| ``AlertRule`` | ``evaluate_against_metric``, ``simulate_dry_run`` |
| ``ScheduledReport`` | ``next_execution_at``, ``skip_window`` |

**Plan de remediación:**

- **NO actualizar domain-model en este WP** — alteraría
  el alcance.
- **SI**, registrar hallazgo para WP
  ``domain-model-method-augmentation-pass`` que audite
  los 39 archivos contra los métodos referenciados en
  los 83 UCs y agregue lo faltante.

## Q5 — ¿Se está aplicando uml-06 en casos-uso?

uml-06 establece (en sus 4 archivos canónicos):

- ``importancia-de-los-casos-de-uso.rst``: el UC
  responde 7 preguntas:

  1. ¿Qué condiciones llevaron al actor a iniciar?
  2. ¿Qué se obtiene como resultado?
  3. ¿Es la única posibilidad?
  4. ¿Qué pasa si el actor no cumple los requisitos?
  5. ¿Qué situaciones impiden alcanzar el propósito?
  6. ¿Qué pasa si el caso de uso falla?
  7. ¿Hay rutas alternativas o acción correctiva?

- ``inclusion-de-los-casos-de-uso.rst``: define
  inclusión textual.

- ``extension-de-los-casos-de-uso.rst``: define
  extensión textual.

- ``caso-de-uso-recolectar-el-dinero.rst``: ejemplo
  con condición previa + resultado.

### Verificación contra casos-uso/

Cada ``casos-uso/<module>/<uc>/`` tiene la estructura de
**12 archivos**:

```
informacion-general.rst       → ¿Qué hace y por qué? (Q1, Q2)
actores-precondiciones.rst    → ¿Quién y bajo qué condición? (Q1)
flujo-principal.rst           → Camino feliz (Q3)
flujos-alternos.rst           → Rutas alternativas (Q3, Q7)
excepciones.rst               → Fallos y propósito no alcanzado (Q4, Q5, Q6)
criterios-aceptacion.rst      → Cómo verificar éxito (Q2)
datos-involucrados.rst        → Qué datos
diagramas-uml/                → Diagramas (uml-07/08/09/11)
patrones-diseno.rst           → Patrones implementación
requisitos-no-funcionales.rst → NFRs
implementacion-tecnica.rst    → Cómo se implementa
testing.rst                   → Cómo se prueba
index.rst                     → Toctree
```

**Veredicto:** las 7 preguntas de uml-06 están cubiertas
en la estructura de 12 partes. ``casos-uso/`` SÍ
aplica uml-06 correctamente.

**Hallazgo menor:** algunos UCs (los 53 sin src diagram)
tienen ``flujo-principal`` y ``excepciones`` completos
pero NO el diagrama uml-07. Esto explica por qué se
necesita este WP: completar la dimensión gráfica que
uml-06 deja a uml-07.

## Resumen de las 5 respuestas

| Q | Pregunta | Respuesta |
|---|----------|-----------|
| Q1 | ¿Cuáles son los 83 UCs? | Listados en uc-list-full.md, con target filename |
| Q2 | ¿Usarán domain-model? | Sí, vía `:doc:` cross-refs (no como elementos del diagrama) |
| Q3 | ¿Faltan clases en domain-model? | Sí: ~18 clases reales faltantes + 7 naming variants. Plan: WP futuro |
| Q4 | ¿Las clases existentes están completas? | No. ~30 métodos referenciados no documentados. Plan: WP futuro |
| Q5 | ¿Se aplica uml-06? | Sí, las 12 partes de casos-uso cubren las 7 preguntas de uml-06 |

## WPs futuros derivados

1. ``domain-model-completion-pass`` — crear ~18 clases
   canónicas faltantes (AuthorizationGuard, AccessService,
   MailboxService, MetricsCache, etc.).
2. ``domain-model-method-augmentation-pass`` — agregar
   métodos faltantes a 8 clases existentes.

Estos NO bloquean el rebuild actual — los diagramas
use-case-view referenciarán las clases faltantes vía
nota ("pendiente de creación, ver WP X").
