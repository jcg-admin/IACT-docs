```yml
created_at: 2026-05-04 07:34:39
project: IACT-docs
work_package: 2026-05-04-07-25-32-uc-numbering-conflict
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Análisis de Gaps — MOD_Admin (módulo faltante)

## Qué se encontró al mapear los phantom UCs

Al intentar resolver los phantom UC-043..047 contra los dominios
existentes, emergió un patrón más significativo: **no existe módulo
de administración del modelo RBAC**. Hay un hueco arquitectónico
entre "asignar accesos a usuarios" (ACC/PERM) y "definir qué accesos
existen" (sin módulo).

---

## Los tres planos del RBAC en IACT

```
PLANO 1 — IDENTIDAD (¿Eres tú?)
  MOD_Auth: login, sesión, contraseña

PLANO 2 — CONFIGURACIÓN (¿Qué accesos EXISTEN?)
  MOD_Admin: catálogo de funciones, grupos del sistema, reglas SoD
  ← ESTE PLANO NO EXISTE FORMALMENTE

PLANO 3 — ASIGNACIÓN (¿Quién TIENE qué?)
  MOD_Access: assign/revoke funciones, agrupadores, permisos excepcionales
  MOD_Permissions: grupos custom, verificación runtime, menú dinámico
```

---

## Evidencia de los gaps (PROVEN)

### Gap 1 — `create_separation_rule` no existe

El catálogo tiene:
- `view_separation_rules` — ver reglas configuradas
- `update_separation_rule` — actualizar parámetros de una regla existente
- `disable_separation_rule` — toggle on/off

**Falta:** `create_separation_rule` — crear una nueva regla SoD. Las 3
reglas actuales (SOD-001..003) son estáticas. No hay mecanismo formal
para añadir una 4ª regla desde la aplicación.

### Gap 2 — No existe gestión del catálogo de funciones

Las 74 funciones se administran editando RST/migraciones — no existe
función RBAC que permita a un admin gestionar el catálogo desde la UI.
Funciones que faltarían: `manage_function_catalog` o equivalente.

### Gap 3 — `update_separation_rule` y `disable_separation_rule` sin UC

Ambas funciones son NUEVAS en v5.4.0 (split SRP de ACC-005). El catálogo
las declara pero NO existen UCs que las implementen:

```
source/requisitos/casos-uso/access/
  uc-acc-01, uc-acc-02, uc-acc-03, uc-acc-04, uc-acc-05, uc-acc-08, uc-acc-09
  ← uc-acc-06 y uc-acc-07 no existen
```

### Gap 4 — MOD_Admin referenciado pero no definido

`arquitectura-sistema.rst:38` menciona MOD_Admin como destino post-login.
`despliegue-multicliente.rst:67` lo muestra en el diagrama de despliegue.
**No existe** `source/arquitectura-tecnica/uc-module-view/mod-admin.rst`.

---

## Mapeo correcto de los phantom UCs

| Phantom | Nombre | Resolución |
|---------|--------|-----------|
| UC-043 | Configurar SoD | **Split**: view → `uc-acc-05`; full lifecycle → `uc-adm-01` |
| UC-044 | Consultar Permisos Efectivos | Existe como `uc-acc-03` |
| UC-045 | Gestionar Catálogo AGR | Nuevo: `uc-adm-03` |
| UC-046 | Gestionar Catálogo Funciones | Nuevo: `uc-adm-02` |
| UC-047 | Auditar Cambios de Permisos | Existe como `uc-acc-09` |

---

## Propuesta: MOD_Admin — Administración del Modelo RBAC

### Definición

**MOD_Admin** es el plano de **configuración del modelo RBAC**: gestiona
QUÉ funciones, grupos y reglas SoD EXISTEN en el sistema — anterior e
independiente de a QUIÉN se asignan (ACC) o de cómo se verifican en
runtime (PERM).

**Actor principal:** `admin_sistema` (AGR-009) — rol de mayor privilegio
técnico. A diferencia de `admin_seguridad` (AGR-008) que opera sobre
asignaciones, `admin_sistema` opera sobre el modelo mismo.

### UCs del nuevo módulo

| ID | Nombre | Funciones RBAC requeridas |
|----|--------|--------------------------|
| `uc-adm-01` | Gestionar Ciclo de Vida de Reglas SoD | `view_separation_rules`, `create_separation_rule` (NUEVA), `update_separation_rule`, `disable_separation_rule` |
| `uc-adm-02` | Gestionar Catálogo de Funciones | `manage_function_catalog` (NUEVA) |
| `uc-adm-03` | Gestionar Catálogo de Agrupadores del Sistema | `assign_functions_to_group` (reutilizada) + scope AGR-001..012 |

### Nuevas funciones RBAC requeridas (2)

| Codename | Módulo | Descripción |
|----------|--------|-------------|
| `create_separation_rule` | ACC (extend) | Crea nueva regla SoD con par de funciones incompatibles |
| `manage_function_catalog` | ADM (nueva) | CRUD sobre definiciones de funciones atómicas |

---

## Impacto en la numeración de phantom UCs

Con MOD_Admin definido, las referencias a "UC-043 Configurar SoD"
se resuelven así en la documentación:

- En BR-007 §5.3: `UC-043` → `uc-acc-05` (view) + `uc-adm-01` (lifecycle)
- En BR-006 §5.3: `UC-044` → `uc-acc-03`; `UC-045` → `uc-adm-03`;
  `UC-046` → `uc-adm-02`
- En todos los demás documentos: reemplazar referencias numéricas por
  IDs de dominio

No se asignan números globales secuenciales a los nuevos UCs de ADM —
el patrón del proyecto es usar IDs de dominio (uc-acc-*, uc-perm-*,
uc-adm-*) en casos-uso/ y requisitos-funcionales/.
