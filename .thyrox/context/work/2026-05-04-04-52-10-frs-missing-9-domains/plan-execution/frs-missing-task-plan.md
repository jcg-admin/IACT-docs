```yml
created_at: 2026-05-04 04:52:10
project: IACT-docs
work_package: 2026-05-04-04-52-10-frs-missing-9-domains
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Pendiente
```

# Task Plan — FRs Faltantes (9 dominios)

Derivar los Requisitos Funcionales para los 9 dominios de UCs que actualmente
no tienen ningún FR en `source/requisitos/requisitos-funcionales/`.

Protocolo obligatorio por cada FR:
1. Leer el UC origen (flujo-principal + criterios-aceptacion)
2. Identificar los comportamientos que el sistema DEBE cumplir
3. Escribir el FR con todas las 6 secciones obligatorias
4. Verificar antes de commitear

---

## Bloque A — Dominio: permissions (FR-012..021)

- [x] **T-001** Crear directorio `requisitos-funcionales/permissions/`
- [x] **T-002** Derivar FRs de `uc-perm-01` (Asignar Grupo a Usuario) → FR-012.01..04
- [x] **T-003** Derivar FRs de `uc-perm-02` (Revocar Grupo de Usuario) → FR-013.01..02
- [x] **T-004** Derivar FRs de `uc-perm-03` (Conceder Permiso Excepcional) → FR-014.01..02
- [x] **T-005** Derivar FRs de `uc-perm-04` (Revocar Permiso Excepcional) → FR-015.01..02
- [x] **T-006** Derivar FRs de `uc-perm-05` (Crear Grupo de Permisos) → FR-016.01..03
- [x] **T-007** Derivar FRs de `uc-perm-06` (Asignar Funciones a Grupo) → FR-017.01..02
- [x] **T-008** Derivar FRs de `uc-perm-07` (Verificar Permiso Usuario) → FR-018.01..02
- [x] **T-009** Derivar FRs de `uc-perm-08` (Generar Menu Dinamico) → FR-019.01..02
- [x] **T-010** Derivar FRs de `uc-perm-09` (Auditar Acceso) → FR-020.01..02
- [x] **T-011** Derivar FRs de `uc-perm-10` (Consultar Auditoria Permisos) → FR-021.01
- [x] **T-012** Commit: "Derive FRs for permissions domain (FR-012..021)"

---

## Bloque B — Dominio: operator (FR-022..031)

- [ ] **T-013** Crear directorio + derivar FRs de uc-opr-01..10
- [ ] **T-014** Commit: "Derive FRs for operator domain (FR-022..031)"

---

## Bloque C — Dominio: reports (FR-032..049)

- [x] **T-015** Crear directorio + derivar FRs de uc-rpt-01..17 + uc-inc-rpt-01
- [x] **T-016** Commit: "Derive FRs for reports domain (FR-032..049)"

---

## Bloque D — Dominio: alerts (FR-050..054)

- [x] **T-017** Crear directorio + derivar FRs de uc-alr-01..05
- [x] **T-018** Commit: "Derive FRs for alerts domain (FR-050..054)"

---

## Bloque E — Dominio: audit (FR-055..058)

- [x] **T-019** Crear directorio + derivar FRs de uc-aud-01..04
- [x] **T-020** Commit: "Derive FRs for audit domain (FR-055..058)"

---

## Bloque F — Dominio: logs (FR-059..065)

- [x] **T-021** Crear directorio + derivar FRs de uc-log-01..07
- [x] **T-022** Commit: "Derive FRs for logs domain (FR-059..065)"

---

## Bloque G — Dominio: caller (FR-066..070)

- [x] **T-023** Crear directorio + derivar FRs de uc-cli-01..05
- [x] **T-024** Commit: "Derive FRs for caller domain (FR-066..070)"

---

## Bloque H — Dominio: pipeline (FR-071..074)

- [x] **T-025** Crear directorio + derivar FRs de uc-pip-01..04
- [x] **T-026** Commit: "Derive FRs for pipeline domain (FR-071..074)"

---

## Bloque I — Dominio: supervision (FR-075..077)

- [x] **T-027** Crear directorio + derivar FRs de uc-sup-01..03
- [x] **T-028** Commit: "Derive FRs for supervision domain (FR-075..077)"

---

## Bloque J — Índices y trazabilidad

- [x] **T-029** Actualizar `requisitos-funcionales/index.rst` con los 9 dominios nuevos
- [ ] **T-030** Verificar trazabilidad UC ↔ FR en cada dominio
- [ ] **T-031** Commit final: "Update FR indexes and traceability"

---

## Orden de ejecución

```
A → B → C → D → E → F → G → H → I → J
```

Cada bloque = 1-2 commits. Push al final de cada bloque.

## Nota sobre volumen

~264 FRs nuevos estimados. Trabajo por bloques de 10-20 FRs.
Este WP es el más extenso — puede tomar múltiples sesiones.
