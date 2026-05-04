```yml
created_at: 2026-05-04 08:36:33
project: IACT-docs
work_package: 2026-05-04-08-32-37-estructura-requisitos-arq-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
```

# Discover — Auditoría de Estructura: source/requisitos/* y source/arquitectura-tecnica/*

## Contexto del análisis

El usuario indica que `source/arquitectura-tecnica/` debería contener
**únicamente** diseño UML, diagramas y flujos. Actualmente contiene además
contenido textual (catálogos, responsabilidades, definiciones conceptuales).

El punto de partida del usuario fue comparar el tipo de contenido de
`source/base-cognitiva/_fundamentos-conceptuales/` y
`source/base-cognitiva/_uml/uml-06-introduccion-casos-uso/` — no como
archivos a mover, sino como **referencia del tipo de contenido** que corresponde
a `requisitos/` vs. el tipo que corresponde a `arquitectura-tecnica/`.

Ejemplos citados explícitamente para análisis:
- `source/requisitos/business-requirements/*`
- `source/arquitectura-tecnica/rbac/*`

---

## 1. Inventario general — tamaños verificados

| Directorio | Archivos RST | Notas |
|---|---|---|
| `source/requisitos/` | 1927 | Incluye _metodologia-aplicacion (extenso) |
| `source/arquitectura-tecnica/` | 815 | Ver breakdown por subdirectorio abajo |
| `source/base-cognitiva/_fundamentos-conceptuales/` | 8 | Referencia de tipo de contenido |
| `source/base-cognitiva/_uml/uml-06-introduccion-casos-uso/` | 5 | Referencia de tipo de contenido |

Cifras verificadas con `find | wc -l`.

---

## 2. Taxonomía de contenido — tres tipos, no dos

El análisis revela que existe **un tercer tipo** de contenido, no cubierto
por la dicotomía "requisitos / diagramas". Esto es fundamental para el diseño
de la solución:

| Tipo | Definición | Ejemplos actuales |
|---|---|---|
| **REQ** — Requisito | QUÉ debe hacer el sistema (nivel BR/BReq/UC/FR/RNF) | `requisitos/business-requirements/`, `requisitos/casos-uso/` |
| **DIAG** — Diagrama/UML | Representación visual: `.. uml::` con PlantUML | `arquitectura-tecnica/use-case-view/`, `deploy-view/`, `design-view/` |
| **ARCH** — Especificación arquitectónica | Catálogos, responsabilidades, componentes, modelo RBAC textual | `arquitectura-tecnica/rbac/modelo-rbac-iact/`, `modulos/*/responsabilidades.rst` |

La pregunta central del WP es: ¿dónde vive el tipo **ARCH**?

---

## 3. source/requisitos/business-requirements/* — análisis

**Ubicación actual:** `source/requisitos/business-requirements/`
**Archivos:** 9 (BReq-001 a BReq-008 + index.rst)

**Tipo de contenido:** REQ — Business Requirements (nivel 2 de ADR-GOB-003).
Cada archivo describe un objetivo de negocio de alto nivel que el sistema
debe satisfacer.

**Veredicto:** CORRECTAMENTE UBICADO.

`business-requirements/` es el directorio canónico para BReq per ADR-GOB-003,
que define la jerarquía de 5 niveles:
```
Level 1: BR   → reglas-negocio/
Level 2: BReq → business-requirements/      ← aquí
Level 3: UC   → casos-uso/
Level 4: FR   → requisitos-funcionales/
Level 5: RNF  → requisitos-no-funcionales/
```

No hay problema de ubicación en este directorio.

---

## 4. source/arquitectura-tecnica/rbac/* — análisis

**Directorio:** `source/arquitectura-tecnica/rbac/`
**Estructura:**
```
rbac/
├── modelo-rbac-iact/      ← 10 archivos textuales + diagramas/
│   ├── catalogo-funciones.rst  (708 líneas — 73 funciones RBAC)
│   ├── sod.rst                 (106 líneas — 3 restricciones SoD)
│   ├── grupos-funciones.rst    (349 líneas — definición de AGRs)
│   ├── mapeo-uc.rst            (186 líneas — función→UC mapping)
│   ├── filosofia.rst           (43 líneas)
│   ├── implementacion.rst      (183 líneas)
│   ├── resumen.rst             (124 líneas)
│   ├── permisos-temporales.rst (46 líneas)
│   ├── modelo-datos.rst        (23 líneas)
│   ├── arquitectura.rst        (82 líneas)
│   └── diagramas/              (3 archivos: clases, flujo, ciclo-vida) ← DIAG ✓
└── raci-rbac-iact/        ← 7 archivos: tablas RACI de responsabilidades
```

**17 archivos textuales no-diagrama** dentro de `arquitectura-tecnica/rbac/`.

**Clasificación por tipo:**

| Archivo | Tipo real | ¿Correcto en arq-tecnica? |
|---|---|---|
| `catalogo-funciones.rst` | ARCH — catálogo de las 73 funciones del sistema | Ambiguo |
| `sod.rst` | ARCH — definición de las 3 reglas SoD | Ambiguo |
| `grupos-funciones.rst` | ARCH — definición de AGRs (9 grupos de agrupadores) | Ambiguo |
| `mapeo-uc.rst` | ARCH — función → UC mapping | Ambiguo |
| `filosofia.rst` | ARCH — conceptual, principios de diseño | Ambiguo |
| `implementacion.rst` | ARCH — decisiones de implementación | Sí (es arquitectura) |
| `resumen.rst` | ARCH — síntesis del modelo | Sí (es arquitectura) |
| `permisos-temporales.rst` | ARCH — diseño de permisos temporales | Sí (es arquitectura) |
| `modelo-datos.rst` | ARCH — entidades de datos | Sí (es arquitectura) |
| `arquitectura.rst` | ARCH — decisiones técnicas RBAC | Sí (es arquitectura) |
| `diagramas/` (3 archivos) | DIAG — UML real con `.. uml::` | ✓ Correcto |
| `raci-rbac-iact/*` | ARCH — tablas RACI de responsabilidades | Ambiguo |

**Hallazgo principal sobre `rbac/modelo-rbac-iact/`:**

Los archivos textuales son especificaciones arquitectónicas del modelo RBAC —
definen QUÉ funciones existen, QUÉ grupos existen, QUÉ reglas SoD existen.
No son diagramas, pero tampoco son "requisitos" en el sentido de ADR-GOB-003
(no son BR, BReq, UC, FR, ni RNF).

Son el **modelo de dominio RBAC textual** que fundamenta los UC specs de
`requisitos/casos-uso/access/`, `requisitos/casos-uso/permissions/`, etc.

**Impacto de cualquier movimiento:** 38 referencias cruzadas desde fuera de
`arquitectura-tecnica/` apuntan a `arquitectura-tecnica/rbac/`. Mover estos
archivos rompería 38 `:doc:` en la documentación.

---

## 5. Breakdown de source/arquitectura-tecnica/ por tipo

### 5.1 Contenido claramente DIAG (UML puro)

| Subdirectorio | Archivos | Descripción |
|---|---|---|
| `use-case-view/` | 80 | Un diagrama UC por UC del sistema |
| `deploy-view/` | 80 | Un diagrama de despliegue por UC |
| `design-view/` | 160 | Diagramas de secuencia y comunicación |
| `uml-system-view/` | 9 | Diagramas de sistema (clases, componentes, etc.) |
| `bounded-contexts/*/` | ~10 | Bounded contexts con `.. uml::` de dominio |
| `modulos/*/diagramas/` | 30 | Diagramas de componentes/secuencia por módulo |
| `rbac/modelo-rbac-iact/diagramas/` | 3 | Clases, flujo enforcement, ciclo vida |
| `arquitectura-sistema/` | 3 | DFD nivel 0 y nivel 1 |

**Total DIAG:** ~375 archivos de diagrama puro.

### 5.2 Contenido claramente ARCH (textual, no diagrama)

| Subdirectorio | Archivos | Descripción |
|---|---|---|
| `modulos/*/responsabilidades.rst` | 10 | Tablas de responsabilidades por módulo |
| `modulos/*/casos-uso.rst` | 10 | Catálogos UC por módulo (texto + tabla) |
| `modulos/*/componentes.rst` | 10 | Componentes técnicos por módulo |
| `modulos/*/dependencias.rst` | 10 | Dependencias entre módulos |
| `modulos/*/restricciones.rst` | 10 | Restricciones por módulo |
| `modulos/*/metricas.rst` (sys-logs) | 1 | Métricas de logging |
| `modulos/rbac-core/enforcers.rst` | 1 | Descripción de enforcers RBAC |
| `rbac/modelo-rbac-iact/*.rst` (textual) | 10 | Catálogo, SoD, grupos, mapeo, etc. |
| `rbac/raci-rbac-iact/` | 7 | Tablas RACI |
| `vistas-kruchten.rst` | 1 | Descripción de las vistas 4+1 |
| `matriz-dependencias-uc-iact.rst` | 1 | Matriz de dependencias |
| `modelo-dominio-iact.rst` | 1 | Descripción del modelo de dominio |

**Total ARCH textual puro:** ~72 archivos.

### 5.3 Contenido MIXED (texto + diagrama en el mismo archivo)

| Subdirectorio | Archivos | Descripción |
|---|---|---|
| `uc-module-view/mod-*.rst` | 14 | Contexto textual + `.. uml::` UC por módulo |
| `bounded-contexts/*.rst` | ~9 | Descripción del contexto + `.. uml::` |
| `process-view/` | variable | Vistas de proceso |
| `implementation-view/` | variable | Vistas de implementación |
| `domain-model/` | variable | Modelo de dominio |
| `diagramas-uc-por-modulo.rst` | 1 | Índice con toctree + prefacio textual |
| `diagramas-uml-sistema.rst` | 1 | Índice con descripción de actores |
| `arquitectura-sistema.rst` | 1 | Descripción de arquitectura general |

**Total MIXED:** ~30 archivos.

---

## 6. Casos específicos que requieren decisión

### 6.1 `modulos/*/casos-uso.rst` — UC catalogs en arquitectura-tecnica

Estos archivos listan los UCs asociados a cada módulo con tabla
(UC ID, nombre, descripción). NO son UML. Son documentación arquitectónica
de qué UCs "pertenecen" a cada módulo.

**Tensión:** El nombre del directorio es `arquitectura-tecnica/modulos/` pero
el tipo es ARCH textual, no DIAG.

**Riesgo de mover:** Cada `casos-uso.rst` contiene referencias cruzadas a
`/requisitos/casos-uso/{dominio}/index`. Si se mueven, los índices de cada
módulo en `arquitectura-tecnica/` quedan con toctree incompleto.

### 6.2 `rbac/modelo-rbac-iact/catalogo-funciones.rst` (708 líneas)

Contiene el catálogo completo de las 73 funciones del sistema RBAC con:
- función, capability, UC relacionado, descripción
- organizadas por módulo

Este archivo es el catálogo maestro que alimenta:
- Los UC specs de `requisitos/casos-uso/access/` (actor management)
- Los specs de `requisitos/casos-uso/admin/` (ADM_01, ADM_02, ADM_03)
- Los `modulos/*/responsabilidades.rst`

**Pregunta de diseño:** ¿Es un artefacto arquitectónico (define QUÉ funciones
existen → ARCH) o es un requisito funcional (especifica las funciones del
sistema → podría ser FR o Nivel 1 en la jerarquía)?

### 6.3 `uc-module-view/mod-*.rst` — mixed content

Cada archivo de `uc-module-view/` sigue este patrón:
```rst
[texto introductorio del módulo — 10-20 líneas]

.. uml::
   :caption: Figura N — MOD_X: casos de uso
   @startuml
   [diagrama UC]
   @enduml
```

El texto introductorio (diferencia entre módulos, actor principal) no es
un diagrama. Pero separarlo del diagrama rompería la coherencia del documento.

---

## 7. Evaluación de source/requisitos/_metodologia-aplicacion/

Este directorio (parte de `source/requisitos/`) merece mención especial.
Contiene 17 sub-secciones de metodología aplicada al dominio IACT:
- `casos-uso-diagramas/` — diagramas UML de casos de uso IACT (DIAG en requisitos)
- `analisis-dominio/` — ERD y clases de dominio (DIAG en requisitos)
- `diagramas-actividades/` — diagramas de actividad (DIAG en requisitos)
- `agregacion-interfaces/` — diagramas de agregación (DIAG en requisitos)
- `casos-uso-especificacion/` — especificación de UC (REQ)
- `diagramas-colaboraciones/` — diagramas de comunicación (DIAG en requisitos)

**Observación:** `requisitos/_metodologia-aplicacion/` ya contiene diagramas
UML aplicados al dominio IACT. Esto muestra que la línea "solo requisitos/
solo diagramas en arquitectura-tecnica" no es tan absoluta en el árbol actual.
La metodología aplicada (con sus UML) vive en `requisitos/`.

---

## 8. Comparación con lo que "debería ser" según el usuario

El usuario indica:
- `requisitos/` → tipo de contenido de `_fundamentos-conceptuales/` y `uml-06-*`
- `arquitectura-tecnica/` → solo diseño UML, diagramas, flujos

Tomando esa guía:

| Contenido actual | Tipo real | Posición per visión del usuario |
|---|---|---|
| `requisitos/business-requirements/*` | REQ | ✓ Correcto |
| `requisitos/casos-uso/*` | REQ | ✓ Correcto |
| `requisitos/requisitos-funcionales/*` | REQ | ✓ Correcto |
| `requisitos/reglas-negocio/*` | REQ | ✓ Correcto |
| `requisitos/_metodologia-aplicacion/*` | REQ + DIAG mezclado | Aceptable — metodología aplicada |
| `arquitectura-tecnica/use-case-view/*` | DIAG puro | ✓ Correcto |
| `arquitectura-tecnica/deploy-view/*` | DIAG puro | ✓ Correcto |
| `arquitectura-tecnica/design-view/*` | DIAG puro | ✓ Correcto |
| `arquitectura-tecnica/uml-system-view/*` | DIAG puro | ✓ Correcto |
| `arquitectura-tecnica/modulos/*/diagramas/*` | DIAG puro | ✓ Correcto |
| `arquitectura-tecnica/modulos/*/responsabilidades.rst` | ARCH textual | ⚠ No es diagrama |
| `arquitectura-tecnica/modulos/*/casos-uso.rst` | ARCH textual | ⚠ No es diagrama |
| `arquitectura-tecnica/modulos/*/componentes.rst` | ARCH textual | ⚠ No es diagrama |
| `arquitectura-tecnica/rbac/modelo-rbac-iact/*.rst` (textual) | ARCH textual | ⚠ No es diagrama |
| `arquitectura-tecnica/rbac/raci-rbac-iact/*` | ARCH textual | ⚠ No es diagrama |
| `arquitectura-tecnica/uc-module-view/mod-*.rst` | MIXED | ⚠ Texto + diagrama mezclado |
| `arquitectura-tecnica/bounded-contexts/*.rst` | MIXED | ⚠ Texto + diagrama mezclado |

---

## 9. Hallazgos prioritarios

### H-01 — ARCH textual masivo en arquitectura-tecnica [ALTA]
72 archivos textuales (no-diagrama) viven en `arquitectura-tecnica/`, incluyendo:
- Catálogo de 73 funciones RBAC (708 líneas)
- Definiciones de SoD, grupos de funciones
- Responsabilidades de 10 módulos
- Tablas RACI

Ninguno de estos es un diagrama UML. Contradicen la visión del usuario.

### H-02 — Tercer tipo: ARCH no tiene hogar claro [CRÍTICO]
El contenido tipo ARCH (especificaciones arquitectónicas textuales) no encaja
ni en REQ (no es un requisito BR/BReq/UC/FR/RNF) ni en DIAG (no es visual).
Cualquier solución debe definir primero dónde vive ARCH.

**Opciones posibles (no decisión — análisis):**
1. ARCH como subnivel de `requisitos/` → `requisitos/arquitectura/rbac/`
2. ARCH permanece en `arquitectura-tecnica/` como excepción documentada
3. Nuevo nivel `source/modelo-dominio/` separado de ambos
4. ARCH embebido en los UC specs de `requisitos/casos-uso/`

### H-03 — 38 referencias cruzadas a rbac/ desde fuera de arquitectura-tecnica [ALTA]
Cualquier movimiento de `arquitectura-tecnica/rbac/` rompe 38 `:doc:` en
otros archivos. Requiere actualización sistemática de links.

### H-04 — Contenido MIXED en uc-module-view y bounded-contexts [MEDIA]
14 archivos en `uc-module-view/` y ~9 en `bounded-contexts/` mezclan texto
introductorio con `.. uml::`. Si el estándar es "solo diagramas en arq-tecnica",
estos archivos requieren decisión: ¿separar texto de diagrama, o aceptar mixed?

### H-05 — source/requisitos/business-requirements/* — sin problema [BAJA]
Ubicación correcta per ADR-GOB-003. No requiere acción.

### H-06 — _metodologia-aplicacion en requisitos contiene diagramas UML [INFORMATIVO]
Prueba que la separación estricta "requisitos=solo texto, arq=solo UML" no
aplica al árbol actual. La metodología aplicada (con sus diagramas IACT) vive
en `requisitos/`. Esto puede ser intencional o accidental — requiere decisión.

---

## 9b. Hallazgos adicionales — domain-model/ y rbac/ confirmados

### H-07 — domain-model/ contiene diagramas UC-por-UC, no el modelo global [ALTA]

`arquitectura-tecnica/domain-model/` tiene **160 archivos** (verificado):
- 80 `{uc-name}-domain-model.rst` — diagrama de clases por UC individual
- 80 `{uc-name}-estado.rst` — máquina de estado por UC individual

**Problema 1 — Mal nombrado:** El directorio se llama "domain model" pero no contiene
el modelo de dominio del sistema. Contiene 80 fragmentos de clase UC-específicos.
El modelo de dominio global (sistema completo) vive en `bounded-contexts/` (UML parcial
por bounded context) y en `modelo-dominio-iact.rst` (descripción textual).

**Problema 2 — Duplicación:** Los UC specs en `requisitos/casos-uso/` ya contienen
sus propias máquinas de estado en `diagramas-uml/`:
- `uc-auth-01/diagramas-uml/diagrama-de-estados-de-session.rst` — ya existe
- `uc-alr-01/diagramas-uml/estado-de-la-regla.rst` — ya existe
- `uc-adm-01/diagramas-uml/estado-sod-rule.rst` — ya existe

Los `{uc}-estado.rst` de `domain-model/` duplican diagramas que ya viven
(o deben vivir) dentro de cada UC spec.

**Lo que debería ir en `domain-model/`:** El modelo de dominio global del sistema —
uno o pocos diagramas de clases de alto nivel con todas las entidades principales
y sus relaciones, a nivel de sistema o de bounded context. No 160 fragmentos UC-por-UC.

**Destino correcto de los 160 archivos actuales:**
- `{uc}-estado.rst` → dentro de `requisitos/casos-uso/{dominio}/{uc}/diagramas-uml/`
  (donde ya existe o debe existir el state machine del UC)
- `{uc}-domain-model.rst` → dentro de `requisitos/casos-uso/{dominio}/{uc}/diagramas-uml/`
  o en `design-view/` (vista de diseño por UC)

### H-08 — arquitectura-tecnica/rbac/ textual pertenece en requisitos/ [ALTA]

Confirmado: si `arquitectura-tecnica/` es exclusivamente para diseño UML/diagramas,
el contenido textual de `rbac/modelo-rbac-iact/` no pertenece ahí.

Clasificación del contenido de `rbac/modelo-rbac-iact/` (10 archivos textuales):

| Archivo | Tipo real | Destino correcto |
|---|---|---|
| `catalogo-funciones.rst` (708 líneas) | BR — define QUÉ 73 funciones existen | `requisitos/reglas-negocio/` |
| `sod.rst` (106 líneas) | BR — define las 3 reglas SoD del sistema | `requisitos/reglas-negocio/` |
| `grupos-funciones.rst` (349 líneas) | BR — define los 9 AGRs del sistema | `requisitos/reglas-negocio/` |
| `mapeo-uc.rst` (186 líneas) | Trazabilidad función→UC (ADR-GOB-007) | `requisitos/` (sección trazabilidad) |
| `filosofia.rst` (43 líneas) | Conceptual — principios del modelo | `normativa/` o `base-cognitiva/` |
| `implementacion.rst` (183 líneas) | Decisiones de diseño técnico | ARCH — podría quedarse si se acepta ARCH en arq-tecnica |
| `arquitectura.rst` (82 líneas) | Decisiones técnicas RBAC | ARCH — ídem |
| `resumen.rst` (124 líneas) | Síntesis del modelo | ARCH — ídem |
| `permisos-temporales.rst` (46 líneas) | Diseño de permisos temporales | ARCH — ídem |
| `modelo-datos.rst` (23 líneas) | Entidades de datos | ARCH — ídem |

`rbac/raci-rbac-iact/` (7 archivos) — tablas RACI: gobernanza, no diseño técnico.
Destino correcto: `normativa/gobernanza/` o directorio de gestión del proyecto.

`rbac/modelo-rbac-iact/diagramas/` (3 archivos) — UML puro: correcto en
`arquitectura-tecnica/`.

**Impacto de mover el contenido textual:** 38 referencias cruzadas desde fuera
de `arquitectura-tecnica/` apuntan a `arquitectura-tecnica/rbac/`. Requiere
actualización sistemática de todos los `:doc:` afectados.

---

## 10. Preguntas de diseño para la fase STRATEGY

Antes de planificar cualquier reorganización, estas preguntas deben responderse:

**P-01:** ¿El contenido tipo ARCH (catálogos, responsabilidades, RACI) debe
vivir en `arquitectura-tecnica/` como un subnivel aceptado, o debe tener un
directorio propio?

**P-02:** ¿Los archivos MIXED (texto + `.. uml::`) en `uc-module-view/` son
válidos tal como están, o se prefiere separar el texto (→ algún otro lugar)
del diagrama (→ `arquitectura-tecnica/`)?

**P-03:** ¿`_metodologia-aplicacion/` con sus diagramas UML de ejemplo IACT
pertenece a `requisitos/`, o debería cruzar a `arquitectura-tecnica/`?

**P-04:** ¿El catálogo de funciones RBAC (`catalogo-funciones.rst`) es un
artefacto de requisitos (define funcionalidad requerida) o de arquitectura
(define la implementación del modelo RBAC)? Su ubicación depende de esto.

---

## 11. Resumen ejecutivo

| Área | Estado | Acción requerida |
|---|---|---|
| `requisitos/business-requirements/` | ✓ Correcto | Ninguna |
| `requisitos/casos-uso/` | ✓ Correcto | Ninguna |
| `requisitos/requisitos-funcionales/` | ✓ Correcto | Ninguna |
| `arquitectura-tecnica/use-case-view/` | ✓ Correcto (DIAG puro) | Ninguna |
| `arquitectura-tecnica/deploy-view/` | ✓ Correcto (DIAG puro) | Ninguna |
| `arquitectura-tecnica/design-view/` | ✓ Correcto (DIAG puro) | Ninguna |
| `arquitectura-tecnica/modulos/*/responsabilidades.rst` | ⚠ ARCH textual en zona DIAG | Decisión pendiente P-01 |
| `arquitectura-tecnica/modulos/*/casos-uso.rst` | ⚠ ARCH textual en zona DIAG | Decisión pendiente P-01 |
| `arquitectura-tecnica/rbac/modelo-rbac-iact/*.rst` | ⚠ ARCH textual en zona DIAG | Decisión pendiente P-01 y P-04 |
| `arquitectura-tecnica/rbac/raci-rbac-iact/` | ⚠ ARCH textual en zona DIAG | Decisión pendiente P-01 |
| `arquitectura-tecnica/uc-module-view/mod-*.rst` | ⚠ MIXED en zona DIAG | Decisión pendiente P-02 |
| `arquitectura-tecnica/bounded-contexts/*.rst` | ⚠ MIXED en zona DIAG | Decisión pendiente P-02 |
| `requisitos/_metodologia-aplicacion/` | ⚠ DIAG dentro de requisitos | Decisión pendiente P-03 |
| `arquitectura-tecnica/domain-model/` (160 archivos) | ⚠ Diagramas UC-por-UC mal ubicados; duplican UC specs | Mover a UC specs; reemplazar con modelo global (H-07) |
| `arquitectura-tecnica/rbac/modelo-rbac-iact/*.rst` (textual) | ⚠ BR/trazabilidad en zona DIAG | Mover a `requisitos/reglas-negocio/` (H-08) |
| `arquitectura-tecnica/rbac/raci-rbac-iact/` | ⚠ Gobernanza en zona DIAG | Mover a `normativa/gobernanza/` (H-08) |
| `arquitectura-tecnica/rbac/modelo-rbac-iact/diagramas/` | ✓ DIAG puro | Correcto |
