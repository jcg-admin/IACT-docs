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

## 9c. Hallazgos adicionales — bounded-contexts y deploy-view

### H-09 — bounded-contexts/ es el verdadero domain model — consolidar [MEDIA]

`arquitectura-tecnica/bounded-contexts/` contiene 10 archivos (1157 líneas):
- `overview.rst` (237 líneas) — modelo canónico global: 25 clases en 7 BCs, método Abbott + IEEE 830
- `bounded-context-{auth,rbac,calls,reports,pipeline-etl,alerts,audit,logs}.rst` — diagrama de clases `.. uml::` por BC

Este contenido ES el modelo de dominio global del sistema — exactamente lo que
`domain-model/` debería contener per H-07. El `:tipo:` declarado en los metadatos
de cada archivo es `Diagrama Arquitectonico — Modelo de Dominio`.

**Propuesta confirmada:** mover `bounded-contexts/` → `domain-model/` y eliminar
el directorio `bounded-contexts/` una vez consolidado.

**Impacto del move (verificado):**
- Referencias externas a `bounded-contexts/` desde fuera de `arquitectura-tecnica/`: **0**
- Referencias internas: **1 sola** — `modelo-dominio-iact.rst` tiene un toctree
  apuntando a `bounded-contexts/overview` y los 8 `bounded-context-*.rst`
- Archivos a actualizar: únicamente `modelo-dominio-iact.rst` (cambiar paths en toctree)

**Estructura resultante de `domain-model/` post-merge:**
```
domain-model/
├── overview.rst                     ← modelo canónico global (25 clases)
├── bounded-context-auth.rst         ← clases BC Auth
├── bounded-context-rbac.rst         ← clases BC RBAC
├── bounded-context-alerts.rst
├── bounded-context-audit.rst
├── bounded-context-calls.rst
├── bounded-context-logs.rst
├── bounded-context-pipeline-etl.rst
├── bounded-context-reports.rst
└── index.rst                        ← actualizar descripción y toctree
```

Los 160 archivos per-UC actualmente en `domain-model/` (H-07) se tratan en
tarea separada — relocalizarlos a los UC specs correspondientes.

### H-10 — deploy-view/ tiene 71 de 80 diagramas idénticos [ALTA]

Verificación por hash MD5 del bloque `@startuml..@enduml` de los 80 archivos:

| Hash | Cantidad | Variante | Archivos representativos |
|---|---|---|---|
| `7307cd15` | **71** | Genérico: Client→WebServer(App)→DB | La gran mayoría |
| `74e2c793` | **5** | Con cache: + node "cache" | `iniciar-sesion`, `cerrar-sesion`, `gestionar-sesiones`, `cambiar-contrasena`, `recuperar-contrasena` |
| `3200ac7f` | **4** | ETL: WebServer(DisparadorETL)→DB vía SP call | `supervisar-etl`, `solicitar-reintento-pipeline`, `consultar-errores-etl`, `consultar-disponibilidad-datos` |

**Conclusión:** `deploy-view/` tiene **3 diagramas únicos reales** embebidos en
80 archivos. Los 71 archivos con hash `7307cd15` son la misma línea
`Client → WebServer → DB` copiada 71 veces. No aportan información de deployment
diferenciada por UC.

**Lo correcto:** 3 diagramas de deployment (uno por variante de infraestructura)
en lugar de 80 copias. La vista de deployment real de IACT no varía por UC —
varía por tipo de componente de backend (app estándar, app con cache, disparador ETL).

**Acción requerida:**
1. Crear 3 diagramas canónicos de deployment (estándar, auth-cache, etl)
2. Eliminar los 80 archivos per-UC redundantes
3. Reemplazar el `deploy-view/index.rst` actual con un índice de 3 entradas

### H-11 — design-view/ tiene 160 archivos de boilerplate genérico [ALTA]

`arquitectura-tecnica/design-view/` contiene **161 archivos**:
- 80 `{uc-name}-secuencia.rst` — diagramas de secuencia por UC
- 80 `{uc-name}-comunicacion.rst` — diagramas de comunicación entre objetos por UC
- 1 `index.rst`

**Hallazgo 1 — Duplicados exactos por hash MD5 (40 archivos):**

| Cantidad | Tipo | UCs afectadas |
|---|---|---|
| 9 | `*-comunicacion.rst` | 9 UCs de reportes (ver-reportes-historicos, ver-reportes-programados, reporte-agentes, reporte-campanas, reporte-colas, reporte-clientes-unicos, reporte-menus-ivr, reporte-transferencias, resolver-segmento) |
| 9 | `*-secuencia.rst` | Mismos 9 UCs de reportes |
| 5 | `*-comunicacion.rst` | 5 UCs de llamadas (iniciar-llamada, esperar-cola, navegar-ivr, calificar, solicitar-callback) |
| 5 | `*-secuencia.rst` | Mismos 5 UCs de llamadas |
| 6 pares | ambos tipos | 6 pares adicionales |

**Hallazgo 2 — Los 120 "únicos" por hash son boilerplate con sustitución de nombres:**

Los 4 pasos del flujo de secuencia aparecen **exactamente 80 veces cada uno**
(verificado por grep sobre todos los archivos):

```
Iface -> SvcNode : POST/GET endpoint     ← presente en 80/80 archivos
SvcNode -> Store : query / SP            ← presente en 80/80 archivos
Store --> SvcNode : resultado            ← presente en 80/80 archivos
SvcNode --> Iface : respuesta JSON       ← presente en 80/80 archivos
```

La única variación entre archivos es el nombre del actor (función RBAC) y la
etiqueta de módulo del servicio (12 variantes: "Interfaz de Acceso", "Interfaz de
Reportes", etc.). El flujo lógico es idéntico en los 160 archivos.

Los "hash únicos" lo son solo porque el actor name cambia el hash — no porque
el diagrama represente un diseño diferente.

**Conclusión:** `design-view/` padece el mismo problema que `deploy-view/`:
160 copias de un template genérico `actor → frontend → api → db` que no describe
el diseño técnico específico de ningún UC. Los UC specs en
`requisitos/casos-uso/*/diagramas-uml/` ya contienen los diagramas de flujo
específicos (flujo-principal, actividad, secuencia con pasos concretos).

**Acción correcta:**
1. Reducir a ~12 diagramas canónicos por módulo (Auth, Access, Permissions,
   Admin, Reports, ETL, Alerts, Audit, Logs, Calls, Supervision, Users)
2. Cada diagrama canónico muestra el patrón de interacción del módulo
3. Eliminar los 160 archivos per-UC redundantes

### H-12 — implementation-view/ tiene 80 archivos para 12 diagramas únicos [ALTA]

`arquitectura-tecnica/implementation-view/` contiene **81 archivos** (80 UCs + index).

**Resultado del análisis por hash MD5:** 12 hashes únicos — exactamente 1 por módulo.
Todos los UCs del mismo módulo comparten el mismo diagrama idéntico.

| Módulo | Archivos UC | Diagrama único |
|---|---|---|
| MOD_Reports | 16 | 1 |
| MOD_Calls / Operator | 10 | 1 |
| MOD_Permissions | 10 | 1 |
| MOD_Access | 7 | 1 |
| MOD_Logs | 7 | 1 |
| MOD_Auth | 5 | 1 |
| MOD_Alerts | 5 | 1 |
| MOD_Caller | 5 | 1 |
| MOD_Users | 4 | 1 |
| MOD_Audit | 4 | 1 |
| MOD_Pipeline | 4 | 1 |
| MOD_Supervision | 3 | 1 |

**Total verificado:** 68/80 archivos son redundantes (mismo diagrama del módulo repetido).

**Diferencia clave vs. deploy-view y design-view:** el agrupamiento es semánticamente
correcto — la vista de implementación ES por módulo, no por UC. El diagrama
`package "MOD_X" { View/Serializer → Service/Repository → ORM/SP }` describe
correctamente la estructura de implementación de cada módulo.

El problema es únicamente la multiplicación innecesaria: 80 archivos UC-indexados
para 12 diagramas de módulo.

**Solución correcta:** 12 archivos canónicos (uno por módulo), reemplazando los
80 per-UC. La estructura ya existe en `modulos/*/componentes.rst` — los diagramas
de `implementation-view/` podrían consolidarse allí o vivir como archivos
`implementation-view/mod-{nombre}.rst` (análogo a `uc-module-view/mod-{nombre}.rst`).

### H-13 — modulos/ mezcla diagramas únicos valiosos con especificaciones textuales ARCH [ALTA]

`arquitectura-tecnica/modulos/` tiene **11 módulos** con dos perfiles radicalmente distintos:

**Perfil A — Solo diagramas (correcto): `caller/`, `operator/`, `supervision/`**
Sin archivos textuales. Solo `diagramas/` con UML específico de dominio.
Estos 3 módulos son el modelo correcto per la visión del usuario.

**Perfil B — Diagramas + textuales (inconsistente): 8 módulos restantes**
`alerts/`, `audit/`, `auth/`, `etl-monitoring/`, `rbac-core/`, `sys-logs/`,
`user-identity/`, `vis-reports/` — cada uno con 5 archivos textuales estándar
más posibles especiales (`retencion`, `metricas`, `enforcers`).

**Los `diagramas/` (30 archivos) — todos únicos, CORRECTO:**
Hash MD5 verificado: 30 hashes únicos, cero duplicados. Son los mejores
diagramas de toda `arquitectura-tecnica/`: lógica de dominio real, específicos
por módulo (ciclo de vida, secuencias con reglas de negocio, diagramas de clases).
Deben quedarse donde están.

**Los archivos textuales (43 archivos) — tipo ARCH, fuera de lugar si arq-tecnica es solo DIAG:**

| Tipo | Contenido | Módulos | Observación |
|---|---|---|---|
| `responsabilidades.rst` (8) | PUEDE/NO PUEDE, UC, CNST | todos los B | Especificación de frontera de módulo |
| `componentes.rst` (8) | Apps, modelos, servicios Django | todos los B | Especificación de implementación |
| `dependencias.rst` (8) | Dependencias inter-módulo | todos los B | Topología del sistema |
| `restricciones.rst` (8) | CNST aplicables al módulo | todos los B | Derivado de `normativa/` — potencialmente redundante |
| `casos-uso.rst` (8) | Catálogo de UCs del módulo | todos los B | Info ya vive en `requisitos/casos-uso/` |
| `retencion.rst` (1) | Política de retención | audit | Podría ir en `normativa/` |
| `metricas.rst` (1) | Métricas de observabilidad | sys-logs | Específico técnico |
| `enforcers.rst` (1) | Middleware de enforcement | rbac-core | Decisión de implementación |

**Evidencia de que los textuales no son indispensables aquí:**
`caller/`, `operator/`, `supervision/` no tienen ningún archivo textual y su
documentación está completa solo con sus `diagramas/`. Esto prueba que los 43
archivos textuales de los otros 8 módulos no son obligatorios en esta ubicación.

**`casos-uso.rst` en particular es redundante:** cada archivo lista los UCs del
módulo en una tabla, pero esa misma información ya vive en `requisitos/casos-uso/`
con sus specs completas. Es duplicación de trazabilidad.

**Confirmado (verificado con find):** `requisitos/casos-uso/` ya tiene los 13
subdominios completos, incluyendo `admin/`:
```
access/, admin/, alerts/, audit/, auth/, caller/, logs/,
operator/, permissions/, pipeline/, reports/, supervision/, users/
```
Los 8 archivos `modulos/*/casos-uso.rst` son una tabla-resumen de UCs cuyo
contenido canónico ya existe en `requisitos/casos-uso/{dominio}/`. No añaden
información nueva — son redundancia de trazabilidad. T-042 confirmará caso por
caso antes de eliminar.

### H-14 — use-case-view/ y uc-module-view/ son redundantes: UC-indexado vs módulo-indexado [ALTA]

`arquitectura-tecnica/` tiene **dos directorios de Use Case View** con diferente
nivel de abstracción y propósito:

**`use-case-view/` (81 archivos — UC-indexado, BOILERPLATE):**

| Característica | Detalle |
|---|---|
| Archivos | 81 `.rst` (80 UCs + index) |
| Granularidad | Un archivo por UC — UC-indexado |
| Contenido por archivo | Actor → UC dentro de rectángulo módulo. Sin relaciones entre UCs. Sin `<<include>>`. Sin `<<extend>>`. |
| Texto introductorio | Ninguno (solo metadata + diagrama) |
| `:tipo:` | `Diagrama Arquitectonico — Use Case View` |
| Patrón | Boilerplate UC-individual — mismo problema que `deploy-view/`, `design-view/`, `implementation-view/` |

Ejemplo (`iniciar-sesion.rst`): `actor "Usuario" → usecase "UC_AUTH_01 Iniciar Sesion"
dentro de rectangle "MOD_Auth"`. Nada más. No muestra las otras 4 UCs de Auth,
no muestra `<<include>>` entre UCs, no muestra actores secundarios.

**`uc-module-view/` (15 archivos — módulo-indexado, CORRECTO):**

| Característica | Detalle |
|---|---|
| Archivos | 13 `mod-*.rst` + `index.rst` + `rbac-funciones-por-modulo.rst` |
| Granularidad | Un archivo por módulo — módulo-indexado |
| Contenido por archivo | TODOS los UCs del módulo con actores completos, relaciones `<<include>>`, contexto del módulo |
| Texto introductorio | 2-3 párrafos explicativos antes del diagrama |
| `:tipo:` | `Diagrama Arquitectonico — UC por Modulo` |
| Patrón | Nivel correcto per estándar 5+1 |

Ejemplo (`mod-auth.rst`): 5 UCs de Auth + 1 UC de Permissions, 3 actores distintos,
`UC_AUTH_01 <<include>> UC_AUTH_05`, contexto narrativo del módulo.

**Diagnóstico:**

`use-case-view/` fue la implementación original del Use Case View (estilo UC-indexado
generalizado). `uc-module-view/` fue creado después como la versión module-level.
Coexisten sin reemplazarse, creando dos representaciones del mismo view con
niveles de abstracción incompatibles.

La **Use Case View** del estándar 5+1 requiere mostrar:
- El conjunto de UCs de cada módulo
- Sus actores y relaciones
- Las dependencias entre UCs (`<<include>>`, `<<extend>>`)

`uc-module-view/` cumple esto. `use-case-view/` no.

**UCs cubiertos por módulo (verificado en `uc-module-view/`):**

| Módulo | UC refs | Módulo | UC refs |
|---|---|---|---|
| mod-access | 8 | mod-logs | 8 |
| mod-admin | 10 | mod-operator | 11 |
| mod-alerts | 7 | mod-permissions | 11 |
| mod-audit | 5 | mod-pipeline | 6 |
| mod-auth | 7 | mod-reports | 17 |
| mod-caller | 6 | mod-supervision | 4 |
| mod-users | 5 | **Total** | **~105** |

**Conclusión (corregida):** `use-case-view/` ES el directorio canónico del Use
Case View según el modelo 5+1 — su nombre es correcto, se mantiene. `uc-module-view/`
es el directorio redundante: contiene el mismo nivel de abstracción (módulo-indexado)
pero con un nombre no estándar. El contenido de `uc-module-view/` debe integrarse en
`use-case-view/` antes de eliminar `uc-module-view/`.

**Plan de integración antes de eliminar `uc-module-view/`:**

1. Los `mod-*.rst` de `uc-module-view/` → reemplazar (o crear) los archivos
   equivalentes en `use-case-view/` a nivel módulo (no UC-individual).
2. `rbac-funciones-por-modulo.rst` → evaluar si pertenece a `requisitos/rbac/` o
   `arquitectura-tecnica/rbac/`.
3. Los 81 archivos UC-individuales actuales de `use-case-view/` → sustituir por
   ~13 archivos módulo-indexados (mismo contenido que los `mod-*.rst`).
4. Eliminar `uc-module-view/` una vez que `use-case-view/` tenga el contenido
   módulo-indexado correcto.

---

## 10. Decisiones tomadas y preguntas resueltas

### D-01 — El estándar es el modelo 5+1 (variante DDD de Kruchten) [DECIDIDO]

El proyecto sigue el modelo de vistas arquitectónicas **5+1** — variante extendida
del modelo 4+1 de Kruchten que añade la Vista de Dominio, usada en contextos DDD:

| # | Vista | Directorio actual | Estado |
|---|---|---|---|
| 1 | **Domain Model** | `domain-model/` + `bounded-contexts/` | ⚠ consolidar (H-07, H-09) |
| 2 | **Design View** | `design-view/` | ⚠ nivel incorrecto (H-11) |
| 3 | **Implementation View** | `implementation-view/` | ⚠ nivel incorrecto (H-12) |
| 4 | **Use Case View** | `use-case-view/` ✓ + `uc-module-view/` ❌ | ⚠ duplicado — integrar `uc-module-view/` → `use-case-view/`, luego eliminar `uc-module-view/` (H-14) |
| 5 | **Process View** | `process-view/` | ⚠ diagramas mal clasificados per Rozanski (H-15) |
| +1 | **Deployment View** | `deploy-view/` | ⚠ nivel incorrecto (H-10) |

Las 6 vistas tienen prioridad sobre cualquier otra organización. **No se eliminan
— se corrigen al nivel de abstracción correcto (módulo, no UC individual).**

El problema transversal: todas las vistas están implementadas por UC individual
en lugar de por módulo o variante de infraestructura. La corrección:

| Vista | Nivel actual (incorrecto) | Nivel correcto | Archivos: actual → objetivo |
|---|---|---|---|
| Domain Model | 160 per-UC + 10 BC separados | sistema/BC | 170 → ~9 BC + overview |
| Use Case View | `use-case-view/` (81 per-UC) + `uc-module-view/` (15 por módulo) | por módulo | eliminar `use-case-view/`; `uc-module-view/` es el canónico (H-14) |
| Deploy View | 80 por UC | por variante de infra | 80 → 3 |
| Design View | 160 por UC | por módulo | 160 → ~12 |
| Implementation View | 80 por UC | por módulo | 80 → 12 |
| Process View | pendiente análisis | — | — |

`modulos/*/diagramas/` (comportamiento de módulo) y las 6 vistas 5+1 NO se
duplican: sirven propósitos distintos (comportamiento interno vs. perspectiva
arquitectónica cruzada).

### D-02 — modulos/ textual (ARCH) se queda en arquitectura-tecnica/modulos/ [DECIDIDO]

Los archivos `responsabilidades`, `componentes`, `dependencias`, `restricciones`,
`casos-uso` de cada módulo permanecen en `arquitectura-tecnica/modulos/{mod}/`.
Son especificaciones de módulo necesarias en ese contexto.

---

### H-15 — process-view/ contiene diagramas de flujo UC mal clasificados y carece del contenido real de Process View [ALTA]

**`process-view/` (81 archivos verificados con `find | wc -l`):**

| Característica | Detalle |
|---|---|
| Archivos | 81 `.rst` (80 UCs + index) |
| Granularidad | Un archivo por UC — UC-indexado |
| Patrón de diagrama | 5 pasos idénticos: `ValidarSolicitud → EjecutarOperacion → PersistirCambios → RegistrarAuditoria → RetornarRespuesta` |
| Variación entre archivos | Solo el nombre del actor (AGR_ADMIN, AGR_OPERADOR, etc.) |
| Tipo de contenido | Diagramas de actividades que modelan el flujo de ejecución de un UC |

**Diagnóstico de mala clasificación:**

Según el estándar 5+1 (variante DDD de Kruchten), la **Process View** modela:
- Concurrencia y paralelismo del sistema
- Sincronización entre procesos/hilos
- Comunicación inter-proceso
- Estructuras de procesos en tiempo de ejecución

Los diagramas actuales en `process-view/` modelan el **flujo de ejecución de un
UC individual** (validar → ejecutar → persistir → auditar → retornar). Eso es
comportamiento funcional — corresponde a la **Use Case View** per 5+1, no a la
Process View.

**Validación con Rozanski & Woods (base cognitiva UML-14):**

El viewpoint Concurrency de Rozanski (equivalente al Process View de Kruchten) aborda:
> "mapeo de elementos funcionales en unidades concurrentes, mecanismos de comunicación
> y sincronización, estructuras de procesos e hilos, comunicación inter-proceso"

Los diagramas actuales no modelan ninguno de estos aspectos.

**Estado del verdadero Process View:**

Una Process View correcta para IACT modelaría:
- Pipeline ETL concurrente (disparadores, colas, workers)
- Procesamiento paralelo de alertas
- Sincronización de sesiones JWT
- Concurrencia en consultas de dashboard de alto volumen

**Ninguno de estos diagramas existe actualmente.** La Process View real de IACT
está vacía.

**Doble problema:**
1. Los 81 archivos existentes están **mal clasificados** — son UC behavior, no Process View
2. El **contenido correcto de Process View** (concurrencia, paralelismo) **no existe**

---

## 10.1 Nota de metodología — Framework Rozanski como base de reestructuración

El análisis discover ha empleado el Framework de Rozanski & Woods
(*Software Systems Architecture*, 2ª ed.) como referencia para evaluar
el estado actual de `arquitectura-tecnica/`. Este framework — documentado
en `base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/` — provee:

1. Un catálogo de 7 viewpoints con definiciones canónicas (Context, Functional,
   Information, Concurrency, Development, Deployment, Operational)
2. Un meta-modelo formal de relaciones entre arquitectura, vistas, viewpoints,
   concerns y stakeholders
3. Tablas de importancia de viewpoints por tipo de sistema

**Aplicación a IACT:**

| Rozanski Viewpoint | 5+1 IACT actual | Estado |
|---|---|---|
| Context | — | Ausente (ningún directorio modela el contexto del sistema) |
| Functional | `use-case-view/` | ⚠ Boilerplate UC-individual (H-14) |
| Information | `domain-model/` (parcial) | ⚠ Confundido con diagramas UC-por-UC (H-07) |
| Concurrency | `process-view/` | ⚠ Mal clasificado — diagramas de flujo UC, no concurrencia (H-15) |
| Development | `design-view/` + `implementation-view/` | ⚠ Boilerplate UC-individual (H-11, H-12) |
| Deployment | `deploy-view/` | ⚠ 71/80 copias idénticas (H-10) |
| Operational | — | Ausente — ningún viewpoint operacional existe |

La fase STRATEGY usará este mapeo Rozanski ↔ 5+1 como framework de decisión para
la reestructuración de `arquitectura-tecnica/`.

---

## 11. Preguntas de diseño pendientes para la fase STRATEGY

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
| `arquitectura-tecnica/use-case-view/` (81 archivos) | ⚠ Boilerplate UC-individual; no muestra relaciones entre UCs — directorio canónico pero contenido incorrecto | Reemplazar 81 archivos UC-individuales por ~13 módulo-indexados; integrar contenido de `uc-module-view/` (H-14) |
| `arquitectura-tecnica/uc-module-view/` (15 archivos) | ⚠ Directorio redundante — contenido correcto en directorio con nombre no estándar | Integrar en `use-case-view/` y eliminar (H-14) |
| `arquitectura-tecnica/process-view/` (81 archivos) | ⚠ Diagramas de flujo UC mal clasificados como Process View; verdadero contenido (concurrencia/ETL) ausente | Reclasificar diagramas existentes a Use Case View; crear Process View real con diagramas de concurrencia (H-15) |
| `arquitectura-tecnica/deploy-view/` | ⚠ 71/80 copias idénticas del mismo diagrama | Reducir a 3 canónicos por variante de infra (H-10) |
| `arquitectura-tecnica/design-view/` | ⚠ 160/160 boilerplate UC-individual | Reducir a ~12 módulo-indexados (H-11) |
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
| `arquitectura-tecnica/bounded-contexts/` | ✓ DIAG puro — es el verdadero domain model | Consolidar en `domain-model/`; eliminar directorio (H-09) |
| `arquitectura-tecnica/deploy-view/` (80 archivos) | ⚠ 71/80 son copia idéntica del mismo diagrama | Reducir a 3 diagramas canónicos por variante de infra (H-10) |
| `arquitectura-tecnica/design-view/` (160 archivos) | ⚠ 160/160 boilerplate genérico; 4 pasos idénticos en todos los archivos | Reducir a ~12 diagramas canónicos por módulo (H-11) |
| `arquitectura-tecnica/implementation-view/` (80 archivos) | ⚠ 12 diagramas únicos reales; 68 redundantes — agrupación correcta es por módulo | Reducir a 12 archivos `mod-{nombre}.rst` (H-12) |
| `arquitectura-tecnica/modulos/*/diagramas/` (30 archivos) | ✓ 30 únicos, dominio-específicos, alta calidad | Correcto — mantener (H-13) |
| `arquitectura-tecnica/modulos/*/` textuales (43 archivos) | ⚠ ARCH textual en zona DIAG; `caller/operator/supervision/` prueban que son opcionales aquí | Decisión pendiente P-01 (H-13) |
