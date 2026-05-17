# CLEAN_CODE_NAMING_PRINCIPLES

```yml
type: Norma de Proyecto (Backend / General)
status: Aprobado
version: 1.0.0
created_at: 2026-05-08
applies_to: IACT-docs, IACT-backend
authoritative_for: nombres de clase, modulo, metodo, variable y archivo
```

> **Documento autoritativo de naming.** Los estandares
> particulares del corpus (`STD-007`, `STD-008`, `STD-010`,
> `STD-013`, `backend/conventions.rst v2.0.0`) **derivan**
> de este documento. Ante cualquier divergencia, prevalece
> CLEAN_CODE.

---

## §1. Principios fundamentales

### §1.1 El nombre describe el **rol en el dominio**

El nombre de una clase, metodo o variable debe permanecer
valido si el framework o la libreria de implementacion
cambian. El nombre **NO** debe contener:

- Marcas del framework (`Django`, `DRF`, `Vue`, `React`).
- Sufijos que describen mecanismo tecnico de la base
  heredada (`Serializer`, `ViewSet`, `Backend`).
- Patrones GoF como sufijo cuando no expresan rol del
  dominio (`Factory`, `Builder`, `Manager` genericos).

### §1.2 Sufijos GoF como **default prohibido**

Los sufijos `Factory`, `Builder`, `Manager`, `Helper`,
`Util`, `Utils`, `Wrapper`, `Provider`, `Service` (cuando
es generico) estan prohibidos como default. Son aceptables
**solo** cuando:

- Expresan rol concreto del dominio
  (e.g., `UserOnboardingService` — el "service" es el rol).
- El patron GoF se materializa con su semantica completa
  (e.g., `QueryBuilder` con interfaz fluent
  `.where().apply().order_by()` real).
- Son API publica de un framework externo
  (e.g., `TransactionManager` de Django ORM,
  `DjangoModelFactory` de `factory_boy`).

### §1.3 Naming de tests

- Datos de prueba: sufijo `TestData`
  (`UserTestData`, `SessionTestData`).
- Fixtures de pytest: prefijo descriptivo (no `Factory`).
- Mocks: `Mock<Concepto>` o `Stub<Concepto>`.
- NO usar sufijo `Factory` para datos de tests.

### §1.4 Distincion produccion vs tests

Una clase de produccion con sufijo prohibido se renombra a
su rol del dominio (no a `*TestData`):

```
EventFactory (uc-perm-09 produccion) → AuditEventCreator
UserFactory  (uc-usr-01 patrones produccion) → UserOnboardingService
UserFactory  (uc-auth-01 testing)            → UserTestData
```

### §1.5 Identificadores en ingles

Toda clase, metodo, atributo y variable se nombra en
**ingles tecnico**. La narrativa de requisitos puede ser en
español; los identificadores no.

```
✓ find_recent(period)        ✗ ejecuciones_recientes()
✓ find_by_state(state)       ✗ por_estado(state)
✓ last_successful_by_dataset ✗ ultima_ejecucion()
```

### §1.6 Nombres canonicos prefijados sobre genericos

Cuando un identificador puede coincidir con uno de otra
clase, prefijar con el concepto especifico:

```
✓ rule_id        ✗ id (en AlertRule)
✓ view_id        ✗ id (en SavedView)
✓ subscription_id ✗ id (en Subscription)
✓ filters_snapshot ✗ filters (cuando es snapshot persistido)
✓ owner_user_id  ✗ owner (cuando es FK a User)
```

---

## §2. Sufijos prohibidos por categoria

### §2.1 Sufijos de framework (Backend Django/DRF)

| Sufijo | Origen | Reemplazo de dominio |
|---|---|---|
| `Serializer` | DRF `ModelSerializer` | `Contract` o `Representation` |
| `ViewSet` | DRF `ModelViewSet` | `Endpoints` |
| `View` (cuando hereda de `APIView`) | DRF | `Endpoint` |
| `Permission` (cuando hereda de `BasePermission`) | DRF | `AccessPolicy` o `RequirePolicy` |
| `Backend` (auth) | Django auth `BaseBackend` | `AuthProvider` |
| `Manager` (cuando es Django Manager generico) | Django ORM | `Query` o `Repository` |
| `Middleware` | Django/WSGI | nombre de rol descriptivo |

**Excepciones (preservar):**

- `BasePermission`, `BaseBackend`, `ModelBackend`,
  `APIView`, `ModelSerializer`, `ModelViewSet`,
  `ReadOnlyModelViewSet`, `TemplateView`, `DjangoModelFactory`,
  `SubFactory` — clases base externas.
- `TransactionManager` — API publica Django ORM
  (`transaction.atomic()`).
- `QueryBuilder` con interfaz fluent real
  `.where().apply().order_by()`.

### §2.2 Sufijos GoF

| Sufijo | Aplicabilidad |
|---|---|
| `Factory` | **Prohibido** salvo lib externa o "rol del dominio que ES factory" |
| `Builder` (sin fluent real) | **Prohibido** — usar `Assembler` |
| `Builder` (con fluent real) | Permitido |
| `Manager` (generico) | **Prohibido** — usar `OperationsCoordinator` o rol especifico |
| `Helper`, `Util`, `Utils` | **Prohibido** — nombrar el rol del dominio |
| `Wrapper` | **Prohibido** — describir el contrato |

### §2.3 Domain-noun preservation (criterio D4)

Si el sufijo prohibido es **noun nominal del dominio** (no
indica rol de framework), se preserva. Casos verificados:

| Clase | Sufijo | Razon de preservacion |
|---|---|---|
| `SavedView` | `View` | "vista guardada" del reporte; entidad de dominio |
| `AuditEventView` | `View` | CQRS read model (DTO), no DRF View |
| `ExceptionalPermission` | `Permission` | Domain entity RBAC; "permission" es noun |
| `TemporaryPermission` | `Permission` | Domain entity RBAC |
| `DirectPermission` | `Permission` | Domain entity RBAC |
| `StorageBackend` | `Backend` | Rol de infraestructura, no Django auth |
| `CacheBackend` | `Backend` | Rol de infraestructura |
| `TransactionManager` | `Manager` | API Django ORM publica |

**Criterio operativo:**

1. ¿La clase EXTIENDE una base del framework
   (`BasePermission`, `BaseBackend`, `APIView`)? → suffix
   prohibido aplica → renombrar.
2. ¿La clase es una entidad de dominio cuyo concepto se
   llama asi en el negocio? → preservar.
3. ¿La clase es API publica de un framework externo? →
   preservar.

---

## §3. Patron por categoria de archivo / componente

### §3.1 Backend Python

```
✓ models.py          UserCapabilityResolver, MenuItemRepo
✓ representations.py UserContract, ReportContract
✓ endpoints.py       LoginEndpoint, ReportEndpoints
✓ access_policies.py FunctionAccessPolicy, GranularAccessPolicy
✓ providers.py       FunctionAuthProvider
✓ services.py        UserOnboardingService, AuditEventCreator
✓ assemblers.py      MenuAssembler, ResumenSaludAssembler
```

NOTA: el nombre del **archivo** sigue STD-007 (snake_case).
El nombre de la **clase** es lo critico, no el del archivo.

### §3.2 Tests

```
tests/
  test_<concepto>.py
  fixtures.py
  test_data.py        UserTestData, SessionTestData,
                      GrupoPermisoTestData
```

### §3.3 Modelos de dominio (RST diagramas)

```
class User {
  + user_id : UUID
  + state : UserState
  --
  + create()
  + deactivate()
}
```

- Atributos prefijados con concepto especifico (no `id`
  generico cuando hay ambiguedad).
- Metodos con verbo descriptivo (`create`, no `make`).

---

## §4. Verbos canonicos en metodos

| Operacion | Verbo canonico | NO usar |
|---|---|---|
| Crear | `create`, `register` | `make`, `new` |
| Listar | `find`, `find_by_*`, `find_recent` | `list`, `query` (excepto en repos) |
| Obtener uno | `get_by_id`, `get` | `retrieve`, `fetch` (mezcla con HTTP) |
| Actualizar | `update`, `modify` | `edit`, `change` |
| Eliminar logico | `deactivate` | `delete` (reservado a fisico) |
| Validar | `validate_<aspecto>` | `check` (ambiguo) |
| Verificar permiso | `has_function`, `is_authorized` | `check_permission` |

---

## §5. Cross-references al corpus

Esta norma es **autoritativa**; los siguientes documentos
del corpus la implementan o la concretan:

- **`backend/conventions.rst`** v2.0.0 — aplicacion al
  contexto Django/DRF. Implementa §2.1, §3.1.
- **`STD-007`** — naming general (kebab-case archivos,
  snake_case Python).
- **`STD-008`** — naming de identificadores; prohibicion de
  acronimos opacos en API publica.
- **`STD-010`** v1.3.0 — vocabulario abstracto en narrativa
  de requisitos. Complementa CLEAN_CODE para narrativa
  (mientras CLEAN_CODE rige identifiers).
- **`STD-013`** — REST API conventions; URLs como recursos
  no acciones.

---

## §6. Implementacion historica

Esta norma fue aplicada al corpus IACT-docs en los
siguientes WPs:

| WP | Alcance |
|---|---|
| `clean-code-naming-audit` | Inventario inicial de violaciones |
| `naming-rules-resolution` | D1: alinear `backend/conventions.rst` v2.0.0 con §2.1 |
| `WP-A` (Sprint 1) | Renombrar archivos con prefijo numerico |
| `WP-B` (Sprint 2) | Limpiar `SoD` en narrativa |
| `WP-C` (Sprint 2) | Limpiar `SoD` en clases |
| `WP-E` | Renombrar 13 clases con sufijos `Factory/Builder/Manager` |
| `WP-F` | Renombrar 22 clases con sufijos `Serializer/ViewSet/View/Permission/Backend` |
| `WP-G` | Aplicar STD-010 vocabulario abstracto |
| `WP-H` (Sprint 1) | Renombrar `ReportFactory` → `ReportTypeRegistry` |
| `TD-D5` / `TD-D6` | Ampliar STD-010 §2.5 con exenciones de scope |
| `uc-view-domain-alignment` | Cross-ref UCs↔domain-model + 3 UCs nuevos |

Cada WP documenta sus decisiones en
`.thyrox/context/work/<WP>/track/`.

---

## §7. Aplicacion del criterio en revisiones

Cuando se introduzca una clase nueva o se modifique una
existente, el revisor debe responder:

1. ¿El nombre describe el **rol del dominio** o el
   mecanismo del framework? Solo el rol.
2. ¿El nombre permaneceria valido si se cambia
   DRF/Django/React? Si no, renombrar.
3. ¿El sufijo es **noun de dominio** o sufijo de
   framework? Si es framework (extiende base), aplicar
   tabla §2.1.
4. ¿El identificador es generico (`id`, `state`) cuando
   debe ser canonico (`view_id`, `status`)? Aplicar §1.6.
5. ¿El identificador esta en español? Traducir a ingles
   tecnico.

---

## §8. Historial

| Version | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-08 | Documento canonico standalone — consolidacion de la norma aplicada al corpus IACT-docs en los WPs A–H, TD-D5/D6 y uc-view-domain-alignment. Reemplaza la transmision oral de la norma con un artefacto consultable. |
