```yml
created_at: 2026-05-04 02:45:00
project: IACT-docs
work_package: 2026-05-04-01-51-32-kruchten-view-diagram-types
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En progreso
```

# Task Plan — Correcciones Restantes

Tareas pendientes identificadas en `remaining-corrections-assessment.md`.
Ejecución autónoma — no requiere aprobación por tarea.

---

## Bloque A — Quick wins (build errors + warnings)

- [x] **T-001** Fix `uc-perm-05/excepciones.rst` — title underline corto en §5.2
  - Underline de 35 → 36 caracteres
  - DONE en commit anterior

- [x] **T-002** Fix `vis-reports/diagramas.rst` — PlantUML `:action; stop` en misma línea
  - Separar en `:action;\n  stop` en 4 ocurrencias
  - DONE en commit anterior

- [ ] **T-003** Fix `diagramas-uml-sistema.rst` — PlantUML errors en §3 (line 3) y §8 (line 48)
  - §3: Leer línea 3 del bloque plantuml del Use Case diagram y corregir
  - §8: El fragmento `neg` en el Sequence diagram puede no ser válido — revisar y reemplazar con `else` en `alt`
  - Commit atómico: "Fix PlantUML syntax errors in diagramas-uml-sistema.rst"

---

## Bloque B — Normativa y estándares

- [x] **T-004** Crear `std-010-vocabulario-abstracto.rst`
  - Tabla de vocabulario canónico (MySQL→repositorio, bcrypt→hash seguro, etc.)
  - Reglas de diagramas UML en narrativa
  - DONE en commit anterior

- [x] **T-005** Agregar STD_010 al toctree de `normativa/estandares/index.rst`
  - DONE en commit anterior

---

## Bloque C — Narrative violations remanentes

- [ ] **T-006** Fix `uc-auth-01/diagramas-uml.rst` — participante `"LoginView\n(Django)"`
  - Reemplazar con `"Servicio de Autenticacion"`
  - Commit: "Fix tech participant names in uc-auth-01 diagramas-uml"

- [ ] **T-007** Fix `uc-aud-03/diagramas-uml.rst` — database `"audit_log\n(PostgreSQL)"`
  - Reemplazar con `"Repositorio de Auditoria"`
  - Commit: "Fix tech participant name in uc-aud-03 diagramas-uml"

- [ ] **T-008** Fix `uc-log-02/diagramas-uml.rst` — `"MariaDB"` en diagrama
  - Reemplazar con `"Almacen de Datos"`
  - Commit: "Fix tech node name in uc-log-02 diagramas-uml"

- [ ] **T-009** Sweep completo de violaciones remanentes en `casos-uso/**/diagramas-uml.rst`
  - Buscar y corregir cualquier `"Frontend\n(React)"`, `"Django"`, `"MySQL"` restante
  - Commit: "Sweep remaining tech names in UC diagramas-uml files"

---

## Bloque D — Adaptación diagramas-uml-sistema.rst §7–§11

- [ ] **T-010** Adaptar §7 State Machine a dominio IACT
  - El diagrama actual ya es IACT (ciclo de vida de sesión IACT)
  - Verificar que no haya nombres tecnológicos incorrectos

- [ ] **T-011** Adaptar §8 Sequence diagram — revisar fragmento `neg`
  - `neg [ETL fallido]` puede ser inválido en versión PlantUML instalada
  - Reemplazar `neg` con `else` dentro de `alt` si causa error

- [ ] **T-012** Verificar §9 Communication diagram — sintaxis de `object`
  - El diagrama actual usa `: User (RBAC group)` — verificar sintaxis
  - Corregir si causa error

- [ ] **T-013** Verificar §10 Component y §11 Deployment
  - Confirmar que los stereotypes son válidos
  - Corregir si hay errores

---

## Bloque E — Validación final

- [ ] **T-014** Ejecutar `make html SPHINXOPTS="-j1"` y capturar warnings
  - Verificar 0 errores PlantUML
  - Verificar 0 warnings RST "title underline too short"
  - Commit WP changelog con resultado

- [ ] **T-015** Actualizar `now.md` con estado final del WP
  - Registrar qué quedó pendiente vs completado

---

## Orden de ejecución

```
A (T-003) → B (ya done) → C (T-006..T-009) → D (T-010..T-013) → E (T-014..T-015)
```

Cada tarea = 1 commit. Push después de cada bloque completo.
