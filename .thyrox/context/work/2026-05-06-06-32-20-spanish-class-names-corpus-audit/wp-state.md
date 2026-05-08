```yml
project: IACT-docs
work_package: 2026-05-06-06-32-20-spanish-class-names-corpus-audit
created_at: 2026-05-06 06:32:20
closed_at: 2026-05-06 07:30:00
current_phase: Phase 11 — TRACK/EVALUATE
status: Cerrado
final_audit_classes: 0 violations
final_audit_methods: 0 violations
final_audit_attrs: 12 false-positives (SBVR vocab + ADR legacy descriptive)
files_modified: 76+
std_008_version: 1.1.0 -> 1.3.0
batches_completed: B-A, B-B, B-C, B-D, B-E, B-F, B-G+ extended
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: grande (Stages 1-12 si se aprueba remediacion masiva)
target: Auditar TODO el corpus de docs (no solo arquitectura-tecnica) en busca de clases con nombres en espanol y producir plan de remediacion. Per directiva del ejecutor: "nada en class names en espanol — solo comentarios". Esto invalida la excepcion §3.5.1 de STD-008 que agregue en el WP previo.
predecessor_wp: 2026-05-06-06-24-49-naming-violations-arquitectura-tecnica-fix
trigger: directiva del ejecutor "no quieremos que nada tenga nombres de clases en espanol, lo unico que va en espanol son los comentarios"
governance_basis:
  - STD-008 §3.1 (Clean Code de Robert C. Martin obligatorio)
  - STD-008 §3.5 (Coherencia de Idioma — identifiers en ingles)
```

# WP — Spanish Class Names Corpus Audit

## Trigger

WP previo `naming-violations-arquitectura-tecnica-fix` agrego una
excepcion §3.5.1 a STD-008 permitiendo identifiers en espanol en
zonas pedagogicas. **El ejecutor rechazo esa excepcion**:

> "no quieremos que nada tenga nombres de clases en espanol, lo
> unico que va en espanol son los comentarios"

La regla original de STD-008 §3.1 (Clean Code obligatorio) y
§3.5 (identifiers en ingles) NO admite excepciones — la
narrativa puede ser en espanol pero los identifiers no.

## Estado actual del corpus

Audit cuantitativo:

| Zona | Archivos | Estado per regla estricta |
|---|---|---|
| `requisitos/_metodologia-aplicacion/` | 61 | ❌ violacion |
| `base-cognitiva/_uml/` | 5 | ❌ violacion |
| `normativa/estandares/metodologia-*-ucs.rst` | 2 | ❌ violacion |
| `backend/adr-back-003-orm-sql-hybrid-permissions.rst` | 1 | ❌ (era considerado descriptivo legacy) |

**Totales:**
- **69 archivos** con clases en espanol.
- **203 declaraciones** `class <NombreEsp>` o `entity <NombreEsp>`.

## Acciones requeridas

### A-1 — Revertir §3.5.1 + §3.5.2 de STD-008

La excepcion para zonas pedagogicas que se agrego en el WP
previo fue rechazada por el ejecutor. Revertir STD-008 a v1.1.0
(quitar §3.5.1 y §3.5.2 que agregue), o avanzar a v1.3.0
agregando §3.5.3 que **explicitamente prohibe identifiers en
espanol incluso en zonas didacticas**, manteniendo la narrativa
en espanol.

Decision pendiente del ejecutor: revertir vs prohibir
explicitamente. Recomendacion: **prohibir explicitamente**
(mas claro que ausencia).

### A-2 — Actualizar audit script C-07

`scripts/validate-naming-arquitectura-tecnica.sh` actualmente
excluye zonas pedagogicas. Cambiar a auditar **todo el corpus**
sin excepciones (renombrar a `validate-naming-corpus.sh` o
quitar la lista de exclusiones).

### A-3 — Plan de remediacion masiva (203 declaraciones)

Tres opciones:

#### Opcion (a) — Re-escribir ejemplos pedagogicos en ingles

- Pros: alinea 100% con STD-008.
- Contras: pierde fidelidad al libro fuente Schmuller (UML
  for Database Design with Patterns) que usa ejemplos en
  espanol; el lector hispanohablante pierde contexto natural.
- Effort: alto (~6-8 horas, 61 archivos del metodologia).

#### Opcion (b) — Eliminar archivos pedagogicos

- Pros: rapido, elimina violacion.
- Contras: pierde material educativo del proyecto. Podrian
  haber sido referenciados desde otros docs.
- Effort: bajo (~30 min) + verificar refs huerfanas.

#### Opcion (c) — Translate solo identifiers, mantener narrativa ES

- Pros: balance entre fidelidad pedagogica y compliance con
  STD-008. La leccion sigue ensenando en espanol pero los
  ejemplos de codigo usan PascalCase ingles.
- Contras: rompe la "naturalidad" del ejemplo (Usuario→User
  pierde el contexto cultural del lector).
- Effort: medio (~3-4 horas).

### A-4 — Backend ADR

`backend/adr-back-003-orm-sql-hybrid-permissions.rst` cita
codigo real del legacy: `class GrupoPermisoAdmin(admin.ModelAdmin):`.

Decision: el ADR es DESCRIPTIVO de un sistema legacy con
identifiers en espanol. Si el sistema se renombra (gran tarea),
el ADR debe actualizarse. Si NO se renombra (asumido stack
legacy), el ADR puede mantenerse pero documentar explicitamente
"este es codigo del legacy, no prescripcion para nuevo codigo".

Opcion mas pragmatica: agregar nota inline al ADR aclarando
naturaleza descriptiva.

## Stopping points

- **SP-01** (gate humano): aprobar la opcion de remediacion
  (a, b, o c) y el alcance.
- **SP-02** (gate humano): aprobar plan de batches por modulo.
- **SP-03** (gate tecnico): audit `validate-naming-corpus.sh`
  con 0 violaciones.

## Riesgos

| ID | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Opcion (a) introduce traducciones inventadas que no estan en domain-model | Validar cada nombre contra catalogo canonico antes de aplicar |
| R-02 | Opcion (b) crea broken refs si los ejemplos eran citados | grep -r "primer-erd-iact-entidad-eventoauditoria" antes de borrar |
| R-03 | Opcion (c) rompe naturalidad pedagogica del libro fuente | Documentar en notas inline del archivo: "los identifiers se traducen al ingles per STD-008; el contenido didactico mantiene espanol" |
| R-04 | Cambio en STD-008 §3.5 invalida WP previo (recien commiteado) | Documentar la reversion explicitamente con commit Tim Pope |
| R-05 | 203 cambios masivos pueden tener typos y romper builds | Build strict tras cada batch (~10 archivos) |

## Output esperado

1. `discover/spanish-class-names-corpus-audit-analysis.md` —
   inventario completo de las 203 declaraciones por archivo
   y categoria.
2. (Si SP-01 aprueba opcion a o c): `analyze/translation-mapping.md` —
   tabla con nombre ES → nombre EN para cada clase.
3. `track/std-008-revert-or-strengthen.md` — diff de la version
   final de STD-008.
4. `scripts/validate-naming-corpus.sh` — version sin
   exclusiones.
5. (Si SP-01 aprueba opcion b): `track/orphan-references.md` —
   refs cross-doc que apuntaban a archivos eliminados.

## Anatomia

```
2026-05-06-06-32-20-spanish-class-names-corpus-audit/
├── wp-state.md
├── discover/
│   └── spanish-class-names-corpus-audit-analysis.md
├── analyze/
│   ├── translation-mapping.md           ← si opcion a/c
│   └── orphan-references.md             ← si opcion b
└── track/
    ├── std-008-revert-or-strengthen.md
    └── spanish-class-names-corpus-audit-changelog.md
```
