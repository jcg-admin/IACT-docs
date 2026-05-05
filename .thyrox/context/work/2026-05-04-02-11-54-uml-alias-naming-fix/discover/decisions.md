```yml
created_at: 2026-05-04 02:11:54
project: IACT-docs
work_package: 2026-05-04-02-11-54-uml-alias-naming-fix
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# Decisiones autónomas — uml-alias-naming-fix

---

## D-ALIAS-001 — Regla de alias auto-documentados en PlantUML

**Decisión:** Todo alias en diagramas PlantUML del proyecto IACT debe
ser auto-documentado. Al leer una flecha (`X -> Y : mensaje`), el lector
debe entender quiénes son X e Y sin necesidad de buscar la declaración.

**Criterios obligatorios:**
1. Mínimo 3 caracteres
2. Refleja el nombre/rol del participante de forma reconocible
3. Preferencia: nombre completo en CamelCase o snake_case
4. Abreviatura solo si es universalmente reconocible en el contexto

**Ejemplos:**

```
CORRECTO:
actor "view_reports" as view_reports       ← igual al nombre
participant "AuthEndpoint" as AuthEndpoint ← nombre completo
participant "SegmentResolver" as SegmentResolver
participant ":GUI" as GUI                  ← patrón del libro de referencia
participant ":SistemaOp" as SisOp          ← abreviatura reconocible

PROHIBIDO:
actor "view_reports" as U                  ← 1 letra
actor "view_reports\n(view_dashboard)" as RVG  ← acrónimo críptico
participant "AuthEndpoint" as AE           ← 2 letras
participant "DashboardEndpoint" as DE      ← 2 letras crípticas
participant "SegmentResolver" as SR        ← 2 letras crípticas
```

**Justificación:** El material de referencia `uml-09-diagramas-secuencias.rst`
muestra el patrón correcto: `as GUI`, `as CPU`, `as SO` (SistemaOp),
`as TV` (TarjetaVideo). Los aliases son reconocibles porque guardan
correspondencia directa con el nombre de la entidad. El código de los
diagramas es documentación — debe ser legible sin glosario.

---

## D-ALIAS-002 — Alias de actores RBAC usan el nombre de función exacto

**Decisión:** Para actores que representan funciones RBAC, el alias es
el nombre exacto de la función del catálogo (en snake_case):

```
actor "view_reports" as view_reports        ← función RBAC exacta
actor "assign_functions" as assign_functions
actor "request_pipeline_retry" as request_pipeline_retry
```

Cuando el actor tiene múltiples funciones en la etiqueta, usar la
función principal (la que da nombre al UC) como alias:

```
actor "view_reports\n(view_dashboard)" as view_reports  ← función principal
actor "assign_functions\n(create_users)" as assign_functions
```

**Justificación:** D-DIAG-001 ya establece que actores usan nombres
exactos de función RBAC. Esta decisión extiende la regla al alias.
Un alias como `RVG` (¿Report Viewer Group?) no es auto-documentado.
`view_reports` sí lo es.

---

## D-ALIAS-003 — Alias de participantes de sistema usan CamelCase del nombre

**Decisión:** Los participantes (clases, servicios, componentes) usan
CamelCase sin espacios como alias:

```
participant "AuthEndpoint" as AuthEndpoint
participant "DashboardEndpoint" as DashboardEndpoint
participant "SegmentResolver" as SegmentResolver
participant "ServicioReportes" as ServicioReportes
participant "DisparadorETL" as DisparadorETL
```

Para nombres con spaces/puntuación, eliminar los caracteres especiales:

```
participant "Interfaz de Acceso" as InterfazDeAcceso
object ":User (RBAC group)" as UserRBAC
```

**Justificación:** CamelCase es convención estándar para identificadores
de código/pseudocódigo. Mantiene correspondencia clara con el nombre
de la entidad.
