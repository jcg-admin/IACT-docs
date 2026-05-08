```yml
created_at: 2026-05-06 06:50:00
project: IACT-docs
work_package: 2026-05-06-06-32-20-spanish-class-names-corpus-audit
phase: Phase 1 — DISCOVER (consolida Phase 3 ANALYZE)
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Phase 1 DISCOVER — Spanish Class Names Corpus Audit

## Hallazgos cuantificados

### Categorias de identifiers en espanol detectados

Per directiva del ejecutor + STD-008 §3.5 v1.3.0, los siguientes
identifiers en espanol son violaciones:

| Categoria | Detalle | Conteo verificado |
|---|---|---|
| Clases / entidades | `class Usuario`, `entity EventoAuditoria`, etc. | **147** |
| Metodos | `+ asignarFunciones()`, `+ verificarPermiso(usuario, funcion)` | **87** |
| Atributos snake_case | `+ usuario_id : int`, `+ tipo_evento : varchar(50)` | **40** |
| **TOTAL violaciones** | | **274** |

### Distribucion por zona

| Zona | Archivos | Violaciones aprox |
|---|---|---|
| `requisitos/_metodologia-aplicacion/` | 61 | ~230 (84% del total) |
| `base-cognitiva/_uml/` | 5 | ~20 |
| `normativa/estandares/metodologia-*-ucs.rst` | 2 | ~15 |
| `backend/adr-back-003-orm-sql-hybrid-permissions.rst` | 1 | ~5 |
| **TOTAL** | **69** | **~274** |

### Vocabulario detectado

**Clases:** Usuario, Sesion, Llamada, Operador, Reporte, Permiso,
Funcion, Grupo, Asignacion, Auditoria, Evento, Cliente,
PermisoExcepcional, AuditoriaAcceso, AuditoriaPermiso,
DetalleAuditoria, EventoAuditoria, TipoEvento, DisparadorETL,
ReporteLlamadasAbandonadas, etc.

**Metodos (verbo ES + PascalCase):** asignar*, consultar*,
registrar*, guardar*, recuperar*, eliminar*, crear*, obtener*,
validar*, verificar*, enviar*, recibir*, cancelar*, reintentar*,
ejecutar*, listar*, buscar*, generar*, disparar*, procesar*,
calcular*, etc.

**Atributos (snake_case ES):** usuario_id, sesion_id, llamada_id,
funcion_id, tipo_evento, payload_json, ip_origen, fecha_*,
hora_*, nombre_*, descripcion_*, tipo_*, estado_*, etc.

## Causa raiz

1. **Material pedagogico siguiendo libros fuente en espanol**
   (Schmuller "Aprendiendo UML en 24 horas", literatura OOP en
   espanol). Los autores tradujeron directamente los ejemplos
   del libro sin re-traducir identifiers al ingles per STD-008.

2. **STD-008 §3.5 v1.0.0..1.1.0 no enumeraba excepciones
   explicitamente** — autores asumieron que zonas didacticas
   estaban exentas. v1.2.0 (que agregue en WP previo) FORMALIZO
   esa interpretacion incorrecta. v1.3.0 (revierte) clarifica
   que NO hay excepciones.

3. **Audit Brown 1998 cubrio domain-model/ pero NO el resto del
   corpus** — los 84/85 archivos de domain-model son canonical
   English, pero las zonas pedagogicas pasaron sin auditoria.

4. **Sin audit script automatizable hasta este WP** — la regla
   "ingles obligatorio" no se enforce'aba. Los autores no tenian
   feedback inmediato si violaban STD-008.

## Implicaciones de la directiva del ejecutor

> "no quieremos que nada tenga nombres de clases en espanol,
> lo unico que va en espanol son los comentarios"

Aplica a: clases, atributos, metodos, variables, parametros,
constantes, enums.
NO aplica a: comentarios, narrativa RST, captions, notas
PlantUML, strings de UI, paths de archivos (per STD-007).

Esto invalida la excepcion §3.5.1 que agregue en el WP previo
`naming-violations-arquitectura-tecnica-fix`. La nueva v1.3.0
de STD-008 (commit `bc2f74d7`) revoca explicitamente la
excepcion.

## Decision pendiente — opciones de remediacion

| Opcion | Descripcion | Esfuerzo | Trade-off |
|---|---|---|---|
| **(a)** | Re-escribir ejemplos pedagogicos en ingles (clases, metodos, atributos, narrativa) | ~6-8h | Pierde fidelidad al libro fuente Schmuller en espanol |
| **(b)** | Eliminar archivos pedagogicos | ~30min | Pierde material educativo del proyecto |
| **(c)** | Translate solo identifiers, mantener narrativa en espanol | ~3-4h | Balance: leccion sigue en espanol, identifiers en ingles |
| **(a) + (c)** | (recomendacion del ejecutor) | ~4-5h | Identifiers ingles + narrativa preservada en espanol donde sea didactica |

Opcion (a) + (c) combinada es la directiva del ejecutor — los
identifiers van TODOS en ingles, la narrativa puede mantenerse
en espanol.

## Plan de batches (si se aprueba opcion combinada)

| Batch | Zona | Archivos | Estrategia |
|---|---|---|---|
| **B-A** | `normativa/estandares/metodologia-*-ucs.rst` (2) | 2 | Pioneer — establece pattern de translation |
| **B-B** | `base-cognitiva/_uml/` (5) | 5 | Lecciones UML del proyecto |
| **B-C** | `requisitos/_metodologia-aplicacion/relaciones-uml/` (~15) | ~15 | Sub-zona |
| **B-D** | `requisitos/_metodologia-aplicacion/agregacion-interfaces/` (~5) | ~5 | Sub-zona |
| **B-E** | `requisitos/_metodologia-aplicacion/analisis-dominio/` (~28) | ~28 | Sub-zona mas grande (incluye EventoAuditoria) |
| **B-F** | `requisitos/_metodologia-aplicacion/orientacion-objetos/` + otros (~13) | ~13 | Resto de sub-zonas |
| **B-G** | `backend/adr-back-003` (1) | 1 | Caso especial — codigo legacy |

## Vocabulario de translation canonico

Mapeo basado en domain-model existente + Clean Code §3.1:

### Clases

| ES | EN |
|---|---|
| Usuario | User |
| Sesion | Session |
| Llamada | Call |
| Operador | Operator |
| Reporte | Report |
| Permiso | Permission |
| Funcion | Function |
| Grupo | Group |
| Asignacion | Assignment |
| Auditoria | Audit |
| Evento | Event |
| EventoAuditoria | AuditEvent |
| TipoEvento | EventType |
| Cliente | Client |
| PermisoExcepcional | ExceptionalPermission |
| AuditoriaAcceso | AccessAudit |
| AuditoriaPermiso | PermissionAudit |
| DetalleAuditoria | AuditDetail |
| DisparadorETL | (eliminar — usar PipelineExecution.start()) |
| ReporteLlamadasAbandonadas | AbandonmentReport |
| ReporteTransferencias | TransferReport |
| Catalogo | Catalog |
| Pagina | Page |
| Tarjeta | Card |

### Metodos (verbos)

| ES | EN |
|---|---|
| asignar* | assign* |
| consultar* | query* o get* |
| registrar* | register* o record* |
| guardar* | save* |
| recuperar* | recover* o retrieve* |
| eliminar* | delete* o remove* |
| crear* | create* |
| obtener* | get* |
| validar* | validate* |
| verificar* | verify* o check* |
| enviar* | send* |
| recibir* | receive* |
| cancelar* | cancel* |
| reintentar* | retry* |
| ejecutar* | execute* o run* |
| listar* | list* |
| buscar* | search* o find* |
| generar* | generate* |
| disparar* | trigger* o fire* |
| procesar* | process* |
| calcular* | calculate* o compute* |

### Atributos snake_case

| ES | EN |
|---|---|
| usuario_id | user_id |
| sesion_id | session_id |
| llamada_id | call_id |
| funcion_id | function_id |
| tipo_evento | event_type |
| payload_json | payload_json (sin cambio — ya neutral) |
| ip_origen | source_ip |
| fecha_creacion | created_at |
| hora_creacion | created_at |
| nombre | name |
| descripcion | description |
| tipo | type |
| estado | state o status |
| cantidad | quantity o count |
| precio | price |
| monto | amount |
| total | total |
| saldo | balance |

## Limitaciones del audit script actual

`scripts/validate-naming-corpus.sh` (commit `bc2f74d7`) detecta
las **147 violaciones de clases** correctamente, pero **NO
detecta metodos ni atributos** debido a un bug en la iteracion
del array de patrones. Los conteos de 87 metodos + 40 atributos
provienen de grep manual directo.

Mejora pendiente: corregir el script para que itere los 5
patrones (3 clases + 1 metodos + 2 atributos) en un solo loop.
Actualmente itera solo los 3 patterns originales.

Workaround actual:

```bash
# Counter de metodos (verbo ES + PascalCase)
grep -rnE --include="*.rst" \
  '^\s*[+\-#~]\s*(asignar|consultar|registrar|guardar|recuperar|eliminar|crear|obtener|validar|verificar|enviar|recibir)[A-Z][a-zA-Z]*\s*\(' \
  source/ | grep -v _generated | wc -l

# Counter de atributos (snake_case ES)
grep -rnE --include="*.rst" \
  '^\s*[+\-#~]\s*(usuario_|sesion_|llamada_|tipo_evento|payload_json|ip_origen|funcion_id)[a-z_]*\s*:' \
  source/ | grep -v _generated | wc -l
```

## Stopping Point Manifest

| ID | Fase | Tipo | Evento | Accion |
|---|---|---|---|---|
| SP-01 | DISCOVER → EXECUTE | gate-humano | aprobar opcion (a/b/c) y vocabulario de translation | Avanzar a EXECUTE batches |
| SP-02 | EXECUTE batch | gate-tecnico | build strict 0 warnings tras cada batch | Continuar siguiente batch |
| SP-03 | EXECUTE → TRACK | gate-tecnico | audit corpus 0 violaciones (con script corregido) | Cerrar WP |

## Riesgos

| ID | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Audit script incompleto reporta falsos OK | Workaround grep manual hasta corregir el script |
| R-02 | 274 cambios manuales en 69 archivos = potencial typos masivos | Build strict tras cada batch |
| R-03 | Translation inventa nombres no canonicos | Validar contra domain-model antes de aplicar |
| R-04 | Cambios pierden valor pedagogico (ej: "Usuario" cultural vs "User" generico) | Mantener narrativa en espanol; solo identifiers en ingles |
| R-05 | Backend ADR documenta legacy real con identifiers ES | Decision: agregar nota inline "esto viola STD-008 v1.3.0; legacy pendiente migracion" |

## Estado actual del WP

- ✅ Phase 1 DISCOVER: este analisis.
- ✅ Foundation: STD-008 v1.3.0 + audit script v1 (con bug de
  metodos/atributos).
- ⏸ Phase 10 EXECUTE: pausa, esperando SP-01 (decision opcion
  + vocabulario aprobado).
