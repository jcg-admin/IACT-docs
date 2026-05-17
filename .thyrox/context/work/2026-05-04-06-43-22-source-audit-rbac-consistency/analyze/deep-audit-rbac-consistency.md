```yml
created_at: 2026-05-04 07:21:55
project: IACT-docs
work_package: 2026-05-04-06-43-22-source-audit-rbac-consistency
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Deep Audit — RBAC Consistency (Segunda Pasada)

Análisis adversarial de segunda pasada sobre `source/`. La primera
pasada corrigió `HasFunctionPermission`, eliminó MODULE-NNN function_ids
en 29 archivos, y corrigió `GranularPermission` en adr-back-006.

Esta segunda pasada examina consistencia semántica entre documentos:
cross-references, conteos declarados, vocabulario SQL/Python, e
identidad de UCs referenciados.

---

## Hallazgos

### F-01 — CRÍTICO: `br-006` §5.1 referencia CNST erróneo

**Archivo:** `source/requisitos/reglas-negocio/br-006-rbac-flat-nist.rst:167`

**Evidencia (PROVEN):**

```
* - :ref:`cnst-012`
  - Modelo RBAC Flat consolidado: 74 funciones, 12 grupos, 3 reglas SoD,
    permisos temporales con vencimiento. Implementa esta BR.
```

`cnst-012` es **"Validación de Input via Serializer"** (serializadores DRF).
La descripción corresponde exactamente a `cnst-029` (**"RBAC Modelo Plano"**).

**Fix:** `:ref:\`cnst-012\`` → `:ref:\`cnst-029\``

---

### F-02 — CRÍTICO: `br-006` §4.2 declara AGR-001..010 — hay 12 AGRs

**Archivo:** `source/requisitos/reglas-negocio/br-006-rbac-flat-nist.rst:144`

**Evidencia (PROVEN):**

```
- **Roles**: Todos los agrupadores RBAC (AGR-001 a AGR-010)
```

`grupos-funciones.rst` lista 12 entradas: AGR-001..AGR-012 (verificado con
`grep -c "^ \* - \*\*AGR-"` → 12). El claim "AGR-001 a AGR-010" está
desactualizado — el modelo v5.5.0 tiene AGR-011 y AGR-012.

**Fix:** `AGR-001 a AGR-010` → `AGR-001 a AGR-012`

---

### F-03 — CRÍTICO: `br-007` §7 ejemplos SoD completamente incorrectos

**Archivo:** `source/requisitos/reglas-negocio/br-007-separacion-funciones-sod.rst:228-230`

**Evidencia (PROVEN — comparación directa contra cnst-030):**

Texto actual en br-007:
```
SOD_001: create_users vs assign_functions
SOD_002: view_audit_log vs export_audit_log
SOD_003: view_pipeline_status vs request_pipeline_retry
```

Definición real en `cnst-030` (fuente de verdad):
- **SOD-001** `pipeline_audit_separation`: Pipeline (view_pipeline_status,
  view_pipeline_errors, view_data_availability, request_pipeline_retry)
  **vs** Audit (view_audit_log, search_audit_log, export_audit_log,
  generate_compliance_report)
- **SOD-002** `user_audit_separation`: Users (create_users, deactivate_users,
  list_users, unblock_users) **vs** Audit (view_audit_log, search_audit_log,
  export_audit_log)
- **SOD-003** `access_audit_separation`: Access (assign_functions,
  revoke_functions, view_separation_rules) **vs** Audit (view_audit_log,
  search_audit_log)

Los ejemplos actuales de br-007 son factualmente erróneos en las tres reglas:
- `SOD_001: create_users vs assign_functions` — ninguna de las dos funciones
  pertenece a SOD-001. `create_users` es lado Users de SOD-002;
  `assign_functions` es lado Access de SOD-003.
- `SOD_002: view_audit_log vs export_audit_log` — ambas son funciones de
  Audit, están del mismo lado de SOD-002 (lado derecho).
- `SOD_003: view_pipeline_status vs request_pipeline_retry` — ambas son
  funciones de Pipeline, están del mismo lado de SOD-001 (lado izquierdo).

Este error fue introducido durante la migración MODULE-NNN → codenames: el
mapeo `USR-001 → create_users, ACC-001 → assign_functions` fue correcto en
términos de vocabulario, pero los ejemplos originales ya tenían la semántica
equivocada respecto a qué regla SoD ilustraban.

**Fix:** Reemplazar §7 completo con ejemplos correctos y nombres canónicos:
```
SOD_001 (pipeline_audit_separation):
  view_pipeline_status vs view_audit_log

SOD_002 (user_audit_separation):
  create_users vs view_audit_log

SOD_003 (access_audit_separation):
  assign_functions vs view_audit_log
```

---

### F-04 — CRÍTICO: UC-043 conflicto de identidad

**Archivos:** múltiples

**Evidencia (PROVEN):**

`br-007` §3.2 y §5.3 referencian UC-043 como **"Configurar SoD"**:
```
- **Proceso de Cambio**: Configuracion via UC-043
* - UC-043
  - Configurar SoD - definir restricciones
```

`fnd-03-casos-de-uso.rst` idem: `UC-043: Configurar SoD`

Pero el directorio real es:
```
source/requisitos/requisitos-funcionales/reports/uc-043-reporte-campanas/
```

`uc-043-reporte-campanas/index.rst` declara: **"FR-043: Reporte de Campañas"**
derivado de UC_RPT_14.

Hay dos UCs distintos usando el número 43:
- UC-043 en dominio reports = Reporte de Campañas
- UC-043 en referencias de br-007/fnd-03 = Configurar SoD (sin archivo propio)

**Alcance limitado de este audit:** la resolución del conflicto de numeración
requiere decisión arquitectónica sobre el plan de numeración de UCs. Se
registra como hallazgo para ADR o tarea de renumeración. NO se corrige
automáticamente.

---

### F-05 — MEDIO: `glosario.rst` usa nombre SQL legacy español

**Archivo:** `source/base-cognitiva/glosario.rst:438`

**Evidencia (PROVEN):**

```
``usuario_tiene_permiso(user_id, function_code)`` y la
variante ``verificar_permiso_y_auditar``
```

Nombre canónico per `adr-back-006` §2.3:
```
user_has_function(p_user_id, p_function_code)
check_function_and_audit(p_user_id, p_function_code)
```

**Fix:** `usuario_tiene_permiso` → `user_has_function`;
`verificar_permiso_y_auditar` → `check_function_and_audit`

---

### F-06 — MEDIO: `analisis-dominio.rst` usa nombre SQL legacy español

**Archivo:** `source/requisitos/_metodologia-aplicacion/analisis-dominio.rst:561`

**Evidencia (PROVEN):**

```
→ SQL nativa usuario_tiene_permiso()
```

Mismo caso que F-05. Este archivo es un documento de metodología de
análisis orientado a objetos — usa el nombre para ilustrar el dominio.

**Fix:** `usuario_tiene_permiso()` → `user_has_function()`

---

### F-07 — BAJO: `br-006` §3.1 `CNST_005` no es "DRF Security Checklist"

**Archivo:** `source/requisitos/reglas-negocio/br-006-rbac-flat-nist.rst:105`

**Evidencia (PROVEN):**

```
* - **Documento**
  - CNST_005_Seguridad_DRF_Checklist
* - **Tipo Fuente**
  - CNST + Estandar NIST
```

CNST-005 real: **"Timeout de Sesión de 15 Minutos"** — no es un "DRF
Security Checklist". El campo `Documento` en §3.1 es texto libre (no
`:ref:`), por lo que puede referirse a un documento histórico pre-corpus.
Idem en `br-007` §3.1.

**Impacto:** bajo — es un campo de metadata de origen histórico, no una
referencia técnica activa. Se registra como deuda documental.

---

### F-08 — INFORMACIONAL: Vocabulario de modelos Django en docs metodológicos

**Archivos:** `analisis-dominio.rst`, `relaciones-uml.rst` (múltiples líneas)

Los documentos de metodología `_metodologia-aplicacion/` usan en diagramas
UML nombres como `ReglaSoD`, `PermisoExcepcional`, `AuditoriaPermiso`.

Per `adr-back-006` §2.4 los nombres canónicos Django son `SeparationRule`,
`ExceptionalGrant`, `FunctionAccessAudit`.

**Evaluación:** estos documentos son guías de enseñanza de UML para el
equipo, no especificaciones de implementación. Los diagramas usan nombres
conceptuales en español para claridad pedagógica. Se considera aceptable
mientras el documento de referencia técnica (`bounded-context-rbac.rst`)
use los nombres canónicos — lo cual es el caso.

**Excepción:** `bounded-context-rbac.rst` usa `ExceptionalPermission` en
lugar de `ExceptionalGrant`. Esto sí afecta un documento arquitectónico.
Requiere verificación de cuál nombre está consolidado entre `adr-back-006`
(`ExceptionalGrant`) y UC docs (`ExceptionalPermission`) — hay uso extensivo
de `ExceptionalPermission` en `uc-perm-04` y `uc-perm-07`, lo que sugiere
que puede ser el nombre de dominio más establecido. Se marca como PENDIENTE
DE DECISIÓN, no se corrige sin ADR.

---

## Resumen ejecutivo

| ID | Severidad | Archivo | Descripción | Accionable |
|----|-----------|---------|-------------|-----------|
| F-01 | CRÍTICO | br-006 §5.1 | `:ref:\`cnst-012\`` debería ser cnst-029 | Sí |
| F-02 | CRÍTICO | br-006 §4.2 | AGR count: "AGR-001 a AGR-010" → debería ser AGR-012 | Sí |
| F-03 | CRÍTICO | br-007 §7 | Ejemplos SoD factualmente erróneos en las 3 reglas | Sí |
| F-04 | CRÍTICO | br-007 + fnd-03 | UC-043 = "Configurar SoD" vs real uc-043 = Reportes | ADR requerido |
| F-05 | MEDIO | glosario.rst | `usuario_tiene_permiso` → `user_has_function` | Sí |
| F-06 | MEDIO | analisis-dominio.rst | `usuario_tiene_permiso()` → `user_has_function()` | Sí |
| F-07 | BAJO | br-006/007 §3.1 | CNST_005 no es "DRF Security Checklist" | Deuda documental |
| F-08 | INFO | metodologia docs | Modelo Django: nombres pedagógicos vs canónicos | Pendiente ADR |

**Hallazgos críticos accionables:** F-01, F-02, F-03, F-05, F-06
**Hallazgos que requieren decisión:** F-04 (UC renumeración), F-08 (ExceptionalPermission)
**Conteo verificado:** 74 funciones en catálogo (PROVEN: `grep -c "^ \* - \`"` = 74), 12 AGRs

---

## Notas de análisis

### Origen de F-03

El error en br-007 §7 fue introducido durante la migración MODULE-NNN →
codenames de la sesión anterior. El mapeo de códigos fue correcto
(`USR-001 → create_users`, `ACC-001 → assign_functions`), pero los ejemplos
originales ya eran semánticamente incorrectos — ilustraban funciones de lados
opuestos incorrectos de las reglas SoD. Al renombrar se preservó el error
de fondo.

### Vocabulario SQL canónico (referencia)

Per `adr-back-006` §2.3 (tabla completa):

| Legacy (español) | Canónico (inglés) |
|-----------------|-------------------|
| `usuario_tiene_permiso()` | `user_has_function()` |
| `obtener_capacidades_usuario()` | `get_user_functions()` |
| `obtener_grupos_usuario()` | `get_user_groups()` |
| `verificar_permiso_y_auditar()` | `check_function_and_audit()` |
