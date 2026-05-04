```yml
created_at: 2026-05-04 07:45:00
project: IACT-docs
work_package: 2026-05-04-06-15-52-cia-rbac-002-drf-integration
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# Análisis de Errores — CNST-033 v1.0.0

Documento: `source/normativa/restricciones/cnst-033-vocabulario-unificado-rbac.rst`
Versión analizada: 1.0.0 (2026-04-29)

---

## 1. Alcance insuficiente

### E-001 — El documento solo cubre "Funcion vs Capacidad"

**Severidad:** Alta

La v1.0.0 define únicamente que el término canónico es "Funcion"
(no "Capacidad") y provee una tabla de equivalencias
(Function, FunctionGroup, SeparationOfDutiesRule, etc.).

**Qué falta:**
- No define el formato de codenames (`snake_case` obligatorio)
- No define el formato de `function_id` (`{MODULO}-{NNN}`)
- No define convenciones de nombres para módulos Python
- No define convenciones de nombres para clases Python
- No tiene catálogo canónico de codenames por módulo
- No tiene catálogo de grupos ni de reglas SoD
- No tiene tabla de transformaciones español→inglés

**Evidencia:** Los errores en `analisis-errores-modelo-rbac-v5-2-0.rst`
incluyen `@require_function('RPT-001')` (uso de `function_id` en
lugar de codename) — error que CNST-033 v1.0.0 no cubre porque no
especifica qué es un codename ni cuál es su formato.

---

## 2. Errores en metadata

### E-002 — Clasificación insuficiente

**Severidad:** Baja

`:clasificacion: Alto`

El vocabulario canónico RBAC es transversal a todo el sistema.
Un error en él afecta código, base de datos, documentación y tests
simultáneamente. La clasificación correcta es `Critico`.

### E-003 — Tipo incorrecto

**Severidad:** Baja

`:tipo: Restriccion`

El estándar del proyecto usa el valor completo. Debería ser
`:tipo: Restriccion Normativa` para consistencia con otros CNST.

---

## 3. Ausencia del catálogo canónico

### E-004 — Sin catálogo de codenames

**Severidad:** Alta

La v1.0.0 menciona ejemplos sueltos (`view_own_sessions`,
`view_reports`) pero no tiene el catálogo completo de los 37
codenames del modelo RBAC v5.2.1 organizados por módulo.

**Consecuencia:** No es posible verificar si un codename es
canónico sin consultar el modelo de datos directamente.

### E-005 — Sin catálogo de grupos

**Severidad:** Media

Los 10 `FunctionGroup` del modelo v5.2.1 (`basic_operator_group`,
`report_viewer_group`, etc.) no están listados. El documento
define el formato del nombre pero no qué nombres son válidos.

### E-006 — Sin catálogo de reglas SoD

**Severidad:** Media

Las 3 `SeparationRule` del modelo v5.2.1 no están listadas.
Mismo problema que E-005.

---

## 4. Ausencia de convenciones Python

### E-007 — Sin convenciones de módulos Python

**Severidad:** Alta

No existe ninguna regla sobre cómo nombrar módulos Python
en el sistema RBAC. Esto permitió nombres como `rbac/` (acrónimo
de implementación) en lugar de `permissions/` (concepto de dominio)
y `permissions_registry.py` en lugar de `catalog.py`.

### E-008 — Sin convenciones de clases Python

**Severidad:** Alta

No existe ninguna regla sobre cómo nombrar clases Python.
Esto permitió nombres como:
- `RBACBackend` (acrónimo + mecanismo) en lugar de `FunctionAuthorization`
- `Perm` (abreviación no pronunciable) en lugar de `FunctionCatalog`
- `HasFunction` (patrón getter) en lugar de `FunctionPermission`
- `drf_permissions.py` (ruido técnico) en lugar de `enforcement.py`

**Evidencia directa:** CIA-RBAC-002 §9.2 documenta 6 renombrados
necesarios, todos causados por ausencia de esta convención en CNST-033.

---

## 5. Referencia incorrecta en §6.2

### E-009 — Referencia a procedimiento inexistente

**Severidad:** Baja

```rst
:doc:`/normativa/procedimientos/proc-req-015-excepciones-cnst`
```

Este archivo no existe en el repositorio (verificado con `find`).
La referencia produce un error de build Sphinx.

---

## 6. Tabla de transformaciones ausente

### E-010 — Sin tabla español→inglés

**Severidad:** Media

La v1.0.0 establece que el código debe estar en inglés pero no
provee la tabla de transformaciones que documente cómo se
tradujo cada término al corregir `MODELO_RBAC_IACT_v5.2.0`.

**Consecuencia:** Un implementador nuevo no sabe que `graficos`
→ `charts` (no `graphics`), que `etl` → `pipeline` (no `etl`),
o que `auditoria` → `audit_log` (con `log` explícito). Estas
decisiones quedan implícitas en el historial de git, no en el
documento normativo.

---

## Resumen

| ID | Error | Severidad | Cubierto por v2.0.0 |
|----|-------|-----------|---------------------|
| E-001 | Alcance limitado a Funcion vs Capacidad | Alta | Sí — §§3-9 |
| E-002 | Clasificación `Alto` en lugar de `Critico` | Baja | Sí |
| E-003 | Tipo `Restriccion` incompleto | Baja | Sí |
| E-004 | Sin catálogo de codenames | Alta | Sí — §5 |
| E-005 | Sin catálogo de grupos | Media | Sí — §6 |
| E-006 | Sin catálogo de reglas SoD | Media | Sí — §7 |
| E-007 | Sin convenciones de módulos Python | Alta | Sí — §4.1 |
| E-008 | Sin convenciones de clases Python | Alta | Sí — §§4.2-4.3 |
| E-009 | Referencia a procedimiento inexistente | Baja | Sí (eliminada) |
| E-010 | Sin tabla de transformaciones | Media | Sí — §8 |

**Total: 4 errores de severidad Alta, 3 Media, 3 Baja.**

La v2.0.0 cubre todos los errores identificados. Es un reemplazo
completo y no un parche — el documento crece de 9 secciones a 11
y de ~300 líneas a ~500 líneas.
