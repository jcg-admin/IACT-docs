```yml
created_at: 2026-05-08 00:15:00
project: IACT-docs
work_package: 2026-05-07-23-30-26-use-case-view-users-alignment
phase: Phase 1 — DISCOVER (extended)
author: NestorMonroy
status: Aprobado
version: 1.0.0
type: Approach Decision
```

# Decision de approach para placeholders Reservado

## Contexto

Tras reanudar el WP `users-alignment` post-cierre del WP
`std-010-compliance`, hay informacion adicional que afecta
la implementacion de la Opcion A original.

## Hallazgos del audit profundo posterior

### Hallazgo 1 — Patron observado en use-case-view Reservados

Los 13 archivos `:estado: Reservado` existentes en
use-case-view (10 operator + 3 supervision, ahora `Fuera del
scope` post-WP std-010) tenian estructura COMPLETA:

- Metadata `:estado: Reservado`.
- Descripcion ~3-5 lineas.
- Bloque `.. uml::` con diagrama plantuml completo (actores,
  use cases, includes/extends, notas).
- `.. seealso::` con cross-refs.

Ejemplo: `operator/uc-opr-01-cambiar-estado-del-agente.rst`
tiene 79 lineas con diagrama de 35 lineas plantuml.

### Hallazgo 2 — Estado de spec en casos-uso

Los 3 stubs (uc-usr-05/06/07) en casos-uso son **muy
diferentes** a los Reservados de operator/supervision:

| Aspecto | operator/* Reservado (pre-WP) | users/uc-usr-{05,06,07} stubs |
|---|---|---|
| Origen | spec conocida, RBAC catalogado | "incierto — referenciado sin decision arquitectonica formal" |
| Capability | confirmada (`manage_own_agent_state`) | propuesta (no existe en catalogo) |
| AGR | catalogado | no catalogado |
| Spec textual | completa | "Decision pendiente — ADR requerido" |
| Flujo | conocido | "Resumen propuesto" hipotetico |

### Hallazgo 3 — Honestidad epistemica vs paridad estructural

Generar un diagrama plantuml para los 3 placeholders requiere
**inventar** actores, use-cases, includes/extends que NO
estan confirmados arquitectonicamente. Esto seria realismo
performativo (similar al patron prohibido en CLAUDE.md
sobre formulas no calibradas).

Crear un diagrama hipotetico podria:

- Inducir error si se interpreta como spec.
- Generar deuda tecnica si el ADR posterior contradice el
  diagrama inventado.
- Romper la trazabilidad (origen del flujo en el diagrama
  ≠ origen de la spec real).

## Re-evaluacion de Opciones (post-hallazgos)

### Opcion A1 — Placeholder minimo (RECOMENDADA)

Estructura del archivo:

```rst
.. meta::
 :artefacto: AT_UC_USR_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: users
 :estado: Reservado
 :version: 0.1.0  # mismo que el stub en casos-uso
 :origen: incierto — sin decision arquitectonica formal

.. _at_uc_usr_05_bloquear_usuario:

==============================================
UC_USR_05 — Bloquear Usuario (RESERVADO)
==============================================

.. warning::

   **UC en estado Reservado — sin diagrama hasta ADR formal.**

   Spec textual stub en
   :doc:`/requisitos/casos-uso/users/uc-usr-05/index`.
   Origen incierto: el UC esta referenciado en uc-auth-03/04/05
   pero nunca tuvo commit de creacion. La decision arquitectonica
   sobre scope, capability RBAC y relacion con BR-015 esta
   pendiente.

   El diagrama uml-07 standalone se generara cuando el ADR
   formalice el scope del UC.

.. seealso::

 - :doc:`/requisitos/casos-uso/users/uc-usr-05/index` —
   stub con resumen propuesto + decision pendiente.
 - :doc:`/requisitos/casos-uso/users/index` —
   seccion "UCs Reservados".
```

**Pro:**

- Honesto: refleja el estado epistemico real del UC.
- Paridad estructural: 1 archivo .rst en use-case-view por
  cada UC en casos-uso.
- Cumple STD-010 desde la creacion.
- Bajo coste de mantenimiento (cuando llegue el ADR, se
  reemplaza el archivo con el diagrama).

**Con:**

- Rompe el patron de "use-case-view siempre tiene diagrama".
  Pero ese patron aplicaba cuando el UC tenia spec conocida;
  estos UCs **no la tienen**.

### Opcion A2 — Placeholder con diagrama hipotetico

Generar diagrama plantuml usando "Resumen propuesto" del
stub + capability propuesta + entidades domain-model.

**Pro:**

- Consistencia estructural con operator/supervision
  Reservados (que tienen diagramas).

**Con:**

- Realismo performativo: el diagrama representaria un flujo
  hipotetico como si fuera spec.
- Riesgo de propagar la inferencia hipotetica.
- Si el ADR contradice el diagrama, hay deuda.

### Recomendacion

**Opcion A1** — placeholder minimo con warning explicito.

Razones:

1. Honestidad epistemica > paridad estructural cosmetica.
2. La paridad estructural (1 archivo por UC) se mantiene.
3. STD-010 se respeta desde la creacion.
4. Reduce deuda tecnica futura.

## Tambien actualizar `users/index.rst`

Agregar seccion "UCs Reservados" siguiendo el patron de
`casos-uso/users/index.rst`:

```rst
UCs Reservados (planificados, sin spec completa)
=================================================

Los siguientes UCs estan declarados como **Reservado** —
referenciados en otros UCs pero sin decision arquitectonica
formal. Diagramas uml-07 se generaran cuando los ADRs
formalicen el scope.

.. toctree::
 :maxdepth: 1

 uc-usr-05-bloquear-usuario
 uc-usr-06-desbloquear-usuario
 uc-usr-07-editar-perfil-propio
```

## Total cambios

- 3 archivos nuevos (placeholders mínimos).
- 1 archivo modificado (users/index.rst).
- Total commits: 4.

## Refs

- WP `std-012-prefix-normalization` (origen del estado
  reclasificado en otros clusters).
- WP `2026-05-07-04-08-13-use-case-view-analysis` (origen
  de la deteccion de los stubs Reservado en users).
- STD-010 v1.0.0 (vocabulario abstracto).
- STD-011 v1.0.0 (aliases auto-documentados — no aplica
  porque no hay diagrama).
- CLAUDE.md "restricciones de formulas probabilisticas"
  (principio anti-realismo performativo aplicable por
  analogia).
