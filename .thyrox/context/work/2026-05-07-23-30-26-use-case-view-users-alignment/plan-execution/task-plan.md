```yml
created_at: 2026-05-08 00:20:00
project: IACT-docs
work_package: 2026-05-07-23-30-26-use-case-view-users-alignment
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Aprobado
version: 1.0.0
type: Task Plan
```

# Task Plan — users-alignment (Opcion A1)

> 4 tareas atomicas + 2 TR.

## Decision arquitectonica

**Approach: A1 (placeholder minimo).** Decidida tras audit
profundo (`discover/approach-decision.md`). Honestidad
epistemica > paridad cosmetica.

## Bloque EXECUTE (4 tareas)

- [ ] **T-001** — Crear
  `source/arquitectura-tecnica/use-case-view/users/uc-usr-05-bloquear-usuario.rst`
  (placeholder Reservado).
- [ ] **T-002** — Crear
  `source/arquitectura-tecnica/use-case-view/users/uc-usr-06-desbloquear-usuario.rst`
  (placeholder Reservado).
- [ ] **T-003** — Crear
  `source/arquitectura-tecnica/use-case-view/users/uc-usr-07-editar-perfil-propio.rst`
  (placeholder Reservado).
- [ ] **T-004** — Actualizar
  `source/arquitectura-tecnica/use-case-view/users/index.rst`
  con seccion "UCs Reservados" + toctree de los 3
  placeholders.

## Bloque TRACK (2 tareas)

- [ ] **TR-01** — changelog + cierre WP.
- [ ] **TR-02** — (deferido) build clean serial al final de
  toda la cola de WPs (post este).

## Reglas de creacion (placeholders)

1. Estructura minima: meta + anchor + titulo + warning +
   seealso. **Sin** bloque `.. uml::`.
2. Metadata:
   - `:artefacto: AT_UC_USR_NN_USECASE`.
   - `:tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone`.
   - `:modulo: users`.
   - `:estado: Reservado`.
   - `:version: 0.1.0` (consistente con el stub).
   - `:origen:` con descripcion del problema epistemico.
3. STD-010 desde la creacion: NO usar terminos tecnicos
   prohibidos.
4. Cross-refs `:doc:` al stub en casos-uso obligatorios.

## Convenciones de commit

- T-NNN: `Add UC_USR_NN reserved placeholder in use-case-view`
- T-004: `Update users/index toctree with reserved UCs section`
- TR-01: `Close WP users-alignment (TR)`
