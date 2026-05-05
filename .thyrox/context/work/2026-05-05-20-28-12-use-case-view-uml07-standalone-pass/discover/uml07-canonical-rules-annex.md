```yml
created_at: 2026-05-05 21:30:00
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
phase: Phase 1 — DISCOVER (anexo)
author: NestorMonroy
status: Aprobado
version: 1.0.0
source: source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/* + STD-008/011/012
```

# Anexo — Reglas canónicas uml-07 + normativas STD vinculantes

Este documento extrae **textualmente** las reglas y convenciones de las 10 lecciones
del módulo `uml-07-diagramas-casos-uso/` (material adaptado de "Aprendiendo UML en 24
horas — Hora 7") y las **normativas STD del proyecto IACT** que aplican a uml-07.
Estas reglas son **vinculantes** para los 83 archivos uml-07 standalone que produce
este WP.

Cada regla cita el archivo fuente y, donde aplica, el override de IACT.

## Normativas IACT vinculantes (overrides sobre uml-07 puro)

| STD / Constraint | Documento | Aplica a |
|---|---|---|
| **STD-008** | `source/normativa/estandares/std-008-naming-identificadores.rst` | Naming de identificadores técnicos |
| **STD-011** | `source/normativa/estandares/std-011-alias-diagramas-uml.rst` | **Aliases auto-documentados** en TODO `as ALIAS` |
| **STD-012** | `source/normativa/estandares/std-012-tipos-de-diagramas-uml.rst` | Ubicación canónica del UC diagram |
| **BR-006** | NIST RBAC Flat | Prohibe generalización entre actores |
| **CNST-005** | SoD evaluado sobre funciones, no roles | |
| **CNST-026** | Sin PII en logs/diagrams | |
| **CNST-033** | Vocabulario unificado RBAC | |

## R-01 — Representación básica del modelo de caso de uso

**Fuente:** `representacion-de-un-modelo-de-caso-de-uso.rst`

> "Un actor es quien **inicia** un caso de uso, y otro actor (posiblemente el que inició,
> pero no necesariamente) es quien **recibe** algo de valor de él. La representación
> gráfica es directa: una **elipse** representa a un caso de uso y una **figura
> agregada** (stick figure) representa a un actor."
>
> "El actor que **inicia** se encuentra a la **izquierda** del caso de uso, y el que
> **recibe** a la **derecha**."
>
> "En UML una **línea asociativa** conecta a un actor con el caso de uso, y representa
> la comunicación entre ambos."
>
> "Generalmente, los actores están **fuera** del sistema, mientras que los casos de uso
> están **dentro** de él. Se utiliza un **rectángulo** (con el nombre del sistema dentro)
> para representar el confín del sistema; el rectángulo envuelve a los casos de uso."

**Implicación para IACT:**

- Iniciador izquierda, beneficiario derecha. Layout `left to right direction`.
- UC = elipse (`usecase "..."`), actor = stick figure (`actor "..."`).
- Rectangle con nombre del sistema = `rectangle "MOD_<Module>"` para cada UC standalone.
- Línea asociativa: `actor --> UC` (sin estereotipo).

## R-02 — Inclusión (`<<include>>`)

**Fuente:** `inclusion.rst`

> "Para representar la inclusión utilizará el símbolo que usó para la dependencia entre
> clases: una **línea discontinua con una punta de flecha** que conecta los casos de uso
> apuntando hacia el caso de uso dependiente; sobre la línea agregará un estereotipo:
> la palabra `<<incluir>>` (o `<<include>>`) bordeada por dos pares de paréntesis
> angulares."
>
> "Un caso de uso incluido **nunca aparecerá solo**: funciona como parte de un caso de
> uso que lo incluya."

**Sintaxis PlantUML:**

```
UC_Base ..> UC_Incluido : <<include>>
```

**Implicación para IACT:**

- `..>` (línea discontinua con punta de flecha) **del UC base AL UC incluido**.
- Estereotipo `<<include>>` (preferir inglés sobre `<<incluir>>` por consistencia).
- **Regla derivada R-02bis:** UC con prefijo `UC_INC_*` (e.g. `UC_INC_RPT_01 Resolver
  Segmento`) **NO recibe archivo standalone propio** — solo aparece como UC incluido
  desde otros archivos uml-07.

## R-03 — Extensión (`<<extend>>`) y extension points

**Fuente:** `extension.rst`

> "Podemos decir que el nuevo caso de uso **extiende** al original dado que *agrega
> otros pasos* a la secuencia del caso de uso original, que se conoce como **el caso
> de uso base**."
>
> "La extensión sólo se puede realizar en puntos indicados de manera específica dentro
> de la secuencia del caso de uso base. A estos puntos se les conoce como **puntos de
> extensión**."
>
> "Podrá concebir la extensión con una línea de dependencia (línea discontinua con
> punta de flecha), junto con un estereotipo que muestra `<<extender>>` (o `<<extend>>`)
> entre paréntesis angulares; el punto de extensión aparecerá debajo del nombre del
> caso de uso."

**Sintaxis PlantUML:**

```
usecase "UC_Base\n.. extension points ..\nNombrePunto" as UC_Base
usecase "UC_Extensor" as UC_Extensor

UC_Extensor ..> UC_Base : <<extend>>\n(NombrePunto)
```

**Implicación para IACT:**

- `..>` **del UC extensor AL UC base** (dirección INVERSA al `<<include>>`).
- Estereotipo `<<extend>>` con punto de extensión entre paréntesis tras un `\n`.
- Extension points declarados en label del UC base con sintaxis
  `"NombreUC\n.. extension points ..\nNombrePunto1\nNombrePunto2"`.
- **Pattern Phase 10:** identificar extension points desde `flujos-alternos.rst` y
  `excepciones.rst` del UC.

## R-04 — Generalización entre UCs

**Fuente:** `generalizacion.rst`

> "Las clases se heredan entre sí; lo mismo se aplica a los casos de uso."
>
> "En la herencia de los casos de uso, el caso de uso secundario hereda las acciones y
> significado del primario, y además agrega sus propias acciones."
>
> "Modelará la generalización de casos de uso con líneas continuas y una **punta de
> flecha en forma de triángulo sin rellenar** que apunta hacia el caso de uso primario."

**Sintaxis PlantUML:**

```
UC_Secundario --|> UC_Primario
```

**Implicación para IACT:**

- **R-04 entre UCs:** PERMITIDA, sintaxis `--|>`. Aplica caso por caso (opcional, R-10
  uml-07). Útil para variantes del mismo flujo (e.g. `UC_PERM_01` vista PERM puede
  generalizar `UC_ACC_04` vista ACC, pero la decisión IACT actual es modelar la vista
  PERM como `<<include>>` del UC ACC backing — más explícito).

## R-05 — Generalización entre actores

**Fuente:** `generalizacion.rst` y `comprension-de-los-usuarios.rst`

> "La relación también se puede establecer entre **actores**, así como entre casos de
> uso. Si cambia el nombre del representante como `Reabastecedor`, tanto éste como el
> `Recolector` serán secundarios del `AgenteProveedor`."
>
> "Sería conveniente mostrar a los usuarios en una **jerarquía de generalización**."

**Sintaxis PlantUML:**

```
ActorPadre <|-- ActorHijo
```

**Override IACT — BR-006 RBAC Flat NIST:**

uml-07 puro PERMITE generalización entre actores con `<|--`. **IACT PROHÍBE esta
construcción** por la restricción de negocio BR-006 (NIST RBAC Flat) y CNST-005
(SoD evaluado sobre funciones, no sobre roles).

**Acción para los 83 archivos:**

- ❌ NO usar `<|--` entre actores en ningún archivo del WP.
- ✅ Si un UC tiene múltiples invokers (e.g. UC_ADM_01 con 4 funciones), declararlas
  como **actores independientes** sin relación de herencia.

## R-06 — Comprensión de los usuarios (entrevistas)

**Fuente:** `comprension-de-los-usuarios.rst`

> "Se tiene que tener atención a los usuarios y entender los tipos de funcionalidad.
> Esto se realiza mediante **entrevistas** — nada puede sustituir a las entrevistas."

**Implicación para IACT:**

Los UCs ya están especificados en `casos-uso/` (12 partes por UC). El equivalente a
"entrevista" para este WP es la **lectura completa de los 7 specs textuales por UC**
(KI-3 del solution-strategy):

1. `index.rst`
2. `informacion-general.rst`
3. `actores-precondiciones.rst`
4. `flujo-principal.rst`
5. `flujos-alternos.rst`
6. `excepciones.rst`
7. `criterios-aceptacion.rst` (+ opcionales `patrones-diseno.rst`,
   `implementacion-tecnica.rst`)

NO leer estos specs equivale a generar el diagrama sin entrevistar al cliente — el
predecesor cometió ese error (L-03).

## R-07 — Comprensión del dominio (clases primero)

**Fuente:** `comprension-del-dominio.rst`

> "Para dicha compresión se tiene que empezar con las entrevistas al cliente; en la
> entrevista tiene que surgir el diagrama de clases."

**Implicación para IACT:**

El diagrama de clases del dominio = `source/arquitectura-tecnica/domain-model/` (67
archivos canónicos + 14 nuevos del WP). Cualquier actor `<<sistema>>` en un uml-07
DEBE corresponder a una clase del domain-model:

- Si la clase existe: usar nombre canónico exacto + cross-ref `:doc:` en seealso.
- Si la clase no existe pero es legítima del dominio: crearla en domain-model
  (Etapa 1, T-001..T-014).
- Si es infraestructura externa (no domain): usar `<<sistema_externo>>`.

## R-08 — Comprensión de los casos de uso (requerimientos funcionales)

**Fuente:** `comprension-de-los-casos-de-uso.rst`

> "Este conjunto de casos de uso constituye los **requerimientos funcionales** del
> sistema."

**Implicación para IACT:**

Los 83 UCs son los requerimientos funcionales del sistema IACT. Cada uml-07 standalone
es la **representación visual** de uno de esos requerimientos. La completitud del set
es importante — los 83 deben existir en use-case-view/ tras el WP.

## R-09 — Profundización (alto nivel → detalle)

**Fuente:** `profundizacion.rst`

> "Determinar cuáles son los casos de uso de alto nivel y a partir de ellos, generar
> el modelo detallado."
>
> "Ciertos pasos se repetirán de un caso de uso a otro, y ello le llevará a otros casos
> de uso (posiblemente incluidos)."
>
> "**El análisis del caso de uso describe el comportamiento de un sistema, nunca toca
> a la implementación**."

**Implicación crítica para IACT (R-09bis):**

- **NO usar nombres de implementación** como UCs:
  - ❌ `usecase "sp_etl_maestro" as UC` (nombre de stored procedure)
  - ❌ `usecase "POST /api/admin/sod-rules/" as UC` (HTTP route)
  - ❌ `usecase "AssignmentRepo.create()" as UC` (método de clase)
  - ❌ `usecase "TX_BEGIN; INSERT ...; TX_COMMIT" as UC` (SQL inline)
- **SÍ usar comportamiento de alto nivel:**
  - ✅ `usecase "Crear regla SoD" as UC`
  - ✅ `usecase "Validar conjuntos disjuntos" as UC`
  - ✅ `usecase "Persistir SeparationRule" as UC`
  - ✅ `usecase "Notificar via InternalMailbox" as UC`

- **Sub-usecases incluidos repetidos en varios UCs:** identificarlos y modelar como
  UCs incluidos (e.g. "Validar SoD", "Emitir AuditEvent", "Invalidar PermissionCache"
  son sub-usecases reutilizados por muchos UCs RBAC). En este WP no se crean archivos
  standalone para sub-usecases incluidos genéricos — solo se modelan como elipses
  dentro del rectangle del UC base que los incluye.

## R-10 — El panorama (qué entidades UML usa cada diagrama)

**Fuente:** `el-panorama.rst`

Las entidades UML que un diagrama de caso de uso usa:

| Categoría UML | Entidades |
|---|---|
| Estructurales | Actor, Caso de uso |
| Relaciones | Asociacion (línea), Generalizacion (`<|--`/`--|>`), Dependencia (con `<<include>>`/`<<extend>>`) |
| Agrupamiento | Paquete (no se usa en uml-07; se usa Rectangle como confín del sistema) |
| Anotacion | Nota (`note bottom of UC`) |
| Extensión | Estereotipo (`<<...>>`) |

**Implicación para IACT:** los 83 archivos uml-07 standalone usan exactamente estas
entidades, en este orden de aparición:

1. `actor "..." as ALIAS [<<stereotype>>]` — actores con/sin estereotipo.
2. `rectangle "MOD_<Module>" { ... }` — confín del sistema.
3. `usecase "..." as ALIAS` — casos de uso dentro del rectangle.
4. `Actor --> UC` — asociación actor-UC.
5. `UC_Base ..> UC_Incluido : <<include>>` — inclusión.
6. `UC_Extensor ..> UC_Base : <<extend>>(NombrePunto)` — extensión.
7. `UC_Sec --|> UC_Pri` — generalización entre UCs (opcional).
8. `note bottom of UC ... end note` — notas con BR/CNST/P/ADR.

## R-11 — Sobre la "Máquina de Gaseosas" (ejemplo de complejidad real)

**Fuente:** `una-nueva-visita-a-la-maquina-de-gaseosas.rst`, `inclusion.rst`,
`extension.rst`

El ejemplo de la máquina de gaseosas demuestra:

- Múltiples actores (Cliente, Representante del proveedor, Recolector) cada uno
  iniciando UCs distintos.
- Inclusión de sub-usecases compartidos ("Exhibir el interior", "Cubrir el interior")
  entre múltiples UCs base.
- Extensión condicional ("Reabastecer de acuerdo a las ventas" extiende "Reabastecer"
  en el extension point "Llenar los compartimientos").

**Implicación para IACT:** los UCs IACT con multiplicidad similar deben modelar
correctamente:

- UCs CRUD umbrella (UC_ADM_01..03) con múltiples funciones invokers.
- UCs vista alternativa (UC_PERM_NN → UC_ACC_NN) con `<<include>>` cross-MOD.
- UCs con flujos alternos modelados como `<<extend>>` (UC_ALR_05 con multi-tipo).

## STD-011 — Aliases auto-documentados (vinculante)

**Fuente:** `source/normativa/estandares/std-011-alias-diagramas-uml.rst` (Aprobado, v1.0.0).

### Principio core

> "Un diagrama de secuencia, comunicación o actividad es documentación. Al leer una
> flecha `A -> B : mensaje`, el lector debe entender quiénes son A y B **sin buscar
> la declaración del participante**."

**Regla principal:** todo alias DEBE ser auto-documentado. El alias por sí solo
revela el rol o nombre del participante.

### Convenciones por elemento

#### Actores RBAC (funciones)

El alias **es el nombre exacto de la función RBAC** del catálogo (snake_case):

```
✓ CORRECTO
actor "view_reports" as view_reports
actor "assign_functions" as assign_functions
actor "request_pipeline_retry" as request_pipeline_retry
actor "view_audit_log" as view_audit_log <<beneficiario>>
```

Cuando el actor tiene múltiples funciones en la etiqueta, usar la **función principal**
como alias:

```
actor "view_reports\n(view_dashboard)" as view_reports
```

#### Sistemas (entidades del domain-model)

El alias **es el nombre de la clase en CamelCase, sin espacios**:

```
✓ CORRECTO
actor "AuditService" as AuditService <<sistema>>
actor "PermissionCache" as PermissionCache <<sistema>>
actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
actor "InternalMailbox" as InternalMailbox <<sistema>>
```

#### Caller externo

```
✓ CORRECTO
actor "Caller" as Caller <<externo>>
```

### PROHIBIDO (rechazo automático en audit)

Aliases de 1-2-3 letras o crípticos:

```
✗ PROHIBIDO          ← motivo
actor "..." as U     ← 1 letra
actor "..." as AE    ← 2 letras (AuthEndpoint)
actor "..." as DE    ← 2 letras (DashboardEndpoint)
actor "..." as SR    ← 2 letras (SegmentResolver)
actor "..." as SRP   ← acrónimo sin significado
actor "..." as RVG   ← sigla de grupo
actor "..." as QSG   ← sigla de grupo
actor "..." as PC    ← 2 letras (PermissionCache)
actor "..." as AS    ← 2 letras (AuditService)
actor "..." as INVOKER  ← genérico, no identifica función
actor "..." as F_OWN    ← genérico
actor "..." as F_ADMIN  ← genérico
```

**Detectado en uml-06 actuales** (a corregir en los uml-07 standalone):

- `as INVOKER`, `as F_CREATE`, `as F_UPDATE`, `as F_DISABLE`, `as F_VIEW`,
  `as F_ASSIGN`, `as F_OWN`, `as F_ADMIN`
- `as AS` (AuditService), `as PC` (PermissionCache), `as RV` (RuleValidator),
  `as EE` / `as ER` (EvaluatorReloader), `as PS` (PermissionService),
  `as TC` (TimingCalculator), `as SAN` (Sanitizer), `as PII` (PIIScanner),
  `as PE` (PipelineExecution), `as PL` (PipelineLog), `as MB` (InternalMailbox),
  `as TARGET`, `as SVC`, `as REPO`, `as KPI`, `as BK`, `as CE`, `as FV`,
  `as CALLER`, `as CALL`, `as SESSION`, etc.

**Acción para los 83 uml-07 standalone:** todos los aliases prohibidos detectados
arriba se reemplazan por el nombre completo (igual al label).

### Excepciones permitidas

Aliases cortos universalmente reconocidos en el dominio:

```
✓ EXCEPCIÓN OK
IVR  ← Interactive Voice Response (entidad externa)
JWT  ← JSON Web Token
ETL  ← Extract-Transform-Load (como nombre de entidad — pero CNST-033 prefiere "Pipeline")
GUI  ← Graphical User Interface
CPU  ← Central Processing Unit
```

### Validación

```bash
# Buscar aliases prohibidos en diagramas PlantUML del WP
grep -rn " as [A-Z][A-Z]\?$\| as [a-z][a-z]\?$" \
  source/arquitectura-tecnica/use-case-view/ \
  --include="*.rst"

# Resultado vacío = conformidad con STD-011
```

### Implicación para Phase 10

**Cambio significativo en el template canónico** (Phase 5 STRATEGY) — actualizar
sección 3.3 del `solution-strategy.md`:

```diff
- actor "<funcion_rbac>" as INVOKER
- actor "<otra_funcion>" as F_OTHER
- actor "view_audit_log" as view_audit_log <<beneficiario>>
- actor "<EntityCanonical>" as ABBR <<sistema>>
- actor "<Boundary>" as B <<sistema_externo>>

+ actor "<funcion_rbac>" as <funcion_rbac>
+ actor "<otra_funcion>" as <otra_funcion>
+ actor "view_audit_log" as view_audit_log <<beneficiario>>
+ actor "<EntityCanonical>" as <EntityCanonical> <<sistema>>
+ actor "<Boundary>" as <Boundary> <<sistema_externo>>
```

**Resultado:** alias = label exactamente. Auto-documentado por construcción.

## STD-012 — Conflicto de ubicación canónica del UC diagram

**Fuente:** `source/normativa/estandares/std-012-tipos-de-diagramas-uml.rst` (Aprobado, v1.0.0).

### Lo que dice STD-012

Para "Casos de uso" (línea 134-140):

> Ubicación canónica:
> - `casos-uso/{cluster}/{uc}/diagramas-uml/caso-de-uso.rst`
> - `arquitectura-tecnica/use-case-view/{cluster}/{uc}/caso-de-uso.rst`
>
> Granularidad: 1 UC / archivo (spec) + 1 vista módulo
>
> Cuándo usar: Spec del UC: actores + relaciones include/extend.
> Vista arq: módulo entero.

### Conflicto con el target del WP

| Aspecto | STD-012 dice | WP target dice |
|---|---|---|
| Ubicación per-UC en use-case-view | `arquitectura-tecnica/use-case-view/{cluster}/{uc}/caso-de-uso.rst` (subdirectorio por UC, archivo único `caso-de-uso.rst`) | `use-case-view/<module>/uc-XXX-NN-<slug>.rst` (flat dentro del módulo, naming auto-explicativo) |

### Decisión a tomar

Hay 3 caminos posibles:

1. **Seguir STD-012 literal** — usar subdirectorios por UC con archivo `caso-de-uso.rst`:
   ```
   use-case-view/access/uc-acc-01/caso-de-uso.rst
   use-case-view/access/uc-acc-02/caso-de-uso.rst
   ...
   ```
   Pro: cumple normativa formal.
   Contra: no es auto-explicativo (target original del WP); requiere navegar dentro
   del subdirectorio para identificar el UC.

2. **Mantener target del WP** — flat con naming auto-explicativo:
   ```
   use-case-view/access/uc-acc-01-asignar-funciones.rst
   ```
   Pro: auto-explicativo (target original).
   Contra: viola STD-012 — requeriría **actualizar STD-012** v1.1.0 con esta variante.

3. **Híbrido** — subdirectorio + naming auto-explicativo dentro:
   ```
   use-case-view/access/uc-acc-01-asignar-funciones/caso-de-uso.rst
   ```
   Pro: subdirectorio (alineado con STD-012) + nombre auto-explicativo en directorio.
   Contra: archivo final dice solo `caso-de-uso.rst`, redundancia entre subdirectorio
   y filename.

**Recomendación:** opción 2 con actualización de STD-012 v1.1.0 si el ejecutor confirma
que el naming auto-explicativo flat es el preferido. Documentar en `decisions-log.md`.

## Síntesis — checklist canónico para CADA archivo uml-07 standalone

Aplicar en orden al construir cada archivo `use-case-view/<mod>/uc-XXX-NN-<slug>.rst`:

```
[ ] R-01: layout left-to-right; actor stick figure; UC elipse;
          rectangle "MOD_<X>" como confín del sistema
[ ] R-01: actor iniciador a la izquierda; beneficiario a la derecha
[ ] R-01: línea asociativa actor --> UC (sin estereotipo)
[ ] R-02: UCs incluidos con ..> y <<include>>; nunca standalone
[ ] R-03: UCs extensores con ..> y <<extend>>(extension point);
          extension points declarados en label del UC base
[ ] R-04: generalización entre UCs con --|> (opcional, evaluar)
[ ] R-05/BR-006: NO <|-- entre actores (override IACT vs uml-07 puro)
[ ] R-06: leer 7 specs textuales del UC antes de diseñar
[ ] R-07: actores <<sistema>> = nombres exactos de domain-model;
          si no existe, crear (Etapa 1) o marcar <<sistema_externo>>
[ ] R-08: el UC representa requerimiento funcional (alto nivel)
[ ] R-09: NO nombres de implementación (SP, HTTP routes, SQL, métodos)
          como labels de UCs; SÍ comportamientos de alto nivel
[ ] R-10: usar solo Actor, UC, Rectangle, asociación, inclusión,
          extensión, generalización entre UCs, nota; NO Paquete
[ ] R-11: modelar correctamente multi-invoker, vistas alternas y
          flujos alternos según el patrón del UC
[ ] STD-011: alias = label exactamente (sin abreviar)
              actores RBAC: as snake_case_function
              sistemas: as CamelCaseClassName
[ ] STD-012: ubicación per-UC = decisión SP-02 (opción 2 recomendada)
```

## Anti-checklist — qué NO debe aparecer en ningún archivo

```
[ ] ❌ <|-- entre actores
[ ] ❌ Nombres de implementación como UCs (SP, HTTP, SQL, métodos)
[ ] ❌ Actor <<sistema>> con nombre que no existe en domain-model
       sin haber creado el archivo en domain-model primero
[ ] ❌ UC_INC_* como archivo standalone (solo aparece included)
[ ] ❌ Sub-usecases sin <<include>> o <<extend>> hacia el UC base
       (UCs huérfanos dentro del rectangle)
[ ] ❌ Estereotipos en líneas asociativas actor-UC
[ ] ❌ Notas con TODO o "pending" — toda nota debe ser definitiva
[ ] ❌ Specs no leídos (R-06 es obligatorio, no opcional)
[ ] ❌ Aliases prohibidos por STD-011: 1-2 letras, INVOKER, F_*,
       AS, PC, RV, EE, ER, PS, TC, SAN, PII, PE, PL, MB, etc.
[ ] ❌ Alias diferente del label (alias DEBE ser igual al nombre
       de la función / clase para auto-documentación)
```

## Trazabilidad

Este anexo materializa las **lecciones canónicas uml-07** del proyecto IACT como
requisitos vinculantes del WP. Cualquier archivo del WP que viole una regla aquí
listada es **rechazo automático en SP-02 PILOT** o en SP-03 build/audit.

## Rules en el audit script (`scripts/validate-uml07-standalone.sh`)

El audit script de Etapa 6 (T-114) implementa estas reglas como checks:

| Check | Regla | Detección |
|---|---|---|
| C-01 | R-01 layout | grep `^\s*left to right direction` |
| C-02 | R-01 rectangle | grep `^\s*rectangle "MOD_` |
| C-03 | R-02 include direction | regex `\w+\s*\.\.>\s*\w+\s*:\s*<<include>>` |
| C-04 | R-03 extend direction | regex `\w+\s*\.\.>\s*\w+\s*:\s*<<extend>>` |
| C-05 | R-05/BR-006 no actor inheritance | grep `<\|--` en bloques `@startuml` |
| C-06 | R-09 no implementation names | regex contra patterns `sp_*`, `^POST `, `\.SQL\b`, `\.\w+\(\)` en labels de UC |
| C-07 | R-10 entidades válidas | parser PlantUML que lista solo Actor/UC/Rectangle/Note |
| C-08 | Sistemas en domain-model | match nombres `<<sistema>>` contra archivos en domain-model/ |

Output: `track/audit-report-{ISO}.md` con violaciones por archivo + line.
