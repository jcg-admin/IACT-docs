```yml
created_at: 2026-05-06 23:35:00
project: IACT-docs
work_package: 2026-05-06-23-25-08-std-010-corpus-compliance
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Changelog — STD-010 Corpus Compliance

## Changed

- ``source/requisitos/casos-uso/auth/uc-auth-02/criterios-aceptacion.rst``:
  CA-09 — sustituida ``Redux state.auth.isAuthenticated == false`` por
  ``Gestor de Estado refleja sesion no autenticada
  (state.auth.isAuthenticated == false)`` (H-1, STD-010 §3.4).
- ``source/requisitos/casos-uso/auth/uc-auth-02/flujo-principal.rst``:
  PASO 10 — sustituido "limpia state de Redux" por "limpia state del
  Gestor de Estado" (H-2, STD-010 §3.4).
- ``source/requisitos/casos-uso/auth/uc-auth-02/diagramas-uml/diagrama-de-secuencia.rst``:
  participante self-message — sustituido ``localStorage.clear\nRedux
  clear`` por "limpia almacenamiento local\nlimpia Gestor de Estado"
  (H-3, STD-010 §3.4 + §4).
- ``source/requisitos/casos-uso/users/uc-usr-01/flujos-alternos.rst``:
  PASO 10A — sustituido ``IntegrityError`` por "error de integridad
  de datos" (H-4, STD-010 §3.2).
- ``source/requisitos/casos-uso/reports/uc-inc-rpt-01/datos-involucrados.rst``:
  §7.2 — sustituido "(PostgreSQL — base operacional IACT)" por
  "(repositorio operacional IACT)" (H-5, STD-010 §3.2).
- ``source/requisitos/casos-uso/reports/uc-rpt-03/datos-involucrados.rst``:
  §7.4 — sustituido "(PostgreSQL — tablas de usuarios, RBAC)" por
  "(repositorio operacional — tablas de usuarios, RBAC)" (H-6, STD-010 §3.2).
- ``.thyrox/context/work/2026-05-06-21-42-06-menu-rbac-user-scope-docs/discover/final-decisions-p1-p4-and-pending-items.md``:
  §4 — heading "Job de monitoreo (Celery beat)" reformulado a
  "Job de monitoreo (Planificador de Tareas)" + nota STD-010 §3.5
  explicando que el motor concreto vive en ``arquitectura-tecnica/``;
  bullet de §5 actualizado análogamente (H-7).

## Added

- ``discover/std-010-corpus-audit.md``: audit principal con 9 hits
  reales clasificados en Tier 1 (clear, 6 corregidos) y Tier 2
  (testing.rst libre por interpretación, sin cambio).
- ``discover/std-010-extension-candidates.md``: inventario Tier 3 —
  términos no listados en STD-010 §3 (`localStorage` 14 hits,
  `Frontend`/`Backend` solos, gateways de pago) con recomendación de
  abrir WP separado para extender STD-010.
- ``discover/build-logs/sphinx-strict-post-fix-*.log``: build limpio
  EXIT=0 post-correcciones.

## Aceptado / no fixeado

- Hits en `testing.rst` (T-1..T-3, 5 ítems): no modificados. STD-010 §2
  no lista `testing.rst` explícitamente. Interpretación adoptada:
  libre por analogía con `implementacion-tecnica.rst` (contiene código
  pytest/jest que requiere nombres de excepción reales). Decisión
  documentada en `std-010-corpus-audit.md` §2 — ejecutor puede
  rechazar la interpretación y abrir corrección posterior.
- Hits Tier 3 (T3-1..T3-5): `localStorage` (14 hits), `Frontend`/`Backend`
  solos (~185 archivos), gateways de pago (0 hits): no corregidos —
  no están literalmente en STD-010 §3.

## Verification

- ``grep -rnE "bcrypt|\bReact\b|MySQL|...|IntegrityError" source/requisitos/casos-uso/ --include="*.rst" --exclude="implementacion-tecnica.rst" --exclude="testing.rst"`` → cero hits.
- ``make html SPHINXOPTS='-W -j auto'`` → ``build succeeded``, EXIT=0,
  sin warnings.

## Status de promoción a CHANGELOG.md raíz

Pendiente. Estos cambios NO modifican comportamiento del sistema
(solo narrativa de requisitos). Promover en el próximo merge a
``main`` con bump de versión bajo sección "Changed" como
"narrativa UC alineada con STD-010".

## Pending — siguiente WP

Retomar **WP padre** ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``
en **Phase 5 STRATEGY** produciendo
``strategy/menu-rbac-user-scope-solution-strategy.md`` con:

- Key Ideas (lifecycle managed wrapper UX, defense-in-depth,
  eventual consistency).
- Fundamental Decisions (P1-P4 confirmadas).
- Technology Stack.
- Architecture Patterns.
- Adherence to Constraints (BR-012, CNST-029, CNST-032,
  ADR-BACK-001/007).
- Traceability + evidence classification.
