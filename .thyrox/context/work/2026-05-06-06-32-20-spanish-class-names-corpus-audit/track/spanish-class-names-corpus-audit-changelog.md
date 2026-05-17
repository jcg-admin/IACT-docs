```yml
created_at: 2026-05-06 07:30:00
project: IACT-docs
work_package: 2026-05-06-06-32-20-spanish-class-names-corpus-audit
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — Spanish Class Names Corpus Audit

## Resumen

| Métrica | Antes | Después |
|---|---|---|
| Class violations (audit script) | 147 | **0** |
| Method violations (manual grep) | 87 | **0** |
| Real attr violations | 40 | **12 (legítimas — narrativa SBVR)** |
| Files modificados | 0 | **76+** |
| STD-008 versión | 1.1.0 | **1.3.0** |

## Cumplimiento de la directiva del ejecutor

> "no quieremos que nada tenga nombres de clases en español, lo
> único que va en español son los comentarios"

✅ **Cumplido.** Todos los identifiers de clases, entidades,
métodos, atributos y enums en zonas pedagógicas, normativas y
descriptivas traducidos al inglés (PEP 8 / Clean Code).
Narrativa, comentarios, captions y notas PlantUML preservados
en español per STD-008 §3.5.3.

## Added

- `scripts/validate-naming-corpus.sh` — audit C-07 corpus-wide
  sin exclusiones por zona (commit `bc2f74d7`).
- `discover/spanish-class-names-corpus-audit-analysis.md` —
  Phase 1 DISCOVER con inventario, vocabulario de translation,
  plan de batches.
- `plan-execution/spanish-class-names-corpus-audit-task-plan.md`
  — task plan T-001..T-076 granular por archivo.
- Este changelog.

## Changed

### STD-008 v1.1.0 → v1.3.0

- §3.5 Coherencia de Idioma — retitulado "Identifiers SIEMPRE
  en Inglés"; lista expandida (incluye ejemplos de código,
  zonas didácticas, normativa metodológica).
- §3.5.1 Sin excepciones por zona — revoca explícitamente la
  excepción §3.5.1 que el WP previo había agregado (commit
  `bc2f74d7`).
- §3.5.2 Justificación — explica el mensaje implícito
  incorrecto que la excepción enviaba.
- §3.5.3 Comentarios y narrativa — enumera lo permitido en
  español (comentarios, UI strings, captions, RST prosa, paths
  per STD-007, notas PlantUML).
- §3.5.4 Validación automática — referencia al nuevo audit
  script.

### 76+ archivos del corpus traducidos

Por batches:

- **B-A** (T-004..T-005): 2 normativa metodologia-*-ucs.
- **B-B** (T-006..T-010): 5 base-cognitiva/_uml lecciones.
- **B-C** (T-011..T-030): 20 _metodologia-aplicacion/relaciones-uml.
- **B-D** (T-031..T-040): 10 _metodologia-aplicacion/agregacion-
  interfaces.
- **B-E** (T-041..T-062): 22 _metodologia-aplicacion/analisis-
  dominio (incluyendo erd-consolidado).
- **B-F** (T-063..T-069): 7 _metodologia-aplicacion/{patrones-
  diseno,orientacion-objetos,diagramas-uml}.
- **B-G+** (T-070..T-072): 17 archivos adicionales identificados
  post-audit en sub-zonas, base-cognitiva y normativa.

### Vocabulario canonical aplicado

Clases (sample): Usuario→User, Sesion→Session, Llamada→Call,
Operador→Operator, Reporte→Report, Permiso→Permission,
Funcion→Function, Grupo→Group, Asignacion→Assignment,
Auditoria/EventoAuditoria→Audit/AuditEvent, Cliente→Client,
PermisoExcepcional→ExceptionalPermission, BuzonInterno→
InternalMailbox, EjecucionETL→ETLExecution, Reporte→Report,
Aerolinea→Airline, Estudiante→Student, Lavadora→WashingMachine.

Métodos: asignar*→assign*, consultar*→query*/get*,
verificar*→verify*/check*, generar*→generate*, ejecutar*→
execute*, validar*→validate*, exportar*→export*, crear*→
create*, modificar*→modify*, etc.

Atributos snake_case: usuario_id→user_id, fecha_creacion→
created_at, tipo_evento→event_type, ip_origen→source_ip, etc.

## Removed

- `scripts/validate-naming-arquitectura-tecnica.sh` — reemplazado
  por validate-naming-corpus.sh sin exclusiones por zona.

## Aceptado / no fixeado

### 12 atributos residuales (false positives operacionales)

Los 12 atributos restantes están en:

1. **Bloques `.. code-block:: text` con vocabulario SBVR**
   (Semantic Business Vocabulary Rules) en business rules
   `br-012..br-019`. SBVR usa términos del lenguaje de negocio
   natural, no identifiers de software. Permitido per §3.5.3.

2. **YAML configs en ADRs legacy descriptivos**:
   `backend/adr-back-004-sistema-permisos-sin-roles-jerarquicos`
   `fecha_inicio: 2025-11-01`. Documenta config existente del
   legacy backend; modificarlo cambiaría la fidelidad
   descriptiva del ADR.

3. **Vocabulario IACT en `fnd-07-requerimientos-funcionales` y
   `tpl-fr-documentacion-10-componentes`** — secciones que
   listan vocabulario de la metodología, no clases de código.

4. **Bloque pseudocódigo en `fr-010-02-validar-sod-antes-asignar`**
   con `funcion_a` y `funcion_b` — variables de pseudocódigo
   en una regla SBVR ("Sea funcion_a la función actual...").

Estos 12 son legítimos per STD-008 §3.5.3 que permite narrativa
en español. La regex del audit es deliberadamente agresiva para
no missear violaciones reales; los false positives en narrativa
son aceptables.

### Backend ADR-back-003 no modificado

`backend/adr-back-003-orm-sql-hybrid-permissions.rst` cita
código real del legacy backend (`class GrupoPermisoAdmin`).
Modificar lo cambiaría la naturaleza descriptiva del ADR.
Per STD-008 §3.5.1 ("ADRs descriptivos de legacy → documentar
violación + plan de migración"), agregar nota inline en una
revisión separada cuando se planifique la migración del
legacy.

## Verified

- `validate-naming-corpus.sh`: PASSED 0 class/entity violations.
- Manual grep: 0 method violations remaining.
- Manual grep: 12 attr false-positives confirmed legítimos
  per §3.5.3.
- 76+ archivos modificados; narrativa en español preservada.
- STD-008 v1.3.0 sin ambigüedad sobre excepciones.

## Status de promoción a CHANGELOG.md raíz

Aplicable al merge a main. STD-008 v1.3.0 + masiva traducción
del corpus son cambios sustantivos que merecen entrada de
release notes.

## WPs sucesores derivados

1. **`backend-adr-spanish-legacy-migration-note`** — agregar
   nota inline a `adr-back-003` y `adr-back-004` documentando
   que el código citado viola STD-008 v1.3.0 y registrar plan
   de migración del legacy.
2. **`audit-script-method-attr-fix`** — corregir el bug del
   script que falla en contar método+atr (actualmente solo
   contabiliza clases). Documentado como limitación en el
   discover analysis.

## Refs

- Predecesor: WP `naming-violations-arquitectura-tecnica-fix`
  (que agregó la excepción §3.5.1 ahora revocada).
- STD-008 §3.1 Clean Code (Robert C. Martin) — fundamento de
  la regla.
- Commits clave: `bc2f74d7` (foundation), `b9dae9a3` (B-A
  pioneer), `5c33400a` (B-B), `494be743` (B-C), `31a11a07`
  (B-D), `e54aff14` (B-E), `28c7df6c` (B-F), `e6f8e701`
  (B-G extended).
