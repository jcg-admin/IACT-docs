```yml
created_at: 2026-05-05 14:35:00
project: IACT-docs
work_package: 2026-05-05-14-30-00-uml07-conformance-deep-analysis
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Catálogo de errores — uml-07 conformance

14 errores tipificados, ordenados por severidad.

----

## E-01 (BLOCKER) — UCs incluidos aparecen como standalone (viola R-07)

**Regla violada:** R-07 — un UC incluido NUNCA aparece
solo.

**Instancias:**

- ``use-case-view/reports/uc-inc-rpt-01/index.rst``
  existe como diagrama standalone con
  ``Operator --> UC_INC_RPT_01``. Pero ``UC_INC_RPT_01
  Resolver Segmento`` es un **UC included-only**
  invocado por todos los UC_RPT_NN. Per R-07 NO debe
  tener diagrama propio ni ser invocado por actor.

**Impacto:** documentación contradice principio canónico.
Un lector formado en uml-07 detecta el error.

----

## E-02 (BLOCKER) — Diagramas per-UC no muestran inclusiones (viola R-06 + R-11)

**Regla violada:** R-06 (`<<include>>`) + R-11
(profundización con UCs incluidos).

**Instancias:** los **83 archivos per-UC** generados son
singletons triviales:

```
actor AccessAdmin
rectangle "MOD_Access" {
  usecase "UC_ACC_01\nAsignar Funciones" as UC_ACC_01
}
AccessAdmin --> UC_ACC_01
```

Pero ``UC_ACC_01`` realmente incluye:
- Validar User destino
- Validar funciones (existen + activas)
- Filtrar idempotente
- Validar SoD (CNST-005)
- Persistir N Assignments
- Invalidar cache permisos
- AuditEvent FUNCTIONS_ASSIGNED

NINGUNO aparece en mi diagrama.

**Impacto:** los stubs no aportan información útil.
Triple duplicación con cero valor agregado.

----

## E-03 (BLOCKER) — Diagramas per-UC no muestran extensiones (viola R-08)

**Regla violada:** R-08.

**Instancias:** ningún archivo per-UC muestra relaciones
``<<extend>>``. Por ejemplo:

- ``uc-rpt-04/index.rst`` (Exportar Reporte) extiende
  UC_RPT_03, pero el diagrama no lo muestra.
- ``uc-rpt-09/index.rst`` (Configurar Filtros) extiende
  UC_RPT_03 — no shown.
- ``uc-acc-08/index.rst`` (Otorgar Permiso Temporal
  Excepcional) extiende UC_ACC_01 — no shown.

----

## E-04 (BLOCKER) — UCs base con extension points sin marcar (viola R-09)

**Regla violada:** R-09 — UC base muestra "..extension
points.." en su label.

**Instancias en diagramas module-level:**

- ``uc-reports/index.rst``: ``UC_RPT_03 Ver Reportes
  Históricos`` recibe `<<extend>>` desde UC_RPT_04,
  UC_RPT_07, UC_RPT_09. Su label NO muestra los
  extension points.
- ``uc-access/index.rst``: ``UC_ACC_01 Asignar
  Funciones`` recibe extend de UC_ACC_08. Sin marca.
- ``uc-pipeline/index.rst``: ``UC_PIP_01`` recibe
  extends de UC_PIP_02 y EJECUCION_AUTO. Sin marca.
- ``uc-audit/index.rst``: ``UC_AUD_01``, ``UC_AUD_02``
  reciben extends. Sin marca.
- ``uc-supervision/index.rst``: ``UC_SUP_01`` recibe
  extend de UC_SUP_02. Sin marca.
- ``uc-caller/index.rst``: ``UC_CLI_02`` y ``UC_CLI_03``
  reciben extends. Sin marca.
- ``uc-logs/index.rst``: ``UC_LOG_01``, ``UC_LOG_02``
  reciben extends. Sin marca.

**Sintaxis correcta esperada:**

```
usecase "UC_RPT_03\nVer Reportes Historicos\n.. extension points ..\nFiltrar / Exportar / Programar" as UC_RPT_03
```

----

## E-05 (MAJOR) — Falta actor BENEFICIARIO (viola R-01)

**Regla violada:** R-01 — actor receptor a la derecha.

**Instancias:** la mayoría de diagramas solo muestran
actor INICIADOR. Casos donde falta el beneficiario:

- ``uc-reports``: el reporte se entrega ¿a quién? Operator
  inicia y consume — same actor. Pero ``Supervisor``
  iniciador de exportación entrega el archivo a un
  **destinatario externo** (cliente, equipo) no
  modelado.
- ``uc-access``: ``UC_ACC_01 Asignar Funciones`` —
  iniciador AccessAdmin, beneficiario es el **User
  destino** (no modelado en el diagrama).
- ``uc-permissions``: idem.
- ``uc-supervision``: ``UC_SUP_03 Enviar Mensaje al
  Equipo`` — sí modela ``Operator`` como receiver
  (correcto). Pero ``UC_SUP_01 Monitorear`` y
  ``UC_SUP_02 Barge-in`` afectan al ``Operator`` y
  al ``Caller`` (3-way) — no modelado.

----

## E-06 (MAJOR) — Generalización entre UCs ausente (viola R-10)

**Regla violada:** R-10 — herencia entre UCs con `--|>`.

**Instancias candidatas en el corpus IACT:**

- ``UC_RPT_12..17`` (los 6 reportes específicos:
  Agentes, Colas, Campañas, Transferencias, Menús IVR,
  Clientes Únicos) son **especializaciones** de un UC
  abstracto "Ver Reporte Especifico". Cada uno hereda la
  estructura común (período, segmento, aplicación de
  filtros) y agrega su lógica propia.
- ``UC_USR_01..04`` Crear/Modificar/Consultar/Eliminar son
  CRUD sobre User — podrían heredar de UC abstracto
  "Operación de Catálogo de Usuarios".
- ``UC_ACC_01/02/04/05/08`` operaciones de modificación
  RBAC — todas heredan "Operación de RBAC con auditoría
  obligatoria" (P-09 audit-or-abort).

Ningún diagrama actual modela estas generalizaciones.

----

## E-07 (MAJOR) — Detalles de implementación en diagramas (viola R-12)

**Regla violada:** R-12 — análisis ≠ implementación.

**Instancias:**

- ``uc-reports/index.rst`` v2: ya REMOVÍ los
  ``(sp_rpt_centros_xsegmento)`` etc. (correcto).
- Sin embargo, los stubs per-UC nuevos en ``reports/``
  no contienen detalles SQL — OK aquí.
- ``uc-pipeline.rst`` (now ``pipeline/index.rst``)
  contiene ``Ejecutar Pipeline\nAutomatico`` que es
  detalle, no UC formal de actor — borderline aceptable
  como UC interno orquestado por Scheduler.
- Las **notas** dentro de los diagramas mencionan
  codenames RBAC (``view_dashboard``, ``export_csv``).
  R-12 estricta diría que esto es implementación. Sin
  embargo, las notas son anotaciones, no parte del
  modelo del UC mismo. Borderline aceptable porque la
  trazabilidad RBAC es parte del análisis funcional
  (no detalle técnico de Python/SQL).

**Decisión:** las notas de codenames RBAC se quedan
(trazabilidad funcional). Otros detalles de
implementación (nombres de SP, tablas SQL) NO.

----

## E-08 (MAJOR) — Diagramas per-UC son stubs duplicados sin valor (consecuencia E-02 + E-03)

**Hallazgo derivado:** dado E-02 y E-03, los 83 archivos
per-UC son stubs sin contenido útil más allá del que ya
provee:

1. ``casos-uso/<module>/<uc>/index.rst`` (spec textual)
2. ``casos-uso/<module>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst``
   (diagrama per-UC con includes/extends ya presentes)
3. ``use-case-view/<module>/index.rst`` (vista módulo)

**Impacto:** triplicación de información, mantenimiento
×3. Cualquier cambio requiere editar 3 lugares.

----

## E-09 (MAJOR) — Casos-uso per-UC diagrams ya tienen mejor contenido (no aprovechado)

**Hallazgo:** ``casos-uso/<module>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst``
ya contiene per-UC diagram con includes/extends. Por
ejemplo ``uc-acc-01`` muestra:

```
UC_ACC_01 ..> VALIDAR_USUARIO_DESTINO : <<include>>
UC_ACC_01 ..> VALIDAR_FUNCIONES : <<include>>
UC_ACC_01 ..> VALIDAR_SOD : <<include>>
... (7 inclusiones)
```

Mi WP previo IGNORÓ este contenido y creó stubs vacíos.
Lo correcto era:

- O **aprovechar** estos diagramas existentes
  (vincularlos vía ``:doc:`` o copiar el ``@startuml``)
- O **mover** estos diagramas de casos-uso a
  use-case-view (Kruchten 4+1: diagramas en use-case-view,
  specs textuales en casos-uso)

----

## E-10 (MINOR) — Nombres de archivo no descriptivos (Clean Code)

**Hallazgo:** los archivos generados se llaman
``uc-acc-01/index.rst`` etc. Nombre del directorio
``uc-acc-01`` no revela intent.

**Cita libro (R-X):** UCs labeled como
"Reabastecer", "Crear una propuesta" — descriptivo.

**Instancias:** los 83 directorios ``uc-XXX-NN/``.

**Atenuante:** preserva trazabilidad al ID canónico de
casos-uso. Trade-off vs Clean Code.

----

## E-11 (MINOR) — Falta jerarquía de UCs en panorámica (subexplotación R-11)

**Regla:** R-11 — modelo detallado a partir de UCs de
alto nivel.

**Hallazgo:** no existe un **diagrama de alto nivel del
sistema completo IACT** mostrando los UCs operativos
clave por dominio (similar al ejemplo
``ejemplo-iact-diagrama-de-alto-nivel.rst`` de
``_metodologia-aplicacion``). El index de
use-case-view solo lista módulos sin un diagrama
panorámico cross-module.

----

## E-12 (MINOR) — Falta diagrama de jerarquía de actores

**Regla:** R-05 — actores en jerarquía de generalización.

**Hallazgo:** la jerarquía
``User <|-- Operator <|-- Supervisor <|-- ...`` se
introduce parcialmente en algunos módulos pero no existe
un **diagrama dedicado** mostrando el árbol completo de
actores del sistema. Este diagrama es estándar en
uml-07 (``comprension-de-los-usuarios.rst``).

----

## E-13 (MINOR) — Falta diagrama de "El panorama" UML elements

**Regla:** ``el-panorama.rst`` — diagrama de elementos
UML usados en el sistema.

**Hallazgo:** este diagrama del libro es opcional pero
útil para onboarding. No está en use-case-view.
Aplicabilidad discutible — quizá pertenece a
``base-cognitiva``, no a ``arquitectura-tecnica``.

----

## E-14 (MINOR) — Diagrama "Comprensión del dominio" ausente

**Regla:** ``comprension-del-dominio.rst`` — diagrama de
clases del dominio (no UCs sino clases).

**Hallazgo:** este es un diagrama de **clases**, no de
UCs. No pertenece a use-case-view (sería
domain-model). Use-case-view OK sin él.

**Atenuante:** corresponde a ``domain-model/`` que ya
está poblado con 68+ clases. No hay error.

----

## E-16 (BLOCKER) — Jerarquía de actores viola BR-006 Flat NIST

**Regla violada:** BR-006 RBAC Flat NIST + CNST-005:

> NIST RBAC. NO existe jerarquia de roles.
> Flat: Sin jerarquia de herencia entre roles.

**Conflicto con uml-07 R-05:** uml-07/comprension-de-los-usuarios.rst recomienda mostrar usuarios en jerarquía de generalización. **Para IACT esta regla NO aplica** — la restricción de dominio (BR-006 + CNST-005) prevalece sobre la recomendación didáctica del libro.

**Instancias detectadas:** 19 usos de `<|--` entre actores en module-level diagrams + panorama + jerarquía. Específicamente:

- `auth/index.rst`: UnauthUser <|-- AuthUser <|-- SystemAdmin
- `users/index.rst`: User <|-- UserAdmin
- `access/index.rst`: User <|-- AccessAdmin, Auditor
- `permissions/index.rst`: idem
- `pipeline/index.rst`: User <|-- PipelineAdmin, Auditor
- `reports/index.rst`: Operator <|-- Supervisor
- `alerts/index.rst`: Operator <|-- Supervisor
- `panorama-iact.rst`: Operator <|-- Supervisor
- `jerarquia-actores.rst`: árbol completo (era el caso peor)

**Causa raíz adicional:** "Operator", "Supervisor" son **títulos de RH**, no entidades RBAC. Para IACT importan las **funciones** (codenames atómicos), no los títulos. Un usuario marcado como "Supervisor" simplemente tiene asignados más AGRs (002+003+004+005) que un "Operator" (001) — sin herencia.

**Fix aplicado:** todas las 19 líneas `<|--` removidas de @startuml blocks. `jerarquia-actores.rst` renombrado a `mapa-funciones-rbac.rst` con diagrama función-céntrico (User → AGR → Function, plano).

----

## Resumen severidad

| ID | Sev | Categoría | Cantidad |
|----|-----|-----------|----------|
| E-01 | BLOCKER | UC included como standalone | 1 (UC_INC_RPT_01) |
| E-02 | BLOCKER | Sin includes en per-UC | 83 archivos |
| E-03 | BLOCKER | Sin extends en per-UC | 83 archivos |
| E-04 | BLOCKER | Extension points no marcados | ~10 module diagrams |
| E-05 | MAJOR | Falta actor beneficiario | varios |
| E-06 | MAJOR | Sin generalización UC | 0 modelados |
| E-07 | MAJOR | Detalles implementación | resuelto en v2 |
| E-08 | MAJOR | Stubs duplicados sin valor | 83 archivos |
| E-09 | MAJOR | Diagramas casos-uso desaprovechados | 83 instancias |
| E-10 | MINOR | Nombres no descriptivos | 83 dirs |
| E-11 | MINOR | Falta panorámica IACT | 1 diagrama |
| E-12 | MINOR | Falta jerarquía actores | 1 diagrama |
| E-13 | MINOR | Falta "el panorama" UML | 1 diagrama (opcional) |
| E-14 | — | Falta dominio (N/A para use-case-view) | OK |

**Errores BLOCKER total:** 4 categorías, ~177 instancias.
**Errores MAJOR total:** 5 categorías.
**Veredicto general:** los WPs previos NO lograron
conformance uml-07 — produjeron forma estructural sin
fondo semántico.
