```yml
created_at: 2026-05-06 07:00:00
project: IACT-docs
work_package: 2026-05-06-06-32-20-spanish-class-names-corpus-audit
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Task Plan — Spanish Class Names Corpus Audit

## Resumen

Plan granular T-NNN para traducir identificadores en español a
inglés en 69 archivos del corpus, preservando narrativa en
español per STD-008 v1.3.0 §3.5.

| Métrica | Valor |
|---|---|
| Total tasks | 76 (T-001..T-076) |
| Archivos a translate | 69 |
| Tasks de infra (audit script, validacion) | 7 |
| Estimación total | 6-10 horas wall-clock multi-sesión |

## Convenciones del plan

- `[x]` = completado
- `[ ]` = pendiente
- `[~]` = en progreso (parcial)
- Estado actual: solo T-001..T-002 completas, T-003 parcial.

----

## Tasks de infraestructura

### Foundation (DONE)

- [x] **T-001** — STD-008 v1.3.0 §3.5 actualizado (revoca §3.5.1 excepción).
- [x] **T-002** — `scripts/validate-naming-corpus.sh` creado (detecta clases).
- [ ] **T-003** — Fix bug del audit script: array iteration NO suma matches de METHOD_PATTERNS + ATTR_PATTERNS. Reescribir con grep recursivo simple. **Bloquea** SP-03.

### Closure infra

- [ ] **T-073** — Re-run audit script post-translation, esperar 0 violaciones.
- [ ] **T-074** — Build strict `-W` 0 warnings post-batch final.
- [ ] **T-075** — Coverage analysis pre-cierre del WP.
- [ ] **T-076** — Cerrar WP (changelog + lessons-learned + wp-state.md status: Cerrado).

----

## B-A — normativa/estandares/metodologia-*-ucs.rst (2 files)

Pioneer batch — establece pattern de translation.

- [x] **T-004** — `metodologia-oop-para-ucs.rst` (5 violaciones)
  - DONE en commit `b9dae9a3`. Audit clean.
- [~] **T-005** — `metodologia-analisis-dominio-ucs.rst` (parcial)
  - Bloque 1 (lineas 124-314) DONE en commit `b9dae9a3`.
  - PENDIENTE: bloques 326-706 (lineas 328 Usuario, 483 Stock, 534 Stock, 618 Cliente, 624 Carrito, 630 Orden, 640 Pago, 647 Cupon, 684 Orden, 697 Pago + atributos + metodos asociados).

----

## B-B — base-cognitiva/_uml/ (5 files)

Lecciones UML del proyecto.

- [ ] **T-006** — `uml-02-orientacion-objetos/tipos-de-asociaciones.rst`
- [ ] **T-007** — `cuando-usar-cada-diagrama/notas-explicaciones-comentarios.rst`
- [ ] **T-008** — `uml-04-uso-relaciones/asociaciones-reflexivas.rst`
- [ ] **T-009** — `uml-04-uso-relaciones/restricciones-en-las-asociaciones.rst`
- [ ] **T-010** — `uml-07-diagramas-casos-uso/comprension-del-dominio.rst`

----

## B-C — requisitos/_metodologia-aplicacion/relaciones-uml/ (~20 files)

Sub-zona "relaciones-uml" — ejemplos de relaciones entre clases.

- [ ] **T-011** — `relaciones-uml/usuario-consulta-reporte-uc-rpt.rst`
- [ ] **T-012** — `relaciones-uml/suscripcion-entre-usuario-y-alerta-uc-alr-05.rst`
- [ ] **T-013** — `relaciones-uml/secrules-usa-funcion-uc-perm-07.rst`
- [ ] **T-014** — `relaciones-uml/roles-en-asociacion-relacion-empleador-empleado.rst`
- [ ] **T-015** — `relaciones-uml/restriccion-xor-permiso-via-grupo-o-excepcional.rst`
- [ ] **T-016** — `relaciones-uml/reporte-usa-filtro-uc-rpt-09.rst`
- [ ] **T-017** — `relaciones-uml/multiplicidades-canonicas-iact.rst`
- [ ] **T-018** — `relaciones-uml/jerarquia-de-usuario-en-iact.rst`
- [ ] **T-019** — `relaciones-uml/herencia-multinivel-reporte.rst`
- [ ] **T-020** — `relaciones-uml/funcion-compuesta-funcion-funcion.rst`
- [ ] **T-021** — `relaciones-uml/ejemplo-iact-snapshot-pre-refactor.rst`
- [ ] **T-022** — `relaciones-uml/ejemplo-aplicado-a-iact.rst`
- [ ] **T-023** — `relaciones-uml/cadena-de-mando-usuario-supervisa-usuario.rst`
- [ ] **T-024** — `relaciones-uml/busqueda-de-reporte-por-nombre-programado.rst`
- [ ] **T-025** — `relaciones-uml/busqueda-de-llamada-por-id.rst`
- [ ] **T-026** — `relaciones-uml/asociacion-bidireccional.rst`
- [ ] **T-027** — `relaciones-uml/asignacion-entre-usuario-y-funcion-uc-acc-01.rst`
- [ ] **T-028** — `relaciones-uml/aplicacion-a-iact-snapshot-de-dependencias.rst`
- [ ] **T-029** — `relaciones-uml/aplicacion-a-iact-consultareporterequest.rst`
- [ ] **T-030** — `relaciones-uml/agregacion-grupo-agrega-funciones.rst`

SP-G-C: build incremental tras T-030.

----

## B-D — requisitos/_metodologia-aplicacion/agregacion-interfaces/ (~10 files)

- [ ] **T-031** — `agregacion-interfaces/restriccion-or-en-agregacion.rst`
- [ ] **T-032** — `agregacion-interfaces/paso-3-diagrama-de-contexto-integrado.rst`
- [ ] **T-033** — `agregacion-interfaces/paso-2-interfaces-visibilidad.rst`
- [ ] **T-034** — `agregacion-interfaces/paso-1-agregacion-composicion.rst`
- [ ] **T-035** — `agregacion-interfaces/isegmentable-filtrado-por-segmento-br-012.rst`
- [ ] **T-036** — `agregacion-interfaces/iexportable-uc-rpt-04-uc-aud-03-uc-log-04.rst`
- [ ] **T-037** — `agregacion-interfaces/funcion-grupo-catalogo-rbac-iact.rst`
- [ ] **T-038** — `agregacion-interfaces/ejemplo-clase-reporte.rst`
- [ ] **T-039** — `agregacion-interfaces/contexto-de-sistema-iact-completo.rst`
- [ ] **T-040** — `agregacion-interfaces/catalogo-de-funciones-instancia-compartida.rst`

SP-G-D: build incremental tras T-040.

----

## B-E — requisitos/_metodologia-aplicacion/analisis-dominio/ (~22 files)

Sub-zona más grande. Incluye los diagramas EventoAuditoria.

- [ ] **T-041** — `analisis-dominio/subtipos-con-etiqueta-implements.rst`
- [ ] **T-042** — `analisis-dominio/sintaxis-plantuml-minima.rst`
- [ ] **T-043** — `analisis-dominio/primer-erd-iact-entidad-eventoauditoria.rst` (ERD EventoAuditoria → AuditEvent)
- [ ] **T-044** — `analisis-dominio/multiplicidad-minima-del-primer-modelo.rst`
- [ ] **T-045** — `analisis-dominio/estructura-uml-de-una-clase.rst`
- [ ] **T-046** — `analisis-dominio/erd-consolidado.rst`
- [ ] **T-047** — `analisis-dominio/equivalente-iact-ejecucionetl-y-sus-partes.rst`
- [ ] **T-048** — `analisis-dominio/el-equivalente-iact-rbac-y-agregaciones-canonicas.rst`
- [ ] **T-049** — `analisis-dominio/ejemplo-iact-vinculacion-textual-recomendada.rst`
- [ ] **T-050** — `analisis-dominio/ejemplo-iact-usuario-grupo.rst`
- [ ] **T-051** — `analisis-dominio/ejemplo-iact-eventoauditoria-y-tipoevento.rst`
- [ ] **T-052** — `analisis-dominio/ejemplo-iact-eventoauditoria-con-fk-opcionales.rst`
- [ ] **T-053** — `analisis-dominio/ejemplo-iact-diagrama-limpio-sin-compartimentos.rst`
- [ ] **T-054** — `analisis-dominio/ejemplo-iact-consolidado.rst`
- [ ] **T-055** — `analisis-dominio/ejemplo-iact-agrupacion-con-package.rst`
- [ ] **T-056** — `analisis-dominio/ejemplo-completo-clase-reporte.rst`
- [ ] **T-057** — `analisis-dominio/diagrama-de-clases-integrado-del-dominio-iact.rst`
- [ ] **T-058** — `analisis-dominio/crecimiento-del-modelo-a-partir-de-la-primera-relacion.rst`
- [ ] **T-059** — `analisis-dominio/conversion-a-clases-vista-global-del-dominio.rst`
- [ ] **T-060** — `analisis-dominio/como-se-ve-aplicado.rst`
- [ ] **T-061** — `analisis-dominio/aplicacion-al-modelo-iact.rst`
- [ ] **T-062** — `analisis-dominio/aplicacion-a-iact.rst`

SP-G-E: build incremental tras T-062 (mayor batch — verificar
con cuidado).

----

## B-F — requisitos/_metodologia-aplicacion/ otros sub-zonas (~9 files)

- [ ] **T-063** — `patrones-diseno/factory-reportefactory.rst`
- [ ] **T-064** — `orientacion-objetos/jerarquia-de-actores-iact.rst`
- [ ] **T-065** — `orientacion-objetos/clase-reporte-uc-rpt.rst`
- [ ] **T-066** — `orientacion-objetos/asociaciones-canonicas-iact.rst`
- [ ] **T-067** — `orientacion-objetos/agregacion-vs-composicion-en-iact.rst`
- [ ] **T-068** — `orientacion-objetos/abstraccion-correcta-para-iact.rst`
- [ ] **T-069** — `diagramas-uml/diagrama-de-clases-entidad-llamada-uc-rpt.rst`
- [ ] **T-070** — buscar más en otras sub-zonas via re-audit (diagramas-secuencias, diagramas-actividades, etc.)
- [ ] **T-071** — verificar zonas que el audit ampliado podría revelar (atributos snake_case en archivos sin clases ES)

SP-G-F: build incremental tras T-071.

----

## B-G — backend ADR (caso especial)

- [ ] **T-072** — `backend/adr-back-003-orm-sql-hybrid-permissions.rst`
  - Decision: agregar nota inline "este código viola STD-008
    v1.3.0 — es legacy del backend, plan de migración pendiente"
    O renombrar las clases del legacy en el ADR (cambia el
    significado descriptivo del documento).
  - Esperar decision del ejecutor en SP-G-G.

----

## DAG de dependencias

```
T-001 (STD-008) ✓
   ↓
T-002 (audit script v1) ✓
   ↓
T-003 (fix audit script) ──┐
   ↓                       │
T-004..T-005 B-A        ✓ partial
   ↓                       │
T-006..T-010 B-B           │
   ↓                       │
T-011..T-030 B-C           │
   ↓                       │
T-031..T-040 B-D           │
   ↓                       │
T-041..T-062 B-E           │
   ↓                       │
T-063..T-071 B-F           │
   ↓                       │
T-072 B-G                  │
   ↓                       │
T-073 (re-audit) ←─────────┘
   ↓
T-074 (build strict)
   ↓
T-075 (coverage analysis)
   ↓
T-076 (cierre WP)
```

T-003 (fix script) puede ejecutarse en cualquier momento — no
bloquea las translations, pero bloquea T-073 (re-audit con
detección de métodos+atributos).

## Trazabilidad

| Stopping Point | Tras task | Validación requerida |
|---|---|---|
| SP-G-A (gate batch A) | T-005 | grep 0 ES en B-A files |
| SP-G-B (gate batch B) | T-010 | grep 0 ES en B-B files |
| SP-G-C (gate batch C) | T-030 | build incremental + grep |
| SP-G-D (gate batch D) | T-040 | build incremental + grep |
| SP-G-E (gate batch E) | T-062 | build incremental + grep |
| SP-G-F (gate batch F) | T-071 | build incremental + grep |
| SP-G-G (gate decisión) | pre-T-072 | decisión ADR backend |
| SP-03 (gate técnico final) | T-074 | audit corpus 0 + build strict 0 |

## Estado actual del WP

- ✅ T-001, T-002 done.
- ~ T-003 pending (medium prio, no blocker for translations).
- ~ T-004 done, T-005 partial.
- ⏸ T-006..T-076 pending.

**Progreso:** 2 / 76 tasks (2.6%) + 1 partial.

## Cómo continuar

Próxima sesión dedicada:

1. Completar T-005 (metodologia-analisis-dominio-ucs.rst restante).
2. Avanzar T-006..T-010 (B-B base-cognitiva, archivos pequeños).
3. T-003 fix audit script.
4. Avanzar B-C..B-F en sesiones múltiples.
5. T-072 cuando ejecutor decida sobre backend ADR.
6. T-073..T-076 cierre.

Cada batch requiere:
- Read file con `Read`.
- Identificar bloques @startuml con violations.
- Reescribir con identifiers en inglés via `Edit` (replace_all=false en patron único, o múltiples Edits).
- Verificar con grep manual.
- Commit Tim Pope per archivo o per sub-batch lógico.
