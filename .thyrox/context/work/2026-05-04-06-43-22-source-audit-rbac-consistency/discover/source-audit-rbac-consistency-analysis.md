```yml
created_at: 2026-05-04 06:47:23
project: IACT-docs
work_package: 2026-05-04-06-43-22-source-audit-rbac-consistency
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# Análisis DISCOVER — Auditoría RBAC consistency en source/

Objetivo: escanear todo `source/` para identificar inconsistencias respecto
a las decisiones tomadas en CIA-RBAC-002 + CNST-033 v2.0.0.

---

## 1. Alcance del scan

Archivos analizados: todos los `.rst` bajo `source/`.
Herramienta: `grep` con patrones por categoría de hallazgo.

Fecha del scan: 2026-05-04

---

## 2. Hallazgos

### F-01 — `HasFunctionPermission` en cnst-010 (CRÍTICO)

**Archivo:** `source/normativa/restricciones/cnst-010-permission-class-explicita-en-vistas-drf.rst`
**Líneas:** 74 y 87

```
permission class especifica (``HasFunctionPermission``, ...)
permission_classes (HasFunctionPermission custom)
```

**Problema:** `HasFunctionPermission` es el nombre INCORRECTO.
CIA-RBAC-002 DEC-005 y CNST-033 §4.3 establecen que el nombre canónico
es `FunctionPermission`. El patrón getter (`Has*`) es un anti-patrón
explícitamente documentado en CNST-033.

**Acción:** Reemplazar `HasFunctionPermission` → `FunctionPermission` en
ambas ocurrencias. Es un documento normativo — la inconsistencia es
especialmente dañina aquí.

**Severidad:** Alta

---

### F-02 — `FunctionCatalogCache` en uc-perm-03 (ACEPTABLE)

**Archivos:**
- `source/requisitos/casos-uso/permissions/uc-perm-03/implementacion-tecnica.rst` (línea 38)
- `source/requisitos/casos-uso/permissions/uc-perm-03/testing.rst` (líneas 68 y 183)

**Contexto:** `FunctionCatalogCache` es un componente de la previsualización
de permisos excepcionales (UC-PERM-03). Representa el cache de la consulta
al catálogo de funciones durante el cálculo de impacto SoD.

**Evaluación:** El nombre sigue las convenciones de CNST-033 §4.2:
- Usa concepto de dominio (`Function`) como prefijo — no abreviación
- `Catalog` identifica el concepto central
- `Cache` es un sufijo de patrón descriptivo y pronunciable

CNST-033 §4.2 no exige que todas las clases estén pre-listadas en el
catálogo — solo que el nombre siga las convenciones. `FunctionCatalogCache`
cumple. **No requiere cambio.**

**Severidad:** Ninguna (no es error)

---

### F-03 — `function_id` en múltiples UCs (ACEPTABLE)

**Archivos:** uc-acc-01, uc-acc-02, uc-perm-02, uc-perm-04, uc-perm-05,
uc-auth-01, uc-perm-06 (docenas de ocurrencias)

**Contexto:** `function_id` se usa como:
- Nombre de campo en modelos Django (`function_id: int` en dataclasses)
- Parámetro de API REST (`{"function_id": 1, ...}`)
- Identificador en criterios de aceptación y test scenarios

**Evaluación:** Estos usos son correctos. `function_id` es la clave primaria
de la tabla `Function` en el modelo de datos. Es correcto como campo de
modelo/API. CIA-RBAC-002 DEC-001 distingue entre:
- `function_id` → identificador de BD (FK en asignaciones, parámetros API)
- `name` (codename) → identificador de runtime para autorización

El error que se corrigió en los 3 archivos (T-006, T-007, T-008) era el
uso de `function_id` como argumento de `@require_function()` — contexto
de autorización donde el codename es el identificador correcto.

En UCs de acceso/asignación, `function_id` es el dato que mueve la
asignación en la base de datos. **No requiere cambio.**

**Severidad:** Ninguna (no es error)

---

### F-04 — `@require_function('manage_users')` en uc-perm-07/testing.rst (CORRECTO)

**Archivo:** `source/requisitos/casos-uso/permissions/uc-perm-07/testing.rst` (línea 172)
**Valor:** `'manage_users'` — codename válido en snake_case

**Evaluación:** Uso correcto. Codename en snake_case como exige DEC-001/DEC-002.
**No requiere cambio.**

---

### F-05 — Referencias a `adr-gob-009` en archivos legacy (ACEPTABLE)

**Archivos:**
- `source/backend/adr-back-005-middleware-decoradores-permisos.rst` (líneas 46, 527)
- `source/gestion/evidencia/rbac-historia/diseno-referencia-implementacion-permisos-legacy.rst` (línea 174)

**Contexto:** Frases como "supersedido por `adr-gob-009` en Z.1" donde
`adr-gob-009` = ADR-GOB-009 (RBAC Modelo Conceptual, Aprobado v1.2.0).
**No** es ADR-GOB-010 (DRF authorization). El número es correcto.

**Evaluación:** Referencias históricas válidas al ADR-GOB-009 existente.
**No requieren cambio.**

---

### F-06 — Sin markdown links en RST (LIMPIO)

Scan completo de RST para links tipo `[text](url)` o `(http://...)` en
contextos de código: **cero ocurrencias encontradas.**

Resultado del scan anterior al WP CIA-RBAC-002 ya eliminó todos los
markdown links. Los archivos nuevos (CIA-RBAC-002, ADR-GOB-010, CNST-033
v2.0.0) también están limpios.

---

### F-07 — Clases con nombres antiguos: RBACBackend, HasFunction (LIMPIO)

Scan de `RBACBackend`, `HasFunction`, `class Perm`, `Perm.` (como
atributo) en todo `source/` excluyendo archivos PlantUML y los archivos
que los documentan como anti-patrones:

**Cero ocurrencias fuera de contexto esperado.**

Los únicos `Perm` encontrados son aliases PlantUML (`as Perm`) en diagramas
UML — naming de UML legítimo, distinto al naming de Python.

---

## 3. Resumen ejecutivo

| ID | Hallazgo | Severidad | Acción |
|----|----------|-----------|--------|
| F-01 | `HasFunctionPermission` en cnst-010 (2 ocurrencias) | Alta | Corregir → `FunctionPermission` |
| F-02 | `FunctionCatalogCache` en uc-perm-03 | Ninguna | No requiere cambio |
| F-03 | `function_id` como campo/param de API | Ninguna | No requiere cambio |
| F-04 | `@require_function('manage_users')` | Ninguna | Correcto |
| F-05 | `adr-gob-009` en archivos legacy | Ninguna | Referencia válida |
| F-06 | Markdown links en RST | Ninguna | Limpio |
| F-07 | Clases con nombres legacy | Ninguna | Limpio |

**Un solo hallazgo accionable: F-01.**
La corrección es simple (2 ocurrencias en 1 archivo), pero es crítica
porque afecta un documento normativo (`cnst-010`) que define la convención
de uso de permission classes en DRF.

---

## 4. Conclusión

El estado del `source/` post-WP `cia-rbac-002-drf-integration` es
mayoritariamente consistente. El único error real (F-01) es una omisión
de la campaña de correcciones anterior: `cnst-010` no fue actualizado
cuando se renombró `HasFunctionPermission` → `FunctionPermission` en
CIA-RBAC-002 DEC-005.

El task plan se reduce a 1 corrección de contenido + commit.
```
