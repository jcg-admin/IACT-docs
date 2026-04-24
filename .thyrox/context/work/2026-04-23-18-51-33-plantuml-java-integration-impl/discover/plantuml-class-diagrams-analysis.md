```yml
created_at: 2026-04-24 00:30:00
project: IACT-docs
work_package: 2026-04-23-18-51-33-plantuml-java-integration-impl
phase: Phase 1 — DISCOVER
author: Claude Code Agent
status: Borrador
version: 1.0.0
```

# Análisis: PlantUML Class Diagrams — Syntax, Styling, Architecture Patterns

**Input:** Guía de Referencia PlantUML 1.2025.0 — pp. 62-77 (Secciones 3.8-3.29)

**Propósito:** Validar si class diagrams son aplicables a IACT-docs y cómo se integran con estrategia de centralización.

**Criticidad:** MEDIA — Menos críticos que UC/Sequence diagrams para IACT, pero útiles para documentación de arquitectura.

---

## 1. Nivel de Aplicabilidad para IACT-docs

### 1.1 Preguntas Clave

**¿Necesita IACT-docs class diagrams?**

1. ¿Documento UC diagrams? → SÍ (100+ diagramas)
2. ¿Documentar sequence flows? → POSIBLEMENTE (flujos complejos)
3. ¿Documentar arquitectura de clases Java/Python? → **PROBABLEMENTE NO** (project es documentación de requisitos, no código interno)
4. ¿Documentar estructura de datos/modelos? → POSIBLEMENTE (si hay especificaciones de dominio)

**Conclusión:** Class diagrams son **opcionales y contextual** — útiles SOLO si IACT documenta arquitectura de software, no requisitos funcionales.

### 1.2 Recomendación para IACT

**Enfoque sugerido:**
- ✅ Si IACT también documenta arquitectura técnica interna → incluir class diagrams
- ❌ Si IACT solo documenta requisitos de negocio/usuario → puede omitir class diagrams
- ⚠️ Si hay componentes de sistemas externos → considerar para mostrar integraciones

---

## 2. Características de Class Diagrams (Secciones 3.8-3.29)

### 2.1 Cuerpo Avanzado: Separadores (Section 3.8)

**Sintaxis:**
```plantuml
class Foo {
  .. Public API ..
  + getName()
  + getAddress()
  
  .. Internal Methods ..
  - _processData()
  
  __ Private Fields __
  - int _age
  
  -- Configuration --
  - String _configPath
}
```

**Separadores válidos:**
- `..` (puntos) — separator simple
- `==` (iguales) — separator doble
- `__` (guiones bajos) — separator de subrayado
- `--` (guiones) — separator estándar

**Aplicabilidad a IACT:**
- ✅ Útil para organizar métodos públicos vs. privados
- ⚠️ Requiere que IACT documente clases reales (no solo casos de uso)
- ⚠️ Naming convention importante: `_privateVar` vs. `privateVar`

**Hallazgo de Naming:** PlantUML usa convención POSIX para variables privadas (`_varName`). Esto alza una **consideración arquitectónica**: ¿IACT seguirá convención Java (camelCase) o POSIX (_prefix)?

### 2.2 Notas y Estereotipos (Sections 3.9-3.10)

**Sintaxis de Estereotipos:**
```plantuml
class User << Human >>
class Database << System >>
class Logger << Utility >>
```

**Sintaxis de Notas:**
```plantuml
class Entity
note top of Entity : This is a base class
note left of Entity : Used by multiple domains
note as N1
  Multiline note
  with **bold** and //italic//
end note
```

**Aplicabilidad:**
- ✅ Estereotipos útiles para clasificar tipos (Human, System, Utility, Service, Repository)
- ✅ Notas para documentar restricciones, invariantes, diseño
- ⚠️ HTML inline (font, size, color) — debe restringirse como en UC/Sequence

**Hallazgo:** Misma restricción que UC/Sequence — NO colores inline, NO tamaños inline. Centralizar vía skinparam.

### 2.3 Atributos y Métodos Ocultos (Sections 3.14-3.18)

**Comandos:**
```plantuml
hide empty members        ← Oculta atributos/métodos vacíos
hide fields               ← Oculta TODOS los atributos
hide methods              ← Oculta TODOS los métodos
hide members              ← Oculta ambos
hide <<Stereotype>>       ← Oculta por estereotipo
remove @unlinked          ← Elimina clases no vinculadas
```

**Aplicabilidad:**
- ✅ Útil para simplificar diagramas complejos
- ⚠️ Requiere que el diagram tenga lógica clara de qué mostrar/ocultar
- ⚠️ No es recomendable para documentación — ocultar puede confundir lectores

**Recomendación para IACT:** Evitar `hide` en documentación de requisitos. Mostrar estructura completa o crear diagrama separado simplificado.

### 2.4 Clases Abstractas, Interfaces, Enums (Section 3.13)

**Sintaxis:**
```plantuml
abstract class AbstractEntity { }
interface Persistable { }
enum Status { ACTIVE, INACTIVE, PENDING }
annotation @Deprecated { }
```

**Aplicabilidad:**
- ✅ Soportado, pero requiere documentación de convención
- ⚠️ ¿IACT documentará interfaces Java o solo entidades de negocio?
- ❌ Probablemente NO necesario para UC (son diagramas de negocio, no técnicos)

### 2.5 Genéricos (Section 3.19)

**Sintaxis:**
```plantuml
class Container<T extends Element> {
  T getValue()
}
```

**Aplicabilidad:**
- ❌ NO APLICABLE a IACT — requisitos no usan genéricos
- ✅ Útil solo si documentar arquitectura Java/TypeScript interna

### 2.6 Paquetes y Espacios de Nombre (Sections 3.21-3.24)

**Sintaxis:**
```plantuml
package "Domain Logic" #DDDDDD {
  class Order
  class LineItem
}

namespace com.iact.domain {
  class User
  class Role
}
```

**Estilos de Paquetes:**
- Rectangle (por defecto)
- Node
- Folder
- Frame
- Cloud
- Database

**Aplicabilidad:**
- ✅ ÚTIL para agrupar clases por módulo/dominio
- ✅ Namespace separator configurable (`::`  vs. `.`)
- ⚠️ Requiere decisión clara sobre estructura de paquetes

**Recomendación:** Si IACT documenta arquitectura, usar `package` para agrupar por módulo (Auth, Access, Users, Reports, Alerts).

### 2.7 Direcciones de Flechas y Asociaciones (Sections 3.26-3.28)

**Sintaxis:**
```plantuml
User -left-> Dashboard
User -right-> Profile
User -up-> Admin
User -down-> Settings

User "1" -- "0..*" Order        ← Multiplicidad
(User, Order) .. Subscription   ← Clase de asociación
```

**Aplicabilidad:**
- ⚠️ Direcciones (`left`, `right`, `up`, `down`) generalmente innecesarias — Graphviz maneja bien
- ⚠️ Multiplicidad (`1`, `0..*`, `*`) es estándar UML — ÚTIL
- ✅ Clases de asociación (association class) útiles para relaciones complejas

---

## 3. Estrategia de Centralización para Class Diagrams

### 3.1 skinparam para Class Diagrams

**Basado en análisis anterior (skinparam context-dependent):**

```plantuml
skinparam class {
  BackgroundColor SECONDARY_COLOR
  BorderColor PRIMARY_COLOR
  BorderThickness 2
  FontColor TEXT_COLOR
  AttributeBackgroundColor #F5F5F5
  ArrowColor TEXT_COLOR
}

skinparam abstract {
  BackgroundColor #E0E0E0
  BorderColor PRIMARY_COLOR
  FontStyle italic
}

skinparam interface {
  BackgroundColor #F0F8FF
  BorderColor SECONDARY_COLOR
  BorderStyle dashed
}

skinparam enum {
  BackgroundColor #FFF8DC
  BorderColor ACCENT_COLOR
}
```

**Nota:** skinparam para class diagrams es **DIFERENTE** de Sequence y UC diagrams.

### 3.2 Centralización vs. Documentación

| Elemento | Centralizable | Método |
|----------|---|---|
| **Colores** | ✅ | skinparam class { } |
| **Estilos de paquete** | ⚠️ | `skinparam packageStyle rectangle` (global) |
| **Visibilidad (+/-)** | ❌ | Documentar en guidelines |
| **Separadores (.., ==, __)** | ❌ | Usar libremente (sin restricción) |
| **Dirección de flechas** | ❌ | Dejar a Graphviz (sin -left-, -right-, etc.) |
| **Hide/Remove logic** | ❌ | NO usar en documentación pública |

---

## 4. Naming & Auto-Explicidad

### 4.1 Convención Recomendada (Clean Code Principles)

**Para clases en IACT diagrams:**

| Tipo | Ejemplo | Recomendación |
|------|---------|---|
| **Entity/Model** | `User`, `Order`, `LineItem` | Sustantivo singular, simple |
| **Service** | `AuthService`, `OrderProcessor` | Sustantivo + sufijo Service/Processor |
| **Repository** | `UserRepository` | Sustantivo + sufijo Repository |
| **Abstract Base** | `AbstractEntity`, `BaseService` | Prefijo Abstract/Base |
| **Interface** | `Persistable`, `Validatable`, `Loggable` | Adjetivo + sufijo -able/-ible |
| **Enum** | `Status`, `Priority`, `Role` | Sustantivo singular |
| **Private fields** | `_internalState`, `_cache` | Prefijo _ (POSIX convention) |
| **Métodos privados** | `_processData()`, `_validateInput()` | Prefijo _ o convención Java |

**Principios:**
- ✅ Revela intención: `UserAuthenticationService` vs. `UAS` (NO abreviar)
- ✅ Pronunciable: `getUserByEmail()` vs. `getUsrByEml()`
- ✅ Buscable: nombres completos facilitan grep/search
- ✅ Longitud equilibrada: corresponde al scope (utilities < domain entities)
- ✅ Evitar trabajalenguas: `validateUserAuthenticationCredentialsProcessingService` es excesivo

### 4.2 Aplicabilidad a IACT

**Si IACT documenta clases, seguir:**
1. Nombres auto-explicativos (revelando intención)
2. Convención POSIX para privados: `_fieldName`
3. Sufijos estándar: Service, Repository, Factory, Handler
4. NO abreviaturas (excepto patrones conocidos: DAO, DTO, MVC)

---

## 5. Casos de Uso de Class Diagrams en IACT

### 5.1 Aplicables

**Caso A: Arquitectura técnica de módulos IACT**
```plantuml
package "Authentication Module" {
  class AuthService
  class CredentialValidator
  interface AuthProvider
}
```
✅ Útil si IACT documenta internals

**Caso B: Modelos de datos del dominio**
```plantuml
class User {
  - _id: UUID
  - _email: String
  - _roles: List<Role>
  + getPermissions(): Set<Permission>
}
```
✅ Útil si IACT especifica estructuras de datos

### 5.2 No Aplicables

**Caso C: Requisitos funcionales puros**
```plantuml
class "Login Requirement" {
  - email validation
  - password hashing
}
```
❌ Esto es UC, no class diagram

---

## 6. Validación: ¿Incluir Class Diagrams en IACT-docs?

### 6.1 Decision Tree

```
¿IACT documenta arquitectura técnica?
├─ SÍ → ¿Incluir class diagrams en Phase 7 design?
│  ├─ Crear ADR: adr-class-diagrams-applicability.md
│  ├─ Definir skinparam class en plantuml-styles.puml
│  └─ Documentar naming convention
└─ NO → Enfocarse solo en UC y Sequence diagrams
   └─ Omitir Class diagrams (no aplicable)
```

### 6.2 Preguntas para Usuario

**Antes de Phase 7 DESIGN/SPECIFY:**

1. ¿IACT-docs incluye documentación de arquitectura técnica interna?
2. ¿Necesita diagramas de estructura de clases Java/Python?
3. ¿Hay requisitos de documentación de modelos de datos?
4. ¿Qué convención prefiere para privados: `_field` (POSIX) vs. `field_` vs. sin prefijo?

---

## 7. Recomendaciones para Phase 1 Setup

### 7.1 Si se incluyen Class Diagrams

**Agregar a plantuml-styles.puml:**

```plantuml
' SECTION: CLASS DIAGRAM STYLING
' ================================

skinparam class {
  BackgroundColor SECONDARY_COLOR
  BorderColor PRIMARY_COLOR
  BorderThickness 2
  FontColor TEXT_COLOR
}

skinparam abstract {
  BackgroundColor #E0E0E0
  FontStyle italic
}

skinparam interface {
  BackgroundColor #F0F8FF
  BorderStyle dashed
}

skinparam enum {
  BackgroundColor #FFF8DC
}

skinparam package {
  BackgroundColor #FAFAFA
  BorderColor PRIMARY_COLOR
  Style rectangle
}

' Namespace separator
set namespaceSeparator ::
```

**Documentación de naming (guidelines):**

```
CLASS NAMING CONVENTION (IACT-docs):

Entidades:        User, Order, Product (sustantivo singular)
Servicios:        UserService, OrderProcessor
Repositorios:     UserRepository, OrderRepository
Interfaces:       Persistable, Validatable
Abstract bases:   AbstractEntity, BaseService
Enumeraciones:    Status, Priority, Role
Campos privados:  _field (POSIX convention, _prefix)
Métodos privados: _method() (POSIX convention, _prefix)

Restricciones:
- SIN abreviaturas (excepto patrones estándar: DAO, DTO)
- Revelar intención > brevedad
- Buscable y pronunciable
- Longitud = scope del elemento
```

### 7.2 Si se OMITEN Class Diagrams

- Documentar decisión en ADR: `adr-diagram-types-iact.md`
- Mantener enfoque en UC y Sequence diagrams
- Simplificar plantuml-styles.puml (omitir skinparam class)

---

## 8. Validación: Cobertura de PlantUML 1.2025.0

### 8.1 Class Diagrams Completamente Documentados ✅

| Sección | Contenido | Status |
|---------|----------|--------|
| 3.8 | Advanced class body (separators) | ✅ Documentado |
| 3.9-3.10 | Notes & stereotypes | ✅ Documentado |
| 3.11 | Note on field/method | ✅ Documentado |
| 3.12 | Note on links | ✅ Documentado |
| 3.13 | Abstract, interface, enum | ✅ Documentado |
| 3.14-3.18 | Hide/Remove/Show commands | ✅ Documentado |
| 3.19 | Generics | ✅ Documentado |
| 3.20 | Custom circle marker | ✅ Documentado |
| 3.21-3.24 | Packages & namespaces | ✅ Documentado |
| 3.25 | Interface Lollipop | ✅ Documentado |
| 3.26-3.28 | Arrows, associations, directions | ✅ Documentado |
| 3.29+ | Skinparam personalization | ⏳ Incompleto (cortado en guía) |

---

## 9. Síntesis: Class Diagrams para IACT-docs

### 9.1 Conclusión

**Class diagrams en PlantUML 1.2025.0:**
- ✅ Soporte completo para arquitectura orientada a objetos
- ✅ Separadores, notas, estereotipos, abstracciones bien documentados
- ✅ Paquetes y namespaces útiles para organización modular
- ⚠️ Hide/Remove commands no recomendable para documentación pública
- ⚠️ Naming convention crítica (auto-explicidad, equilibrio)

**Aplicabilidad a IACT:**
- **IF** documentar arquitectura técnica → Incluir con skinparam class
- **IF** solo requisitos funcionales → Omitir (usar UC/Sequence)

### 9.2 Decisión Recomendada

**Propuesta:**
1. Phase 1 Setup: Crear plantuml-styles.puml sin sección class (aún no decidido)
2. Phase 5 STRATEGY: Crear ADR sobre applicability de class diagrams
3. Phase 7 DESIGN: Decidir si incluir based en scope de IACT-docs
4. Phase 10 EXECUTE: Implementar skinparam class solo si aprobado

---

**Análisis Completado:** 2026-04-24 00:30:00  
**Hallazgo clave:** Class diagrams son opcionales; decision en Phase 5 STRATEGY  
**Confianza:** 0.95 (well documented in guide, clear decision tree)  
**Naming Principle:** Auto-explicidad + equilibrio = Clean Code adherence
