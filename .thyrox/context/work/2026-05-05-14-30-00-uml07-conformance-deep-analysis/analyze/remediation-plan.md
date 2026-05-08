```yml
created_at: 2026-05-05 14:40:00
project: IACT-docs
work_package: 2026-05-05-14-30-00-uml07-conformance-deep-analysis
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Plan de remediación — uml-07 conformance

Plan ordenado por dependencia + severidad. Ejecutable en
4 fases.

----

## Decisión arquitectónica fundamental (raíz de errores)

Antes de ejecutar fixes, **resolver una decisión
estructural** que dispara cascada de errores:

### Opción A — use-case-view es ÚNICO dueño de diagramas UC

- Mover los `diagrama-de-caso-de-uso.rst` de
  ``casos-uso/<module>/<uc>/diagramas-uml/`` a
  ``use-case-view/<module>/<uc>/`` o
  ``use-case-view/<module>/<descriptive-name>.rst``.
- ``casos-uso/`` queda con specs textuales solamente
  (sin diagramas UC; mantiene actividad/secuencia/estado).
- Use-case-view hereda diagramas RICH (con includes,
  extends, actor beneficiario, extension points marcados).

**Pros:**
- Single source of truth (Kruchten 4+1: vista UC tiene
  todos los diagramas UC).
- Sin duplicación.
- Aprovecha el contenido ya creado en casos-uso (no
  hay que reinventar inclusiones).

**Cons:**
- Ruptura de muchos `:doc:` refs en casos-uso/<uc>/
  diagramas-uml/index.rst.
- Refactor pesado.

### Opción B — use-case-view solo agrega module-level + xrefs

- Eliminar los 83 stubs per-UC creados (están vacíos,
  E-08).
- Use-case-view solo tiene 13 module-level diagrams
  (los reescritos uml-07).
- Cada module-level link via `:doc:` a casos-uso/<uc>/
  diagramas-uml/diagrama-de-caso-de-uso.rst para detalle
  per-UC.

**Pros:**
- Cero duplicación.
- Aprovecha el contenido existente sin moverlo.
- Refactor mínimo.

**Cons:**
- Use-case-view tiene menos contenido propio.
- "Vista de casos de uso" no es self-contained.

### Recomendación: **Opción B**

Justificación: los diagramas per-UC ya viven en casos-uso
con includes/extends correctos. Duplicarlos o moverlos
añade riesgo. Use-case-view aporta valor con la **vista
agregada por módulo** + xrefs. Esto resuelve E-01, E-02,
E-03, E-08, E-09, E-10 de un solo movimiento.

----

## Fase 1 — Eliminar stubs vacíos (BLOCKER)

**Resuelve:** E-01, E-02, E-03, E-08, E-09, E-10.

1. Borrar los 83 archivos
   ``use-case-view/<module>/uc-XXX-NN/index.rst`` y los
   subdirs ``uc-XXX-NN/``.
2. Quitar la toctree "Casos de uso del módulo" de los 13
   ``use-case-view/<module>/index.rst``.
3. Reemplazar con una **sección de cross-references** que
   linkea a ``casos-uso/<module>/<uc>/index.rst`` y a
   ``casos-uso/<module>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst``.

----

## Fase 2 — Marcar extension points en module diagrams (BLOCKER)

**Resuelve:** E-04.

Aplicar sintaxis R-09 a los UCs base que reciben
`<<extend>>`:

```
usecase "UC_RPT_03\nVer Reportes Historicos\n.. extension points ..\nFiltrar / Exportar / Programar" as UC_RPT_03
```

**Archivos a editar:**

| Archivo | UC base | Extension points |
|---------|---------|------------------|
| ``reports/index.rst`` | UC_RPT_03 | Filtrar, Exportar, Programar |
| ``access/index.rst`` | UC_ACC_01 | Permiso temporal |
| ``pipeline/index.rst`` | UC_PIP_01 | Ver errores, Ejecución auto |
| ``audit/index.rst`` | UC_AUD_01 | Buscar |
| ``audit/index.rst`` | UC_AUD_02 | Exportar |
| ``alerts/index.rst`` | UC_ALR_02 | Reconocer |
| ``alerts/index.rst`` | UC_ALR_05 | Ver alerta |
| ``supervision/index.rst`` | UC_SUP_01 | Barge-in |
| ``caller/index.rst`` | UC_CLI_02 | Esperar cola |
| ``caller/index.rst`` | UC_CLI_03 | Recibir callback |
| ``logs/index.rst`` | UC_LOG_01 | Buscar |
| ``logs/index.rst`` | UC_LOG_02 | Buscar |

----

## Fase 3 — Actor beneficiario donde aplique (MAJOR)

**Resuelve:** E-05.

Modelar el receptor donde semánticamente exista:

| Diagrama | UC | Beneficiario a agregar |
|----------|----|------------------------|
| ``access/index.rst`` | UC_ACC_01/02/04/08 | ``TargetUser`` (User destino) |
| ``permissions/index.rst`` | UC_PERM_01/02/03/04 | ``TargetUser`` |
| ``users/index.rst`` | UC_USR_01..04 | ``TargetUser`` |
| ``supervision/index.rst`` | UC_SUP_01/02 | ``Operator`` (ya hay UC_SUP_03) |

Sintaxis: ``UC --> TargetUser`` (flecha sale del UC).

----

## Fase 4 — Generalización entre UCs (MAJOR)

**Resuelve:** E-06.

Modelar las jerarquías que aporten clarity:

### En reports/index.rst

```
usecase "UC_RPT_BASE\nVer Reporte Especifico" as UC_RPT_BASE <<abstract>>

UC_RPT_12 --|> UC_RPT_BASE
UC_RPT_13 --|> UC_RPT_BASE
UC_RPT_14 --|> UC_RPT_BASE
UC_RPT_15 --|> UC_RPT_BASE
UC_RPT_16 --|> UC_RPT_BASE
UC_RPT_17 --|> UC_RPT_BASE
```

### En access/index.rst

UCs con auditoría obligatoria heredan de UC abstracto
"Operación RBAC con audit-or-abort".

----

## Fase 5 — Diagramas panorámicos (MINOR)

**Resuelve:** E-11, E-12.

### Crear ``use-case-view/panorama-iact.rst``

Diagrama de alto nivel del sistema completo (referencia:
``ejemplo-iact-diagrama-de-alto-nivel.rst``).

### Crear ``use-case-view/jerarquia-actores.rst``

Diagrama dedicado a la generalización de actores:

```
User <|-- Operator <|-- Supervisor
User <|-- UserAdmin
User <|-- AccessAdmin
User <|-- Auditor
User <|-- PipelineAdmin
User <|-- SystemAdmin
Caller (independiente — actor externo)
Scheduler, IvrSwitch, AlertEngine (sistemas)
```

Actualizar ``use-case-view/index.rst`` toctree para
incluir estos dos.

----

## Orden de ejecución recomendado

1. **Fase 1** primero (elimina ruido — stubs vacíos).
2. **Fase 2** (extension points en module diagrams).
3. **Fase 3** (actores beneficiarios).
4. **Fase 4** (generalización UCs — opcional, valida con
   ejecutor si aporta o complica).
5. **Fase 5** (panorámicos — bonus).

Cada fase con commit independiente para trazabilidad.

----

## Validación post-remediación

Audit script que verifique cada regla:

```python
for diagram in all_use_case_view_diagrams:
    assert no_standalone_included_uc(diagram)        # R-07
    assert if_extends_then_extension_point(diagram)  # R-09
    assert no_implementation_details(diagram)        # R-12
    assert at_least_one_actor(diagram)               # R-01
    assert system_boundary_present(diagram)          # R-03
```

----

## Decisiones pendientes del ejecutor

1. **Aprobar Opción B** (eliminar 83 stubs) vs Opción A
   (mover diagramas de casos-uso). Recomendación: B.
2. Aprobar la lista de extension points de Fase 2 (12
   UCs base identificados).
3. Aprobar las jerarquías de generalización propuestas
   en Fase 4 (UC_RPT_BASE, etc.) — pueden ser
   sobre-modelado.
4. Aprobar diagramas panorámicos de Fase 5 (panorama
   completo + jerarquía actores).
