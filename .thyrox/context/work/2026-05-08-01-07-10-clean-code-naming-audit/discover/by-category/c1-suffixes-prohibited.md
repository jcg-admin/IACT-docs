```yml
created_at: 2026-05-08 01:15:00
project: IACT-docs
work_package: 2026-05-08-01-07-10-clean-code-naming-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: Cat-1 Audit (Sufijos Prohibidos)
```

# Cat-1 — Sufijos tecnicos prohibidos en nombres de clase

> Norma: CLEAN_CODE_NAMING_PRINCIPLES §1.2, §6.2, §9.

## 1. Resumen

| Sufijo | Norma | Clases unicas | Severidad |
|---|---|---|---|
| `Factory` | §1.2 (sin excepciones) | **9** | Alta |
| `Builder` | §1.2 (sin excepciones) | **7** | Media-Alta |
| `Manager` | §6.2 | **4** | Alta |
| `Serializer` | §6.2 | **27** | Alta |
| `ViewSet` | §6.2 | **7** | Alta |
| `Backend` | §6.2 | **5** | Media |
| `Permission` | §6.2 (mismo patron) | **8** | Media |
| `View` | §6.2 (mismo patron) | **81** | Alta |
| **Total clases unicas con sufijo prohibido** | | **148** | |

## 2. Hallazgo CRITICO — `backend/conventions.rst` contradice la norma

El archivo `source/backend/conventions.rst` lineas 36-39 prescribe
explicitamente como convencion:

```
- **Serializers:** sufijo ``Serializer`` (``UserSerializer``).
- **ViewSets:** sufijo ``ViewSet`` (``UserViewSet``).
- **APIViews:** sufijo ``View`` (``LoginView``).
- **Permissions:** sufijo ``Permission`` (``IsOwnerOrReadOnly``).
```

**Conflicto normativo:** este documento contradice
CLEAN_CODE_NAMING_PRINCIPLES v1.0.0 §6.2.

**Resolucion requerida:** ADR explicito para alinear ambas
normas. Opciones:

- Opcion A: Actualizar `backend/conventions.rst` para alinear
  con CLEAN_CODE (renombrar 100+ clases en docs).
- Opcion B: Documentar excepcion en CLEAN_CODE para clases
  de capas tecnicas explicitas (DRF).
- Opcion C: Mantener el conflicto registrado como TD hasta
  decision de la organizacion.

Sin resolver este conflicto, cualquier rename de clases
tecnicas crea otra contradiccion.

## 3. Detalle por sufijo

### 3.1 Factory (§1.2 — sin excepciones)

Clases unicas detectadas:

- `DjangoModelFactory` — base class de factory_boy (libreria)
- `EventFactory` — uc-perm-09
- `GrupoPermisoFactory` — backend
- `ReportFactory` — patrones-diseno + UCs
- `ReporteFactory` — patrones-diseno (Spanish variant)
- `SessionFactory` — backend
- `SubFactory` — factory_boy library
- `UserFactory` — uc-usr-01
- `UsuarioGrupoFactory` — backend (Spanish variant)

**Notas:**

- `DjangoModelFactory`, `SubFactory` son nombres de la
  libreria `factory_boy` — fuera del scope del proyecto.
- Resto: violan §1.2. Renombrar a `*TestData` o nombre de rol.

### 3.2 Builder (§1.2)

Clases unicas detectadas:

- `ComparativeBuilder`, `DisponibilidadBuilder`,
  `HeatmapBuilder`, `MenuBuilder`, `QueryBuilder`,
  `ResumenSaludBuilder`, `SummaryBuilder`.

**Notas:**

- `ResumenSaludBuilder` ya existe como dominio en
  domain-model (creado por WP `uml-deep-audit`). El nombre
  describe el rol "construye un ResumenSalud agregando
  fuentes" — semanticamente legitimo pero VIOLA la regla
  de prohibicion de Builder en §1.2.
- Discusion necesaria: ¿la regla §1.2 admite excepcion para
  builders de DTOs complejos? Si no, todos requieren rename.

### 3.3 Manager (§6.2)

- `AccessGroupManager`, `AlertManager`, `TransactionManager`,
  `TxManager` (alias plantuml).

**Recomendacion:**

- `AccessGroupManager` → `AccessGroupQuery` o
  `AccessGroupRepository` (Django Manager → Query).
- `AlertManager` → nombre de dominio especifico.
- `TransactionManager` → preservar (es API publica de
  Django ORM `transaction.atomic`).
- `TxManager` (alias plantuml) → `TransactionalContext`.

### 3.4 Serializer (§6.2 — 27 clases unicas)

Sample:

```
AccessSerializer, AdminSerializer, AdminUserSerializer,
AlertSerializer, ApplicationLogSerializer,
AssignmentSerializer, AuditEventSerializer, AuditSerializer,
AuthSerializer, CallSerializer, CallerSerializer,
ETLSerializer, FunctionGroupSerializer, LogSerializer,
LoginSerializer, MenuItemAdminSerializer, MenuItemSerializer,
ModelSerializer (DRF base), MySerializer (sample), PermSerializer
... (10 mas)
```

**Severidad alta** porque la mayoria son referencias en
multiples UCs/patrones a lo largo de docs.

**Recomendacion:** rename a `*Representation` (§6.3).

### 3.5 ViewSet (§6.2 — 7 clases)

`DashboardViewSet, MenuItemAdminViewSet, ModelViewSet (DRF
base), MyViewSet (sample), ReadOnlyModelViewSet (DRF base),
ReportViewSet, UserViewSet`

**Recomendacion:** rename a `*Endpoint` (§6.3).

### 3.6 Backend (§6.2 — 5 clases)

`CacheBackend, FunctionAuthBackend, ModelBackend (Django
base), RBACBackend, StorageBackend`.

**Notas:**

- `FunctionAuthBackend` → `FunctionAuthProvider` (§6.3
  ejemplo canonico).
- `RBACBackend` → `RBACAuthProvider` (tambien viola §8 por
  acronimo, doble violacion).
- `CacheBackend`, `StorageBackend` — son tipos de DTOs/atributos
  que representan "backend de almacenamiento como concepto
  abstracto"; ambiguo. Verificar con dominio.
- `ModelBackend` es base class de Django auth — fuera de scope.

### 3.7 Permission (§6.2 — 8 clases)

`BasePermission (DRF), DirectPermission, ExceptionalPermission,
FunctionPermission, GranularPermission, HasFunctionPermission,
RBACPermission, TemporaryPermission`.

**Notas:**

- `DirectPermission`, `ExceptionalPermission`,
  `TemporaryPermission` son **nombres de dominio** (un permiso
  excepcional es un concepto de negocio). NO son sufijo
  tecnico de DRF en este caso.
- `HasFunctionPermission`, `IsOwnerOrReadOnly` (mencionado en
  conventions.rst) SI son sufijos tecnicos DRF →
  `*AccessPolicy`.
- Discusion necesaria: distinguir caso por caso.

### 3.8 View (§6.2 — 81 clases)

Volumen alto. Sample: `APIView (DRF base), AbandonoReportView,
AccessAuditView, AccessView, AdminUserView, AdminView,
AlertView, ApplicationLogView, ArchView, AssignAGRView, ...`.

**Severidad alta** por volumen. Rename → `*Endpoint`.

## 4. Recomendaciones por severidad

### 4.1 Pre-requisito (bloqueante)

**Resolver el conflicto normativo `backend/conventions.rst`
vs CLEAN_CODE_NAMING_PRINCIPLES.** Sin esto, cualquier
rename masivo crea inconsistencia.

### 4.2 Bloque 1 — Bajo volumen, alto impacto (WP separado)

- 9 Factory + 7 Builder = 16 clases. WP focused: rename
  + update refs.

### 4.3 Bloque 2 — Manager + Backend + Permission (mezcla dominio/tecnico)

- 4 + 5 + 8 = 17 clases. Requiere triage caso-por-caso para
  separar dominio (preservar) vs sufijo tecnico (renombrar).

### 4.4 Bloque 3 — Alto volumen (Serializer + View + ViewSet)

- 27 + 81 + 7 = 115 clases. WP grande con plan dedicado.
- Solo proceder tras resolver conflicto normativo (4.1).

## 5. Out-of-scope (preservar)

- Clases base de librerias externas:
  `DjangoModelFactory`, `SubFactory`, `BasePermission`,
  `ModelBackend`, `ModelViewSet`, `ReadOnlyModelViewSet`,
  `APIView`.

## Refs

- CLEAN_CODE_NAMING_PRINCIPLES v1.0.0 §1.2, §6.2, §9.
- backend/conventions.rst (CONFLICTO documentado).
