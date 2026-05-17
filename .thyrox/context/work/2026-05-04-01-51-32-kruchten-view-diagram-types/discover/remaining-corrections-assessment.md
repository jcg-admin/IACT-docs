```yml
created_at: 2026-05-04 02:30:00
project: IACT-docs
work_package: 2026-05-04-01-51-32-kruchten-view-diagram-types
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# Remaining Corrections Assessment

Resultado del análisis de agente Explore sobre el estado actual de
`source/` tras las correcciones de esta sesión.

---

## Issues confirmados pendientes

### P-001 — Technology names en UC diagramas-uml.rst (3 archivos)

| Archivo | Línea | Violación |
|---------|-------|-----------|
| `requisitos/casos-uso/auth/uc-auth-01/diagramas-uml.rst` | 70 | `participant "LoginView\n(Django)"` |
| `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml.rst` | 77 | `database "audit_log\n(PostgreSQL)"` |
| `requisitos/casos-uso/logs/uc-log-02/diagramas-uml.rst` | 35,48 | `"MariaDB"` en diagrama de actividades |

**Acción:** Reemplazar con nombres de rol semántico (Servicio de Autenticacion,
Repositorio de Auditoria, Almacen de Datos).

---

### P-002 — diagramas-uml-sistema.rst §7–§11 (adaptación pendiente)

- Archivo: `source/arquitectura-tecnica/diagramas-uml-sistema.rst`
- §7 State Machine, §8 Sequence, §9 Communication, §10 Component, §11 Deployment
- Estos diagramas necesitan adaptación desde el dominio healthcare al dominio IACT
- Build anterior reportó errors en línea 3 y línea 48 (PlantUML syntax errors)

**Acción:** Leer y reescribir §7–§11 con diagramas IACT correctos.

---

### P-003 — modulos/etl-monitoring/diagramas.rst (tech name)

- Archivo: `source/arquitectura-tecnica/modulos/etl-monitoring/diagramas.rst`
- Línea 17: `participant "sp_etl_maestro\n(MariaDB)"` — mezcla nombre de SP con tecnología

**Acción:** En diagramas arquitectónicos (arquitectura-tecnica/) sí se
permiten nombres concretos. Este caso puede quedar como está o refactorizar
a `participant "Servicio ETL\n(sp_etl_maestro)"` para consistencia visual.

---

### P-004 — uc-perm-05/excepciones.rst title underline

- Archivo: `source/requisitos/casos-uso/permissions/uc-perm-05/excepciones.rst`
- Warning RST: "Title underline too short" en líneas 13/13
- Necesita verificación y corrección de la longitud del underline

**Acción:** Leer el archivo y ajustar el underline del título.

---

### P-005 — vis-reports/diagramas.rst PlantUML error

- Archivo: `source/arquitectura-tecnica/modulos/vis-reports/diagramas.rst`
- Build reportó PlantUML error en línea 28
- Requiere lectura y corrección de la sintaxis del diagrama

**Acción:** Leer el archivo, identificar el error en línea 28 y corregir.

---

## Issues NO prioritarios (aceptables en contexto)

- `arquitectura-sistema.rst`: Referencias a MariaDB/PostgreSQL son CORRECTAS
  en documentos de arquitectura técnica (D-ETL-005: en `arquitectura-tecnica/`
  sí se pueden usar nombres concretos).
- Cross-references en `.. seealso::` de DesignView/ProcessView: ya se
  verificaron y apuntan a archivos existentes.

---

## Prioridad de corrección

| P | Issue | Impacto | Esfuerzo |
|---|-------|---------|---------|
| P-002 | diagramas-uml-sistema §7–§11 | Alto (build errors) | Alto |
| P-005 | vis-reports diagramas.rst | Alto (build error) | Bajo |
| P-004 | uc-perm-05 title underline | Medio (RST warning) | Bajo |
| P-001 | UC diagramas-uml.rst tech names | Medio (narrativa) | Bajo |
| P-003 | etl-monitoring tech name | Bajo (arch doc) | Bajo |
