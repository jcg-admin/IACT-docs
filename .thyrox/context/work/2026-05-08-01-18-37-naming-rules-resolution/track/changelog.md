```yml
created_at: 2026-05-08 02:00:00
project: IACT-docs
work_package: 2026-05-08-01-18-37-naming-rules-resolution
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — naming-rules-resolution (4 decisiones)

## [1.0.0] — 2026-05-08

### Changed (D1) — `backend/conventions.rst` v1.0.0 → v2.0.0

**BREAKING normative change.**

- Declarada `CLEAN_CODE_NAMING_PRINCIPLES` como autoridad
  normativa (cross-ref agregada).
- Reemplazada prescripcion de sufijos DRF (`Serializer`,
  `ViewSet`, `View`, `Permission`) por **tabla de sufijos
  prohibidos** con reemplazos canonicos del dominio.
- Agregada seccion "Convivencia con la herencia del
  framework" con ejemplos de codigo donde el nombre de
  clase es de dominio y la base class DRF es detalle de
  implementacion.
- Naming guidance de archivos: nombre de la **clase** es
  critico, no el del archivo.

### Changed (D2 + D4) — `STD-010` v1.0.0 → v1.1.0

**MINOR — amplia sin contradecir.**

D2 (scope clarification):

- §2.1 tabla expandida (4 entradas adicionales: reglas-negocio,
  base-cognitiva, index.rst raiz por contenido, backend
  exempt, _metodologia-aplicacion exenta).
- §2.2 nueva: `index.rst` raiz aplica por contenido (no por
  nombre).
- §2.3 nueva: `_metodologia-aplicacion/` exenta formalmente
  (documentacion de proceso, no especificacion).
- §2.4 nueva: sistemas externos del cliente exentos por
  nombre propio + criterio "comportamiento IACT vs hechos
  arquitectonicos del entorno".

D4 (RBAC + opacos):

- §5.4 nueva: RBAC declarado vocabulario disciplinar
  aceptado en prosa explicativa, con criterio explicito
  donde APLICA y donde NO APLICA.
- §5.5 nueva: identificadores opacos con dependencias
  externas (tokens RBAC backend `access:*_sod` + codigos
  BD `SOD-NNN`, `AGR-NNN`).

### Renamed (D3) — `ResumenSaludBuilder` → `ResumenSaludAssembler`

- Verificacion del UML: la clase tiene UN solo metodo
  publico (`build`), sin interfaz fluent encadenable.
- Por tanto, el sufijo `Builder` viola CLEAN_CODE §1.2
  (implica interfaz fluent inexistente).
- `git mv resumen-salud-builder.rst resumen-salud-assembler.rst`.
- Title, anchor, artefacto identifier renombrados.
- Descripcion actualizada con explicacion del patron
  Assembler vs Builder GoF.
- Nota historica documentando el rename para trazabilidad.
- 24 cross-refs externos actualizados en:
  - `domain-model/index.rst` (toctree).
  - `domain-model/resumen-salud.rst` (2 refs).
  - `domain-model/supervision-etl-service.rst` (5 refs +
    1 `:doc:`).
  - `casos-uso/pipeline/uc-pip-01/implementacion-tecnica.rst`
    (3 refs).
  - `casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-actividad.rst`
    (1 `:doc:`).
  - `casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-clases.rst`
    (3 refs).

### Verification

```bash
# D1: backend/conventions.rst v2.0.0 ✅
grep -E "version: 2.0.0" source/backend/conventions.rst

# D2 + D4: STD-010 v1.1.0 con §2.1-2.4 + §5.4-5.5 ✅
grep -E "version: 1.1.0" source/normativa/estandares/std-010-vocabulario-abstracto.rst

# D3: ResumenSaludBuilder removido excepto nota historica ✅
grep -rn "ResumenSaludBuilder\|resumen-salud-builder" source/
# (1 hit esperado: nota en el propio archivo nuevo)
```

## Efectos sobre el roadmap futuro (clean-code-naming)

| WP futuro | Estado |
|---|---|
| WP-D (ADR conflicto conventions) | ✅ Resuelto en este WP |
| WP-E (Factory/Builder/Manager) | Criterio claro; 1 caso resuelto (ResumenSalud); 6 Builder restantes pendientes |
| WP-F (Serializer/ViewSet/View) | Desbloqueado por D1 |
| WP-G (STD-010 cleanup) | Scope reducido ~40% por D2; criterio claro por D4 |

## Commits del WP (5 commits)

1. WP setup.
2. D1 — backend/conventions v2.0.0.
3. D2 + D4 — STD-010 v1.1.0.
4. D3 — ResumenSalud rename.
5. (este commit) — TR cierre + decisions-log.

## Refs

- WP `clean-code-naming-audit` (predecesor, audit-only).
- `discover/decisions-log.md` (artefacto principal del WP).
- `CLEAN_CODE_NAMING_PRINCIPLES` v1.0.0.
- `STD-010` v1.1.0 (bumpeado aqui).
- `backend/conventions.rst` v2.0.0 (bumpeado aqui).
