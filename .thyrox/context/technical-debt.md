```yml
type: Registro de Deuda Técnica
project: IACT-docs
created_at: 2026-04-23 08:30:00
updated_at: 2026-05-06 20:30:00
scope: IACT-docs project only — NOT framework THYROX
```

# Deuda Técnica — IACT-docs

Registro de problemas conocidos específicos del proyecto IACT-docs que no se corrigen inmediatamente pero deben ser atendidos. Cada ítem tiene un ID, descripción, impacto, y criterio de resolución.

**Nota:** Esta lista es SOLO para IACT-docs. La deuda técnica del framework THYROX está separada.

## Convenciones

- `[ ]` = Pendiente
- `[-]` = En progreso
- `[x]` = Resuelto (YYYY-MM-DD)
- `[~]` = Aceptado / Obsoleto (con razón)
- Severidad: alta | media | baja
- Origen: security-review, calibration-analysis, Phase X DIAGNOSE, etc.

---

## TD-001: Information Disclosure via Git History — Configuración Sensible en Commits

```
Severidad: ALTA → BAJA (reclasificada 2026-05-06)
Origen: security-review (2026-04-23)
Estado: [~] Aceptado / Obsoleto (2026-05-06)
Resolución: documentada en adr-sensitive-info-policy.md
WP de cierre: 2026-05-06-20-26-07-close-all-technical-debt
```

**Estado original (2026-04-23):**

Reportaba que `PROJECT_CONFIGURATION_REVIEW.md` (commits `e5c0ff1` → `2a21dd0`) expuso en git history:

- RBAC model v5.1.1 (8 módulos, 44 funciones, 3 SoD).
- 8 restricciones del sistema (CNST_001..008).
- Información de compliance: OWASP, NIST RBAC, ISO 27001.

**Reclasificación 2026-05-06:**

El contenido en cuestión es hoy **parte legítima y pública del corpus IACT-docs**:

- RBAC v5.6.0 con 64 funciones documentadas en `source/arquitectura-tecnica/rbac/modelo-rbac-iact/`.
- 31 CNSTs documentados en `source/normativa/restricciones/`.
- BR-006 declara explícitamente cumplimiento NIST RBAC.

El "riesgo" original era exposición accidental; el estado actual es **publicación deliberada y diseñada** como documentación del proyecto. La severidad ya no es ALTA — el contenido cumple su función pública.

**Decisión:** se acepta la presencia del contenido en git history. Force-push history rewrite **NO se ejecuta** porque:

1. El contenido es hoy publicable y legítimo.
2. Force-push reescribiría historial de un repo posiblemente compartido — riesgo de regresión > beneficio.
3. La política `adr-sensitive-info-policy.md` clarifica qué SÍ es sensible (credenciales, IPs internas, PII, llaves) — distinto del contenido conceptual del modelo RBAC.

**Trabajo futuro relacionado:** TD-002 → ADR creado; TD-003 → pre-commit hook implementado.

---

## TD-002: Crear ADR-sensitive-info-policy — Política de Información Sensible en Repositorio

```
Severidad: MEDIA
Origen: TD-001 (como resultado de limpieza)
Estado: [x] Resuelto 2026-05-06
WP de cierre: 2026-05-06-20-26-07-close-all-technical-debt
```

**Resolución:**

Creado `.thyrox/context/decisions/adr-sensitive-info-policy.md` con:

1. **Qué es sensible:** credenciales activas, infraestructura interna, PII, config por instancia, llaves privadas.
2. **Qué NO es sensible (publicable):** modelo RBAC conceptual, CNSTs, ADRs, BReqs/BRs/UCs, convenciones — el corpus IACT-docs.
3. **Mecanismos de prevención:** `.gitignore`, pre-commit hook (TD-003), code review checklist, CI/CD futuro con gitleaks.
4. **Recuperación si ocurre leak:** procedimiento documentado.
5. **Alternativas consideradas:** git-crypt (descartada), repo separado (parcialmente aplicable).

---

## TD-003: Implementar Pre-commit Hooks para Detectar Información Sensible

```
Severidad: MEDIA
Origen: TD-001 + TD-002 (prevención)
Estado: [x] Resuelto 2026-05-06
WP de cierre: 2026-05-06-20-26-07-close-all-technical-debt
```

**Resolución:**

Creado `.githooks/pre-commit` que detecta:

1. Credential markers con valor: `API_KEY=`, `SECRET_KEY=`, `PASSWORD=`, `TOKEN=`, `BEARER`, `AWS_ACCESS_KEY_ID=`, `AWS_SECRET_ACCESS_KEY=`, `PRIVATE_KEY=`, `JWT_SECRET=`.
2. Filenames históricamente sensibles: `PROJECT_CONFIGURATION_REVIEW.md`, `*.env`, `*credentials*`, `*secrets*`.
3. Strings base64-like largas (60+ chars) — warning, no bloqueo.

**Falsos positivos:** keywords de exclusión (`example`, `placeholder`, `<your`, `TODO`, `XXX`, `REDACTED`, `dummy`, `fake`).

**Bypass documentado:** `git commit --no-verify` con referencia al ADR.

**Hook activo via `git config core.hooksPath .githooks` (`scripts/install-hooks.sh`).**

---

## TD-004: Documentar Estructura de Directorios para Desarrolladores

```
Severidad: BAJA
Origen: calibration-analysis (2026-04-23)
Estado: [x] Resuelto 2026-05-06
WP de cierre: 2026-05-06-20-26-07-close-all-technical-debt
```

**Resolución:**

Actualizada sección "Estructura del Repositorio" en `readme.rst` con:

- Estructura real (paths con dash, no underscore).
- Inclusión de `.thyrox/`, `.claude/`, `.githooks/`, `.github/workflows/`, `scripts/`, `tools/`.
- Cross-link a STD-007 (naming), STD-013 (REST API), normativa/procedimientos.

---

## TD-005: Validar que Todas las Extensiones Sphinx se Cargan Correctamente

```
Severidad: MEDIA
Origen: security-review / config-review (2026-04-23)
Estado: [x] Resuelto 2026-05-06 (verificado)
```

**Resolución verificada:**

- El proyecto compila con `sphinx-build -W` (warnings as errors) sin warnings.
- Verificado en CI (`.github/workflows/validate.yml`) con strict build en cada PR.
- Verificado localmente en sesiones recientes (~31 builds OK durante refactor masivo 2026-05-06).
- `sphinxcontrib.spelling` está en `extensions` y carga; `spelling_wordlist.txt` es opcional para uso de spell-check; sin él, la extensión no falla.

---

## TD-006: Crear CI/CD Pipeline para Validación Automática de Builds

```
Severidad: ALTA
Origen: config-review (2026-04-23)
Estado: [x] Resuelto (preexistente, verificado 2026-05-06)
```

**Resolución verificada:**

`.github/workflows/validate.yml` existe y ejecuta en cada `push` a feature branches y `pull_request` a `develop`/`main`:

1. `make clean && sphinx-build -W -j auto -b html -d build/doctrees source build/html` — strict build.
2. `bash scripts/validate-plantuml.sh` — validación PlantUML.
3. Upload artifact `docs-html-{PR}` con preview HTML.

**Adicionalmente:** `release.yml`, `dependabot-auto-merge.yml` están configurados.

---

## TD-007: Crear Plan de Remediación para Phase 3 DIAGNOSE

```
Severidad: ALTA → OBSOLETO (2026-05-06)
Origen: Phase 1 DISCOVER inicial (2026-04-23)
Estado: [~] Obsoleto 2026-05-06
```

**Reclasificación:**

TD-007 era meta-task del WP DISCOVER inicial (2026-04-23) que dependía de TD-001..006. Con TD-001..006 ya cerrados (Resueltos / Aceptados), el plan de remediación que demandaba ya no es necesario:

- TD-001 → Aceptado (contenido es público y legítimo).
- TD-002 → Resuelto (ADR creado).
- TD-003 → Resuelto (pre-commit hook).
- TD-004 → Resuelto (readme.rst actualizado).
- TD-005 → Verificado Resuelto (strict build OK).
- TD-006 → Verificado Resuelto (CI/CD existente).

El proyecto avanzó significativamente desde el DISCOVER inicial: 7+ WPs ejecutados (rbac-v5-6-0, uc-opr-sup-reserved, mapeo-uc, corpus-tech-debt, AGR-research, RBAC-bootstrap-ADR, este WP). Phase 3 DIAGNOSE en su forma original ya no es la fase activa.

---

**Total TDs:** 7 (IACT-docs specific)
**Pendientes:** 0 · **En progreso:** 0 · **Resueltos:** 5 · **Aceptados/Obsoletos:** 2
**Ubicación:** `.thyrox/context/technical-debt.md`
**Alcance:** Solo IACT-docs project

**Estado del WP:** todas las TDs cerradas el 2026-05-06 en el WP
`2026-05-06-20-26-07-close-all-technical-debt`. No hay deuda técnica pendiente al cierre de esta actualización.

---

## TD-RBAC-03: `manage_critical_function_flag` sin titular runtime

```
Severidad: media
Origen: ADR-BACK-010 §3.6 (2026-05-07)
Estado: [ ] Pendiente
WP de origen: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
```

**Descripción:**

La capability ``manage_critical_function_flag`` se declara en
el catálogo RBAC v5.6.x como activa (``is_active=True``,
``is_critical=True``) **sin AGR titular**. Cambios al campo
``Function.is_critical`` solo se aplican via Django RunPython
data migration con review obligatoria ≥ 2 aprobaciones —
**no hay vía runtime para modificar el flag**.

**Justificación de la postergación:**

ADR-BACK-010 §3.4 documenta el vector de ataque que la
governance separada mitiga: si la capability fuera asignable a
un AGR comun, un atacante con acceso a `manage_function_catalog`
comprometido podria marcar su propia capability como
``is_critical=False`` antes de ser revocado, anulando la
proteccion AP-2b.

**Trigger de revisión:**

- Si el equipo operativo requiere modificar `is_critical` con
  frecuencia mayor a 1 vez por release.
- Si surge una operación de seguridad que requiere bloquear /
  desbloquear capabilities en runtime.
- Si se aprueba la asignación a un slot reservado (AGR-013) o
  hardcoded a un superuser específico.

**Resolución requerida:**

ADR explícito que apruebe (a) asignación a un AGR especial
(consume slot reservado AGR-011/012 o crea AGR-013), o (b)
mecanismo alternativo (e.g., feature flag con gate doble).

**Refs:**
- ``source/backend/adr-back-010-function-is-critical-governance.rst``
- ``source/requisitos/reglas-negocio/rbac/catalogo-funciones.rst`` §3.11
