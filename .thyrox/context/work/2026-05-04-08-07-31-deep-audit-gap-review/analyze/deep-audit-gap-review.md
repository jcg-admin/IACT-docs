```yml
created_at: 2026-05-04 08:07:31
project: IACT-docs
work_package: 2026-05-04-08-07-31-deep-audit-gap-review
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Deep Audit — Revisión de Gaps Post-Migración

Análisis adversarial de lo que queda pendiente después de:
- MOD_Admin module creation (commit f804352)
- Phantom UC-043..047 replacement (commit 1cbc50f)
- Legacy MODULE-NNN → codename migration (commit 0c8fa7b)

Todo lo aquí clasificado como PROVEN fue verificado con grep ejecutado
en esta sesión.

---

## CATEGORÍA A — Phantom UC refs: RESUELTOS vs RESTANTES

### Resueltos (PROVEN)
Archivos con `UC-043..047` que fueron actualizados:
- `fr-010-02` ✓ · `fnd-03` ✓ · `fnd-04` ✓ · `fnd-05` (parcial) ✓
- `txm-01` ✓ · `mapeo-uc.rst` ✓ · `tpl-uc-casos-de-uso.rst` ✓
- `br-006` ✓ · `br-007` ✓

### Restantes (PROVEN — 17 ocurrencias en 6 archivos)

#### R-01 `rbac-core/responsabilidades.rst` + `rbac-core/casos-uso.rst`
**Veredicto: INTENCIONADO — contexto distinto, no phantom SoD**

El módulo rbac-core usa UC_043..047 para describir sus propias
responsabilidades con SEMÁNTICA DIFERENTE:
- UC_043 = "Asignar/retirar roles a usuarios" (≠ "Configurar SoD")
- UC_044 = "Configurar segmentos de datos"
- UC_045 = "Asignar permisos directos con vigencia"
- UC_046 = "Simular acceso de un usuario"
- UC_047 = "Generar matriz de roles/permisos"

Estas son UCs del módulo técnico RBAC_CORE (ARQ_MOD_003), numeradas
con el esquema secuencial antiguo (antes de domain-prefix). NO son las
phantom SoD UCs. **No deben cambiarse por UC_ADM_01 — serían falsas.**

**Acción correcta:** Mapear UC_043..047 de rbac-core a sus equivalentes
reales del catálogo de casos de uso:
- UC_043 (asignar/retirar) → UC_ACC_01/UC_ACC_02
- UC_044 (segmentos datos) → UC_ACC_04
- UC_045 (permisos directos) → UC_PERM_03
- UC_046 (simular acceso) → UC_ACC_03 (modo simulación)
- UC_047 (matriz roles) → UC_ACC_03 (modo lista)

**Severidad: MEDIA** — inconsistencia de nomenclatura, no error de contenido.

#### R-02 `fnd-05-jerarquia-4-niveles.rst` línea 351
**Veredicto: INCORRECTO — falta actualizar tabla de conteo**

```
MOD_Access 9 UC-010, UC-011, UC-041 a UC-047
```

Debería ser:
```
MOD_Access 7 UC-010, UC-011, UC-041, UC-042, UC_ACC_03, UC_ACC_05, UC_ACC_08, UC_ACC_09
MOD_Admin  3 UC_ADM_01, UC_ADM_02, UC_ADM_03
```

**Severidad: ALTA** — la tabla afirma 9 UCs de MOD_Access cuando ya
hay 13 módulos con UC_ADM separado.

#### R-03 `catalogo-funciones.rst` línea 149
**Veredicto: INCORRECTO — UC-044 es phantom**

```
view_assignments   UC-011, UC-044
```

UC-044 "Consultar Permisos Efectivos" fue el phantom → UC_ACC_03.
`view_assignments` ya está mapeada a UC_ACC_03 en la lógica. Debe ser:
```
view_assignments   UC-011, UC_ACC_03
```

**Severidad: ALTA** — el catálogo de funciones es el artefacto más
consultado por desarrolladores.

#### R-04 `gestion/evidencia/analisis-catalogo-modular-iact.rst` 
**Veredicto: PRESERVAR — documento de evidencia histórica**

Tipo: `Evidencia`. Registra un análisis de fase anterior.
Las referencias UC-043..047 allí son parte del análisis histórico,
no navegación activa. Cambiarlas alteraría la evidencia.
**No tocar.**

#### R-05 `proc-req-007-generacion-uc.rst`
**Veredicto: INCORRECTO — módulos desactualizados**

```
MOD_Access: UC_010 - UC_011, UC_041 - UC_047
```

El procedimiento de generación de UC debe reflejar el catálogo actual.
Debe actualizarse con MOD_Admin y la lista correcta de UCs de MOD_Access.

**Severidad: ALTA** — procedimiento normativo que guía la creación
de nuevos UCs.

---

## CATEGORÍA B — Legacy MODULE-NNN: RESUELTOS vs RESTANTES

### Resueltos (PROVEN)
- 5 bounded-context files ✓ · matriz-dependencias (clusters ACC/USR/AUTH/ALR) ✓
- sod.rst ✓ · grupos-funciones.rst ✓ · convenciones.rst ✓
- modulos/supervision/index.rst ✓ · fnd-00 ✓ · modelo-dominio ✓ · cnst-030 ✓

### Restantes (PROVEN — 12 ocurrencias en 7 archivos)

#### R-06 `matriz-dependencias-uc-iact.rst` — AUD/LOG/SUP clusters (líneas 631..810)
**Veredicto: INCORRECTO — misma migración sin completar**

El cluster ACC fue limpiado pero el AUD, LOG y SUP clusters en el mismo
archivo quedaron con el patrón `AUD-NNN \`\`codename\`\`` y `LOG-NNN \`\`codename\`\``.

```
AUD-001 ``view_audit_log``    → ``view_audit_log``
AUD-002 ``search_audit_log``  → ``search_audit_log``
AUD-003 ``export_audit_log``  → ``export_audit_log``
AUD-004 ``generate_compliance_report`` → ``generate_compliance_report``
LOG-001 ``view_application_logs`` (rename Z.2 D-05) → ``view_application_logs`` (rename Z.2 D-05)
LOG-002..007 ``codename``     → ``codename``
SUP-001 ``monitor_live_calls`` → ``monitor_live_calls``
SUP-002/003 idem
```

Y en la sección de notas de T-03 (línea 209):
```
OPR-02/05/06 (call state changes) y SUP-02 (barge-in)
→ OPR-02/05/06 (call state changes) y ``barge_in_calls``
```

**Severidad: ALTA** — es el mismo archivo que ya fue parcialmente
migrado; dejar AUD/LOG/SUP con IDs crea inconsistencia interna.

#### R-07 `catalogo-funciones.rst` línea 647
**Veredicto: CASO BORDE — compliance note técnica**

```
SUP-001 (monitor_live_calls) y SUP-002 (barge_in_calls) generan
notificación audible...
```

Aquí el ID aparece junto al codename — patrón de claridad. No es
incorrecto per se, pero es inconsistente con el resto. Puede
eliminarse el prefijo: `\`\`monitor_live_calls\`\` y \`\`barge_in_calls\`\``.

**Severidad: BAJA** — legible como está.

#### R-08 `cnst-020-throttling.rst` línea 152
**Veredicto: INCORRECTO**

```
Aplica throttling en exportación de logs (CNST-024 + LOG-002)
```

LOG-002 = `export_logs`. Debe ser: `CNST-024 + \`\`export_logs\`\``.

**Severidad: MEDIA** — restricción activa que desarrolladores consultan.

#### R-09 `tpl-br-decision-tipo.rst` línea 583 y 564
**Veredicto: PRESERVAR — entidad, no función**

```sql
WHERE recipient_id = 'SUP-001'
```

SUP-001 aquí es un valor de base de datos (supervisor_id), NO una
función RBAC. Es un ejemplo de cómo usar un business rule template
con datos concretos. Cambiar 'SUP-001' a `\`\`barge_in_calls\`\`` sería
semánticamente incorrecto.

#### R-10 `breq-006` y `breq-004` — sin ocurrencias de IDs de función
**Veredicto: FALSO POSITIVO** — la búsqueda inicial identificó estos
archivos pero el grep refinado no encuentra IDs activos de función
(los que existían son BRQ-MODULE-NNN que son IDs de business requirements).

---

## CATEGORÍA C — MOD_Admin: integración incompleta

### C-01 UC specs: solo Parte 1 (informacion-general)
**PROVEN** — `ls` de los directorios confirma:
```
uc-adm-01/: diagramas-uml/, index.rst, informacion-general.rst
```
Faltan: actores-precondiciones, criterios-aceptacion, datos-involucrados,
excepciones, flujo-principal, flujos-alternos, implementacion-tecnica,
patrones-diseno, requisitos-no-funcionales, testing.rst (× 3 UCs = 30 archivos)

**Severidad: ALTA** — cualquier desarrollador que navegue a uc-adm-01
encontrará el UC incompleto vs. los 9 UCs de access/permissions completos.

### C-02 MOD_Admin no aparece en arquitectura-sistema.rst ni despliegue-multicliente.rst
**INFERRED** — el gap-analysis menciona que esas dos referencias existen,
pero como referencias implícitas a un módulo sin definición formal. Ahora
que MOD_Admin está definido, esas referencias deberían actualizar sus
contextos para apuntar a la definición formal.

**Severidad: BAJA** — las referencias siguen siendo válidas (apuntan a algo
que ya existe).

### C-03 No existe FR para `manage_function_catalog`
**INFERRED** — el catálogo declara la función como nueva v5.6.0, pero no
hay `fr-*-manage-function-catalog.rst` en `requisitos-funcionales/`.

**Severidad: MEDIA** — sin FR no hay criterios de aceptación formales
para implementar la función.

---

## CATEGORÍA D — Inconsistencias introducidas por los cambios

### D-01 fnd-03 tabla de módulos: módulo count inconsistente
En fnd-03 se cambió la fila de MOD_Access a 7 UCs pero el total
de la tabla podría no cuadrar si hay otras filas de conteo.
**Requiere verificación.**

### D-02 fnd-04 etiqueta `.. _uc-adm-01:` duplicada
En `fnd-04-trazabilidad.rst` se creó `.. _uc-adm-01:` en un bloque de
código inline (`::` block), mientras que el label real está en
`casos-uso/admin/uc-adm-01/index.rst`. El label en fnd-04 está dentro
de un bloque de código — Sphinx NO lo registrará como anchor real.

**Veredicto:** No hay conflicto — el label dentro de `::` es texto plano,
no una directiva RST activa. La referencia `:ref:\`uc-adm-01\`` resuelve
correctamente al `index.rst` del UC.

### D-03 `view_assignments` en `UC-011, UC_ACC_03` (mapeo-uc.rst)
La función `view_assignments` ahora tiene `UC-011, UC_ACC_03` — mezclando
el formato numérico antiguo con el domain-prefixed nuevo. Inconsistente
con el resto del catálogo.

**Severidad: BAJA** — UC-011 es un ID real (existe en casos-uso/access/
como domain ID), no un phantom.

---

## RESUMEN: ACCIONES PENDIENTES PRIORITIZADAS

### Prioridad ALTA (corregir inmediatamente)

| ID | Archivo | Cambio |
|----|---------|--------|
| R-02 | `fnd-05-jerarquia-4-niveles.rst:351` | `MOD_Access 9 UC-041 a UC-047` → corregir con MOD_Admin |
| R-03 | `catalogo-funciones.rst:149` | `UC-044` → `UC_ACC_03` |
| R-05 | `proc-req-007-generacion-uc.rst:158` | actualizar lista MOD_Access + añadir MOD_Admin |
| R-06 | `matriz-dependencias-uc-iact.rst` AUD/LOG/SUP | strip MODULE-NNN prefix (11 líneas) |
| C-01 | `admin/uc-adm-01/02/03/` | 30 archivos de spec faltantes |

### Prioridad MEDIA (corregir en el sprint)

| ID | Archivo | Cambio |
|----|---------|--------|
| R-01 | `rbac-core/responsabilidades.rst` + `casos-uso.rst` | mapear UC_043..047 a domain IDs correctos |
| R-08 | `cnst-020:152` | `LOG-002` → `\`\`export_logs\`\`` |
| C-03 | nuevos FR | crear FR para `manage_function_catalog` |

### Prioridad BAJA (deuda técnica documentada)

| ID | Archivo | Cambio |
|----|---------|--------|
| R-07 | `catalogo-funciones.rst:647` | eliminar `SUP-001` prefix |
| D-03 | `mapeo-uc.rst` | `UC-011` → verificar si debe ser `UC_ACC_?` |
| C-02 | `arquitectura-sistema.rst` | añadir referencia formal a mod-admin.rst |

### PRESERVAR (no cambiar)

| ID | Archivo | Razón |
|----|---------|-------|
| R-04 | `analisis-catalogo-modular-iact.rst` | evidencia histórica |
| R-09 | `tpl-br-decision-tipo.rst` | entity ID en SQL, no function ID |
| `adr-gob-009` changelog | rename history | registro histórico |
| `cia-rbac-002 §14` | AUTH-001 ejemplo negativo | argumento técnico |
```
