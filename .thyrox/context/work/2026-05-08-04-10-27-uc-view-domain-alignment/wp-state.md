```yml
project: IACT-docs
work_package: 2026-05-08-04-10-27-uc-view-domain-alignment
created_at: 2026-05-08 04:10:27
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: por estimar (alineacion baseline buena, gaps focalizados — DISCOVER lo cuantifica)
target: Auditar y alinear use-case-view/ con casos-uso/. Validar conformidad UML uml-07. Verificar y completar domain-model contra clases referenciadas por UCs.
predecessor_wp: 2026-05-08-03-56-35-tdd6-std010-scope-extension (cerrado)
trigger: directiva del ejecutor "abre un WP nuevo para auditar y alinear ..."
```

# WP — Use-Case-View ↔ Casos-Uso ↔ Domain-Model alignment

## Phase 1 — DISCOVER

### Inventario de los tres directorios

| Directorio | Conteo | Detalle |
|---|---|---|
| `source/requisitos/casos-uso/` | 88 UCs | 13 clusters (access, admin, alerts, audit, auth, caller, logs, operator, permissions, pipeline, reports, supervision, users) |
| `source/arquitectura-tecnica/use-case-view/` | 88 archivos UC + 13 cluster index + 3 raiz (index, panorama-iact, mapa-funciones-rbac) = 104 .rst | 1:1 numerico con casos-uso/ |
| `source/arquitectura-tecnica/domain-model/` | 109 archivos .rst de clases del dominio + index/overview | — |
| `source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/` | 11 archivos .rst (referencia normativa) | comprension, representacion, inclusion, extension, generalizacion, panorama, profundizacion, gaseosas, index |

### Alineacion casos-uso ↔ use-case-view

**Cobertura numerica:** 88 UCs en casos-uso/ ↔ 88 archivos UC en
use-case-view/. **1:1 perfecto** por UC ID.

**Cross-link integrity:**

- ✅ Todos los 88 archivos use-case-view linkean correctamente
  a `:doc:\`/requisitos/casos-uso/{cluster}/{uc-id}/index\``.
- ✅ Cero broken refs detectados desde casos-uso/ a use-case-view/
  (solo 2 refs totales — minimo cross-linking, esperado por
  separacion Kruchten).

### Alineacion casos-uso ↔ domain-model

**Refs casos-uso → domain-model:** 77 clases unicas referenciadas.
**Existen TODAS** en `source/arquitectura-tecnica/domain-model/`.

**Refs use-case-view → domain-model:** 86 clases unicas referenciadas.
**Existen TODAS** en `source/arquitectura-tecnica/domain-model/`.

✅ **Cero clases faltantes** detectadas en domain-model/ desde
ninguna direccion.

### Hallazgos de gap detectados

#### F-01: Tres UCs `Reservado` placeholder en casos-uso/ (uc-usr-05/06/07)

**Estado:** asimetrico.

| UC | use-case-view | casos-uso |
|---|---|---|
| uc-usr-05 (bloquear-usuario) | ✅ 56 lineas, diagrama UML completo | ⚠ solo `index.rst` placeholder Reservado, sin sub-archivos |
| uc-usr-06 (desbloquear-usuario) | ✅ 53 lineas, diagrama UML | ⚠ solo `index.rst` placeholder |
| uc-usr-07 (editar-perfil-propio) | ✅ 67 lineas, diagrama UML | ⚠ solo `index.rst` placeholder |

Los archivos casos-uso para estos UCs estan en estado
`:estado: Reservado` con `:version: 0.1.0` y nota
"origen: incierto — referenciado en uc-auth-03/04/05 sin
decision arquitectonica formal documentada".

Sin embargo, en use-case-view/ ya existen archivos completos
con diagramas UML y referencias a domain-model.

**Decision pendiente del ejecutor:** completar las 3 specs de
casos-uso o reducir el use-case-view a "Reservado" hasta tener
spec textual.

#### F-02: Conformidad UML uml-07 — todos cumplen los elementos basicos

Sample de 88 archivos use-case-view UC:

| Criterio uml-07 | Conformidad |
|---|---|
| `actor "..."` (stick figure) | ✅ 88/88 |
| `usecase "..."` (elipse) | ✅ 88/88 |
| `rectangle "..." { ... }` (system boundary) | ✅ 88/88 |
| `<<include>>` (relacion de inclusion) | usado en 85/88 |
| `<<extend>>` (relacion de extension) | usado en 27/88 |
| Generalizacion entre actores (`<|--`) | 0/88 (no aplica al modelo) |

**Resultado:** todos los archivos cumplen los elementos
estructurales basicos de uml-07. No se detecta violacion
sistematica.

**Pendiente verificar caso por caso (sample-based no
completo):** posicionamiento "iniciador a la izquierda /
beneficiario a la derecha" (uml-07
representacion-de-un-modelo-de-caso-de-uso). Esto requiere
revision visual o por convenciones (`left to right direction`,
orden de declaracion).

#### F-03: Asimetria de diagramas en casos-uso/uc-usr-05/06/07

Las tres UCs Reservado no tienen `diagramas-uml/`
directorio en su carpeta casos-uso. La asimetria con
use-case-view (que tiene diagramas) sugiere que se creo el
view con expectativa de UC futuro pero el UC nunca se
elaboro.

#### F-04: Otros 85 UCs tienen estructura completa

Los UCs restantes (auth, access, admin, alerts, audit, caller,
logs, operator, permissions, pipeline, reports, supervision, y
4 de users) tienen estructura completa:

```
casos-uso/{cluster}/{uc-id}/
├── index.rst
├── informacion-general.rst
├── actores-precondiciones.rst
├── flujo-principal.rst
├── flujos-alternos.rst
├── excepciones.rst
├── criterios-aceptacion.rst
├── datos-involucrados.rst
├── patrones-diseno.rst
├── requisitos-no-funcionales.rst
├── implementacion-tecnica.rst
├── testing.rst
└── diagramas-uml/
    ├── index.rst
    ├── diagrama-de-caso-de-uso.rst
    ├── diagrama-de-secuencia.rst
    ├── diagrama-de-actividad.rst
    ├── (diagrama-de-estados-*.rst, opcional)
    └── notas-sobre-los-diagramas.rst
```

440 archivos UML totales en `casos-uso/*/uc-*/diagramas-uml/`.

### Estimacion de scope para Phases 2+

**Trabajo bajo en cantidad, focalizado:**

1. **Resolucion de F-01 / F-03** — decidir tratamiento de
   uc-usr-05/06/07. Dos rutas alternativas:
   - **Ruta A (completar):** elaborar spec textual completa
     para cada UC siguiendo plantilla larman. ~3 UCs × ~10
     archivos cada uno = ~30 archivos a producir + diagramas
     (~3-5 diagramas por UC = ~15 archivos UML adicionales).
     **Total: ~45 archivos nuevos.**
   - **Ruta B (degradar view):** marcar use-case-view de
     uc-usr-05/06/07 como `:estado: Reservado` con misma
     justificacion que casos-uso side. **Total: 3 archivos
     modificar.**
   - **Decision del ejecutor.**

2. **F-02 conformidad uml-07 caso por caso** — auditoria
   visual o automatizable (verificar `left to right
   direction`, orden iniciador→receptor) sobre 88 archivos.
   Probablemente menor a un dia de trabajo. **Posible scope:
   0-15 ediciones de re-orden si se detecta inconsistencia.**

3. **Domain-model completeness** — todas las clases
   referenciadas existen. **Trabajo: 0 archivos nuevos
   necesarios desde el punto de vista de "clase faltante".**

**Pendiente verificacion mas profunda:**

- ¿Tienen las clases existentes los atributos y metodos que
  los UCs requieren? Esta es la pregunta de "completar
  clase existente" del scope original. Requiere extraer
  refs `attribute`/`method` de las RST de casos-uso/UML y
  cotejar con las clases. **Estimacion: 1-2 horas de
  analisis mecanico para cuantificar; ediciones si hay gaps.**

### Total estimado

- Tareas confirmadas: **3-15 ediciones** (mejores casos).
- Tareas dependientes de decisiones: **3-45 archivos** segun
  ruta A vs B para uc-usr-05/06/07.
- Tarea "completeness de atributos/metodos": **scope
  desconocido hasta hacer Phase 2 measure**.

**WP size estimado:** pequeño-mediano dependiendo de:
- Decision del ejecutor sobre uc-usr-05/06/07.
- Hallazgos de la verificacion mas profunda de
  completeness de atributos/metodos en domain-model.

## Decisiones pendientes (D-XX)

- **D1**: ruta A o B para uc-usr-05/06/07. Pendiente del
  ejecutor.
- **D2**: scope de la verificacion uml-07 — superficial
  (elementos presentes, ya verificado) vs profunda (orden
  iniciador→beneficiario, naming convention de actores,
  relaciones include/extend correctas).
- **D3**: scope de completeness domain-model — verificar
  atributos/metodos referenciados por UCs vs definidos en
  clases.

## Stopping points

- **SP-01:** revisar este DISCOVER antes de avanzar a
  Phase 2 MEASURE.
- **SP-02:** decidir D1/D2/D3 antes de ejecutar.

## Refs

- WP `cnst-033-uml-conformance` (precedente — origen del
  refactor de domain-model y view-case files).
- uml-07 normative reference:
  `source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/`.

## Artefactos discover

- `discover/uc-ids-casos-uso.txt` — 88 UC IDs.
- `discover/view-ids.txt` — 89 stems (88 UCs + 1 index).
- `discover/refs-from-view.txt` — 86 clases referenciadas
  desde use-case-view.
- `discover/refs-from-casos-uso.txt` — 77 clases referenciadas
  desde casos-uso.
- `discover/domain-model-existing.txt` — 109 archivos
  domain-model existentes.
- `discover/casos-uso-missing-diagram.txt` — 3 UCs.
- `discover/casos-uso-missing-diagrams-index.txt` — 3 UCs.
- `discover/view-no-system-boundary.txt` — 0 archivos.
- `discover/view-no-actor.txt` — 0 archivos.
- `discover/view-no-usecase.txt` — 0 archivos.
- `discover/view-thin.txt` — 0 archivos <30 lineas.
