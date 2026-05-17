```yml
created_at: 2026-05-08 01:50:00
project: IACT-docs
work_package: 2026-05-08-01-18-37-naming-rules-resolution
phase: Phase 10 — EXECUTE (loop)
author: NestorMonroy
status: Aprobado
version: 1.0.0
type: Decisions Log (4 decisiones)
```

# Decisions Log — 4 decisiones del audit

> Documenta las 4 decisiones normativas resueltas en este WP,
> con hallazgo, decision aplicada, cambio ejecutado y
> validacion.

## Orden de ejecucion (segun directiva del ejecutor)

D1 → D4 → D2 → D3.

D1 desbloquea Sprint 1 + Sprint 3.
D4 + D2 amplian alcance real de WP-G futuro.
D3 es caso puntual independiente.

---

## D1 — Conflicto `backend/conventions.rst` vs CLEAN_CODE §6.2

### Hallazgo

`source/backend/conventions.rst` v1.0.0 (lineas 36-39)
prescribia explicitamente sufijos prohibidos por CLEAN_CODE §6.2:

- `Serializer` (DRF mecanismo)
- `ViewSet` (DRF mecanismo)
- `View` (DRF APIView)
- `Permission` (DRF permission class)

### Decision aplicada

**Opcion A** (alinear `conventions.rst` con CLEAN_CODE).

Razon documentada por el ejecutor:

> "El conflicto es real y tiene una causa clara:
> conventions.rst fue escrito antes de que se estableciera
> la regla de prohibicion. No es conflicto de opinion, es
> documento desactualizado. Mantener los dos en conflicto
> (B o C) es tecnicamente peor que resolver, porque
> cualquier desarrollador que lea conventions.rst va a
> seguir usando los sufijos creyendo que esta correcto."

### Cambio ejecutado

`source/backend/conventions.rst` bumpeado a **v2.0.0**:

1. Agregada nota explicita declarando CLEAN_CODE como
   autoridad normativa.
2. Tabla de sufijos prohibidos con reemplazos canonicos
   (Serializer → Representation, ViewSet → Endpoint, etc.).
3. Seccion "Convivencia con la herencia del framework" con
   ejemplos de codigo donde el nombre de la clase es de
   dominio y la clase base es DRF.
4. Guia de archivos: nombre de la CLASE es lo critico, no
   el del archivo (`serializers.py` puede mantener su
   nombre tradicional si el proyecto ya lo usa).

### Validacion

- ✅ Bump version 1.0.0 → 2.0.0.
- ✅ Cross-ref a `clean-code-naming-principles` agregado.
- ✅ Sufijos prohibidos enumerados explicitamente.
- ✅ Ejemplos de codigo correctos.

### Efecto sobre el roadmap

WP-D del roadmap futuro: **resuelto en este commit**.

Sprint 1 y Sprint 3 del roadmap **desbloqueados** —
pueden proceder con rename masivo de clases sin generar
nueva contradiccion normativa.

---

## D4 — Excepcion RBAC formal en STD-010

### Hallazgo

El audit detecto 1373 refs a `RBAC` en source/. El analisis
mostro que la mayoria son uso disciplinar legitimo (vocabulario
estandar de seguridad informatica), pero la norma STD-010
no tenia excepcion formal para acronimos disciplinares.

### Decision aplicada

**Excepcion formal escrita en STD-010, no implicita.**

Razon documentada por el ejecutor:

> "No hay excepciones implicitas en un documento normativo.
> Una excepcion implicita es una excepcion que cada
> desarrollador va a interpretar de forma diferente. La
> excepcion correcta es una regla escrita con criterio
> claro de donde aplica y donde no."

### Cambio ejecutado

`source/normativa/estandares/std-010-vocabulario-abstracto.rst`
v1.0.0 → **v1.1.0** (bump MINOR — amplia sin contradecir).

Agregada **§5.4 "Acronimos de disciplina aceptados en prosa"**:

- RBAC declarado vocabulario disciplinar aceptable en prosa
  explicativa de documentos normativos y arquitectonicos.
- Lista explicita de "donde APLICA" (prosa, cross-refs,
  directorios, captions con concepto disciplinar).
- Lista explicita de "donde NO APLICA" (identificadores
  Python, sufijos de clase, variables, atributos UC tipo
  `RBAC-gated`).
- Criterio de distincion documentado.

Agregada **§5.5 "Identificadores opacos con dependencias
externas"**:

- Tokens RBAC backend: `access:view_sod`, `access:update_sod`,
  `access:disable_sod`.
- Codigos BD: `SOD-001..003`, `AGR-001..010`.
- Razon: contratos de integracion / IDs persistidos
  requieren migracion de datos para cambiar.

### Validacion

- ✅ Bump version 1.0.0 → 1.1.0.
- ✅ §5.4 con criterio explicito de aplicacion / no-aplicacion.
- ✅ §5.5 alineada con audit C2 §6 (excepciones documentadas).

### Efecto sobre el roadmap

WP-G futuro tiene ahora **criterio claro** sobre los 1373
hits de RBAC: la gran mayoria son prosa disciplinar (no
violacion). Solo restan los identificadores tipo
`RBACBackend`, `RBACPermission`, `RBAC-gated` que el WP-G
deberia atender.

---

## D2 — Scope de STD-010

### Hallazgo

STD-010 §2 tabla original solo declaraba 2 entradas exempt:
`implementacion-tecnica.rst` y `arquitectura-tecnica/**`.
El audit detecto ambiguedad en:

- `_metodologia-aplicacion/` (no listado)
- `index.rst` raiz (no listado)
- Sistemas externos del cliente (sin tratamiento normativo)
- `backend/` (no listado, pero documenta implementacion)
- `reglas-negocio/`, `base-cognitiva/` (no listados,
  interpretacion ambigua)

### Decision aplicada

Tres reglas distintas segun naturaleza del archivo:

**a)** `_metodologia-aplicacion/` **exenta** — es
documentacion de proceso interno, no especificacion de
sistema. Aplicar STD-010 a doc sobre como trabajar es
error de categoria.

**b)** `index.rst` raiz **por contenido** (no por nombre).
Si tiene narrativa de UC o diagramas, aplica. Si es solo
navegacion, exento.

**c)** Sistemas externos del cliente **exentos** por
nombre propio. Cuando se referencia un sistema externo por
su nombre real (ej: "MySQL del IVR del cliente"), la
abstraccion oculta informacion factual relevante.

### Cambio ejecutado

`std-010-vocabulario-abstracto.rst` v1.1.0 amplia §2:

- §2.1 tabla expandida con entradas explicitas:
  - `requisitos/reglas-negocio/**` → Sí
  - `base-cognitiva/**` → Sí (vocabulario)
  - `index.rst` raiz → Por contenido (§2.2)
  - `backend/**` → No — libre
  - `_metodologia-aplicacion/**` → No — exenta (§2.3)

- §2.2 nueva: clarificacion de aplicacion por contenido
  para `index.rst`.
- §2.3 nueva: exencion formal de `_metodologia-aplicacion/`.
- §2.4 nueva: exencion formal de sistemas externos del
  cliente con criterio de aplicacion.

### Validacion

- ✅ Tabla §2.1 expandida con 4 entradas adicionales.
- ✅ §2.2, §2.3, §2.4 con razonamiento explicito.
- ✅ Criterio claro: "comportamiento del sistema IACT" vs
  "hechos arquitectonicos del entorno externo".

### Efecto sobre el roadmap

WP-G futuro tiene ahora **scope real**:

- Excluye `_metodologia-aplicacion/` (~80 ediciones
  estimadas en audit C3 — fuera de scope).
- Excluye `backend/` (no listado, pero confirmado libre
  porque documenta implementacion).
- Aplica a `casos-uso/*/{flujo,actores,...}`,
  `reglas-negocio/`, `base-cognitiva/`, `index.rst` (segun
  contenido).
- Refs a sistemas externos preservadas con nota.

Reduccion estimada del scope WP-G: de ~265 ediciones a
~150-180 (40% menos).

---

## D3 — `ResumenSaludBuilder`: ¿viola §1.2?

### Hallazgo

El audit C1 detecto `ResumenSaludBuilder` como una clase
con sufijo `Builder` (prohibido por CLEAN_CODE §1.2).

Verificacion del codigo (UML en
`source/arquitectura-tecnica/domain-model/resumen-salud-builder.rst`):

```
class ResumenSaludBuilder {
  - umbral_lag_amarillo : Integer
  - umbral_lag_rojo : Integer
  - umbral_errores_rojo : Integer
  --
  + build(executions : List<PipelineExecution>, \
           errores : List<ETLError>) : ResumenSalud
  - derive_estado(metrics : Metrics) : EstadoSalud
}
```

**Resultado:** UN solo metodo publico (`build`) que recibe
todas las entradas como parametros y devuelve el resultado.
**No hay encadenamiento fluent** (`.conFecha(...).conIndicadores(...).build()`).

### Decision aplicada

Segun criterio del ejecutor:

> "Si es simplemente una clase que construye un ResumenSalud
> sin encadenamiento, el nombre correcto es
> ResumenSaludAssembler o directamente nombrar por el rol
> que cumple en el dominio."

**Renombrar a `ResumenSaludAssembler`.**

### Cambio ejecutado

1. `git mv resumen-salud-builder.rst resumen-salud-assembler.rst`
2. Contenido actualizado:
   - Title `ResumenSaludBuilder` → `ResumenSaludAssembler`
   - Anchor `_dm_class_resumen_salud_builder` →
     `_dm_class_resumen_salud_assembler`
   - Artefacto `AT_DM_CLASS_RESUMEN_SALUD_BUILDER` →
     `AT_DM_CLASS_RESUMEN_SALUD_ASSEMBLER`
   - Descripcion: "Builder que ensambla..." → "Assembler que
     construye... Patron Assembler (no Builder GoF)".
   - Nota agregada explicando el rename historico.
   - Identificadores en plantuml (3 refs en clases +
     relations).
3. Cross-refs externos actualizados:
   - `domain-model/index.rst` toctree.
   - `domain-model/resumen-salud.rst` (2 refs).
   - `domain-model/supervision-etl-service.rst` (5 refs +
     1 :doc: ref).
   - `casos-uso/pipeline/uc-pip-01/implementacion-tecnica.rst`
     (3 refs).
   - `casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-actividad.rst`
     (1 :doc: ref).
   - `casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-clases.rst`
     (3 refs).

### Validacion

- ✅ 0 refs `ResumenSaludBuilder` en codigo (excepto la
  nota historica en el propio archivo).
- ✅ 24 refs nuevas a `ResumenSaludAssembler`.
- ✅ `git mv` preserva historia.

### Efecto sobre el roadmap

WP-E futuro tiene un caso menos. Los 6 Builder restantes
(`ComparativeBuilder`, `DisponibilidadBuilder`,
`HeatmapBuilder`, `MenuBuilder`, `QueryBuilder`,
`SummaryBuilder`) deben verificarse caso-por-caso con el
mismo criterio (¿interfaz fluent real o no?).

---

## Resumen — efectos en el roadmap futuro

| Decision | WPs afectados | Estado post-decision |
|---|---|---|
| D1 | WP-D, WP-F | WP-D resuelto aqui; WP-F desbloqueado |
| D4 | WP-G criterio | WP-G tiene criterio claro |
| D2 | WP-G scope | WP-G alcance reducido ~40% |
| D3 | WP-E | 1 caso resuelto; 6 pendientes con criterio |

## Refs

- WP `clean-code-naming-audit` (predecesor, audit-only).
- `CLEAN_CODE_NAMING_PRINCIPLES` v1.0.0.
- `STD-010` v1.0.0 → v1.1.0 (bumpeado en este WP).
- `backend/conventions.rst` v1.0.0 → v2.0.0 (bumpeado en
  este WP).
- `domain-model/resumen-salud-assembler.rst` (renombrado).
