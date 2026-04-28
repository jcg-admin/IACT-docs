```yml
created_at: 2026-04-28 23:06:00
project: IACT-docs
work_package: 2026-04-28-05-28-45-source-rebuild-requisitos
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Inventory UC v4.0.0 — 40 UCs Canónicos IACT

## Nota de método

Este inventario cruza el **catálogo canónico v4.0.0** (40 UCs del prompt
ejecutor) contra los archivos `.rst` reales en
`temp-backup/source-2026-04-28/requisitos/casos_uso/`. Hallazgos:

- Los 40 archivos `UC_<MOD>_NN_<nombre>.rst` existen en el repo. IDs y módulos
  coinciden con el catálogo. Metadata de cada RST (`:normativa:`, actor, BReq,
  CNST en flujo) se extrajo verbatim.
- **Discrepancia de títulos** detectada en módulos RPT y ALR: los títulos del
  catálogo del prompt no coinciden con los títulos del RST canónico v4.0.0.
  Ejemplo: `UC_RPT_01` en el catálogo del prompt = "Consultar Reporte
  Trimestral"; en el RST = "Ver Dashboard". Se reportan **ambos** títulos por
  UC. La fuente de verdad técnica son los RST (cabecera `.. meta:: :version:
  4.0.0`).
- Mapeo legacy v2.0 → v4.0.0 referenciado en `PLAN_MAESTRO_Actualizacion_
  Referencias_v4_0_0_SIN_EMOJIS.md` indica equivalencias parciales (UC-010 →
  UC_ACC_01, UC-043 → UC_ACC_05, UC-001..003 → UC_AUTH_01..03, UC-050 →
  UC_PIP_01). El plan no provee tabla 1:1 exhaustiva para los 40 UCs; los
  legacy IDs no listados se marcan "(no documentado en inputs)".
- Flujos principales (5 pasos numerados) NO se transcriben aquí — viven en
  cada RST sección 5 "Flujo Normal (Camino Feliz)". El inventario referencia
  el path. Esto preserva el budget de prosa (≤800 palabras) y evita duplicar.
- Nomenclatura CNST usada en RST es `CNST-NNN` (3 dígitos con guion). El
  prompt menciona `CNST_001..CNST_031` (SRP-31, 31 constraints). Se reportan
  los CNST citados en cada RST verbatim. La conciliación SRP-31 ↔ CNST-NNN es
  fuera de scope de este inventario.

## Tabla resumen — 40 UCs

| ID v4.0.0 | Título catálogo (prompt) | Título RST (real) | Módulo | Actor primario | CNST citados |
|-----------|--------------------------|-------------------|--------|----------------|--------------|
| UC_USR_01 | Crear Usuario | Crear Usuario | USR | AGR-006 agr_admin_usuarios | CNST-001, 005, 009 |
| UC_USR_02 | Consultar Usuarios | Consultar Usuarios | USR | AGR-006 agr_admin_usuarios | CNST-009 |
| UC_USR_03 | Modificar Usuario | Modificar Usuario | USR | AGR-006 agr_admin_usuarios | CNST-001, 005, 009 |
| UC_USR_04 | Eliminar Usuario | Eliminar Usuario | USR | AGR-006 agr_admin_usuarios | CNST-005, 009 |
| UC_ACC_01 | Asignar Funciones | Asignar Funciones | ACC | AGR-007 agr_admin_acceso | CNST-005, 009 |
| UC_ACC_02 | Revocar Funciones | Revocar Funciones | ACC | AGR-007 agr_admin_acceso | CNST-005, 009 |
| UC_ACC_03 | Consultar Permisos | Consultar Permisos | ACC | AGR-007 agr_admin_acceso | CNST-005 |
| UC_ACC_04 | Asignar Agrupador | Asignar Agrupador | ACC | AGR-007 agr_admin_acceso | CNST-005, 009 |
| UC_ACC_05 | Gestionar SoD | Gestionar SoD | ACC | AGR-007 agr_admin_acceso | CNST-005, 009 |
| UC_ACC_06 | Gestionar Segmentos | Gestionar Segmentos | ACC | AGR-007 agr_admin_acceso | CNST-005, 009 |
| UC_ACC_07 | Asignar Segmento | Asignar Segmento | ACC | AGR-007 agr_admin_acceso | CNST-005, 009 |
| UC_ACC_08 | Permiso Temporal | Permiso Temporal | ACC | AGR-007 agr_admin_acceso | CNST-005, 009 |
| UC_ACC_09 | Auditar Cambios Acceso | Auditar Cambios Acceso | ACC | AGR-008 agr_auditor | CNST-009 |
| UC_RPT_01 | Consultar Reporte Trimestral | Ver Dashboard | RPT | AGR-001 agr_operador_basico | CNST-003, 004 |
| UC_RPT_02 | Consultar Problemas Menu | Ver Métricas Tiempo Real | RPT | AGR-001 agr_operador_basico | CNST-003, 004 |
| UC_RPT_03 | Consultar Transferencias | Ver Reportes Históricos | RPT | AGR-002 agr_operador_reportes | CNST-003, 004, 006 |
| UC_RPT_04 | Filtrar Por Fecha | Exportar CSV | RPT | AGR-004 agr_exportador | CNST-004, 007, 009 |
| UC_RPT_05 | Filtrar Por Centro | Exportar Excel | RPT | AGR-004 agr_exportador | CNST-004, 007, 009 |
| UC_RPT_06 | Exportar CSV | Exportar PDF | RPT | AGR-004 agr_exportador | CNST-004, 007, 009 |
| UC_RPT_07 | Exportar Excel | Programar Reporte | RPT | AGR-003 agr_supervisor | CNST-001, 004, 009 |
| UC_RPT_08 | Exportar PDF | Ver Reportes Programados | RPT | AGR-003 agr_supervisor | CNST-004 |
| UC_RPT_09 | Ver Dashboard | Configurar Filtros | RPT | AGR-003 agr_supervisor | CNST-004, 009 |
| UC_RPT_10 | Ver KPIs | Guardar Vista | RPT | AGR-002 agr_operador_reportes | CNST-004 |
| UC_RPT_11 | Ver Tendencias | Compartir Reporte | RPT | AGR-003 agr_supervisor | CNST-001, 004, 009 |
| UC_RPT_12 | Ver Gráfico Hora | Ver Reporte Agentes | RPT | AGR-003 agr_supervisor | CNST-003, 004 |
| UC_RPT_13 | Ver Gráfico Día | Ver Reporte Colas | RPT | AGR-003 agr_supervisor | CNST-003, 004 |
| UC_RPT_14 | Ver Distribución Centro | Ver Reporte Campañas | RPT | AGR-003 agr_supervisor | CNST-003, 004 |
| UC_ALR_01 | Configurar Alerta | Configurar Umbrales | ALR | AGR-005 agr_gestor_alertas | CNST-004, 009 |
| UC_ALR_02 | Consultar Alertas | Ver Alertas Activas | ALR | AGR-001 agr_operador_basico | CNST-001, 003, 004 |
| UC_ALR_03 | Pausar Alerta | Reconocer Alerta | ALR | AGR-003 agr_supervisor | CNST-001, 009 |
| UC_ALR_04 | Eliminar Alerta | Ver Historial Alertas | ALR | AGR-003 agr_supervisor | CNST-003, 004, 006 |
| UC_ALR_05 | Gestionar Destinatarios | Gestionar Suscripciones | ALR | AGR-005 agr_gestor_alertas | CNST-001, 004, 009 |
| UC_PIP_01 | Disparar ETL | Supervisar ETL | PIP | AGR-009 agr_admin_pipeline | CNST-003, 009 |
| UC_PIP_02 | Consultar Errores ETL | Consultar Errores ETL | PIP | AGR-009 agr_admin_pipeline | CNST-003, 009 |
| UC_PIP_03 | Consultar Disponibilidad | Consultar Disponibilidad | PIP | AGR-009 agr_admin_pipeline | CNST-003 |
| UC_PIP_04 | Solicitar Reintento | Solicitar Reintento | PIP | AGR-009 agr_admin_pipeline | CNST-003, 009 |
| UC_AUD_01 | Consultar Auditoría | Consultar Auditoria | AUD | AGR-006 agr_auditor | CNST-009, 010 |
| UC_AUD_02 | Generar Reporte Compliance | Buscar Auditoria | AUD | AGR-006 agr_auditor | CNST-009, 010 |
| UC_AUD_03 | Exportar Auditoría | Exportar Auditoria | AUD | AGR-006 agr_auditor | CNST-007, 009, 010 |
| UC_AUD_04 | Registrar Evento | Generar Reporte Compliance | AUD | AGR-006 agr_auditor | CNST-009, 010 |

## Detalle por módulo

Cada bloque debajo cita: ID v4.0.0, título RST canónico, ID legacy v2.0
(según mapeo PLAN_MAESTRO o "(no documentado)"), descripción, precondición
genérica, flujo, BRs, CNST. Path RST: `temp-backup/source-2026-04-28/
requisitos/casos_uso/<mod>/<archivo>.rst`.

### Módulo USR — 4 UCs

**UC_USR_01 — Crear Usuario** · legacy: (no documentado en inputs) · Actor:
AGR-006 agr_admin_usuarios · BReq: BRQ-USR-001 · Precondición: usuario admin
autenticado, segmento existente (PRE-01..N en RST §4.1) · Flujo: 5 pasos en
RST §5 (validar datos → generar username CNST-005 → crear cuenta estado
PENDIENTE_CONFIGURACION → notificar via InternalMessage CNST-001 → registrar
USER_CREATE en auditoría CNST-009) · CNST: CNST-001, CNST-005, CNST-009.

**UC_USR_02 — Consultar Usuarios** · legacy: (no documentado) · Actor:
AGR-006 · Precondición: sesión activa (RST §4.1) · Flujo: §5 (autenticar →
seleccionar filtros → ejecutar query → presentar tabla paginada → exportar
opcional) · CNST: CNST-009 (auditoría no aplica a lecturas).

**UC_USR_03 — Modificar Usuario** · legacy: (no documentado) · Actor: AGR-006
· Precondición: usuario destino existe, no eliminado · Flujo: §5 (seleccionar
usuario → editar campos editables — username NO modificable CNST-005 →
validar → confirmar → notificar cambios críticos InternalMessage CNST-001 →
registrar USER_UPDATE CNST-009) · CNST: 001, 005, 009.

**UC_USR_04 — Eliminar Usuario** · legacy: (no documentado) · Actor: AGR-006
· Precondición: usuario destino activo · Flujo: §5 (seleccionar → confirmar →
ejecutar baja LÓGICA CNST-005 — nunca física → registrar USER_DELETE CNST-009)
· CNST: 005, 009.

### Módulo ACC — 9 UCs

**UC_ACC_01 — Asignar Funciones** · legacy: UC-010 (PLAN_MAESTRO §3.1) ·
Actor: AGR-007 agr_admin_acceso · Flujo: §5 (seleccionar usuario → seleccionar
función RBAC Flat CNST-005 → validar SoD → asignar → registrar
FUNCTION_ASSIGN CNST-009) · CNST: 005, 009.

**UC_ACC_02 — Revocar Funciones** · legacy: (no documentado) · Actor: AGR-007
· Flujo: §5 (seleccionar → revocar → registrar FUNCTION_REVOKE CNST-009) ·
CNST: 005, 009.

**UC_ACC_03 — Consultar Permisos** · legacy: UC-011 (PLAN_MAESTRO §3.1) ·
Actor: AGR-007 · CNST: 005.

**UC_ACC_04 — Asignar Agrupador** · legacy: (no documentado) · Actor: AGR-007
· Agrupadores: AGR-001..AGR-010 (RST §10) · CNST: 005, 009.

**UC_ACC_05 — Gestionar SoD** · legacy: UC-043 (PLAN_MAESTRO §3.1, FND_03 L100)
· Actor: AGR-007 · Reglas SoD predefinidas (RST §10) · CNST: 005, 009.

**UC_ACC_06 — Gestionar Segmentos** · legacy: (no documentado) · Actor:
AGR-007 · CNST: 005, 009.

**UC_ACC_07 — Asignar Segmento** · legacy: (no documentado) · Actor: AGR-007
· Flujo: §5 (registra SEGMENT_ASSIGN CNST-009) · CNST: 005, 009.

**UC_ACC_08 — Permiso Temporal** · legacy: (no documentado) · Actor: AGR-007
· Restricción: máx 6 meses (CNST-005) · CNST: 005, 009.

**UC_ACC_09 — Auditar Cambios Acceso** · legacy: (no documentado) · Actor:
AGR-008 agr_auditor · Solo lectura (CNST-009 inmutable) · CNST: 009.

### Módulo RPT — 14 UCs

NOTA: el catálogo del prompt y los títulos RST divergen completamente para
RPT (excepto coincidencia parcial en exportaciones). Se reporta el contenido
RST canónico v4.0.0 bajo cada ID.

**UC_RPT_01** (RST: Ver Dashboard) · Actor: AGR-001 · BD Analytics
(CNST-003), filtrado por segmento (CNST-004) · CNST: 003, 004.

**UC_RPT_02** (RST: Ver Métricas Tiempo Real) · Actor: AGR-001 · CNST: 003,
004.

**UC_RPT_03** (RST: Ver Reportes Históricos) · Actor: AGR-002 agr_operador_
reportes · Rango máx 2 años (CNST-006) · CNST: 003, 004, 006.

**UC_RPT_04** (RST: Exportar CSV) · Actor: AGR-004 agr_exportador · Límite
100k registros (CNST-007), audit EXPORT_CSV (CNST-009) · CNST: 004, 007, 009.

**UC_RPT_05** (RST: Exportar Excel) · Actor: AGR-004 · EXPORT_EXCEL CNST-009
· CNST: 004, 007, 009.

**UC_RPT_06** (RST: Exportar PDF) · Actor: AGR-004 · EXPORT_PDF CNST-009 ·
CNST: 004, 007, 009.

**UC_RPT_07** (RST: Programar Reporte) · Actor: AGR-003 agr_supervisor ·
Notificación InternalMessage (CNST-001) · CNST: 001, 004, 009.

**UC_RPT_08** (RST: Ver Reportes Programados) · Actor: AGR-003 · CNST: 004.

**UC_RPT_09** (RST: Configurar Filtros) · Actor: AGR-003 · CNST: 004, 009.

**UC_RPT_10** (RST: Guardar Vista) · Actor: AGR-002 · CNST: 004.

**UC_RPT_11** (RST: Compartir Reporte) · Actor: AGR-003 · CNST: 001, 004,
009.

**UC_RPT_12** (RST: Ver Reporte Agentes) · Actor: AGR-003 · CNST: 003, 004.

**UC_RPT_13** (RST: Ver Reporte Colas) · Actor: AGR-003 · CNST: 003, 004.

**UC_RPT_14** (RST: Ver Reporte Campañas) · Actor: AGR-003 · CNST: 003, 004.

Legacy v2.0 mapping para RPT: (no documentado en inputs).

### Módulo ALR — 5 UCs

NOTA: títulos divergen entre catálogo y RST.

**UC_ALR_01** (RST: Configurar Umbrales) · Actor: AGR-005 agr_gestor_alertas
· Umbrales por segmento (CNST-004), audit THRESHOLD_CONFIG (CNST-009) · CNST:
004, 009.

**UC_ALR_02** (RST: Ver Alertas Activas) · Actor: AGR-001 · CNST: 001, 003,
004.

**UC_ALR_03** (RST: Reconocer Alerta) · Actor: AGR-003 agr_supervisor ·
ALERT_ACK CNST-009, notif InternalMessage CNST-001 · CNST: 001, 009.

**UC_ALR_04** (RST: Ver Historial Alertas) · Actor: AGR-003 · Máx 2 años
(CNST-006) · CNST: 003, 004, 006.

**UC_ALR_05** (RST: Gestionar Suscripciones) · Actor: AGR-005 · Notif
EXCLUSIVAMENTE InternalMessage CNST-001 · CNST: 001, 004, 009.

Legacy v2.0: (no documentado en inputs).

### Módulo PIP — 4 UCs

**UC_PIP_01** (RST: Supervisar ETL) · legacy: UC-050 (PLAN_MAESTRO §3.2,
FND_03 L277 actor TIEMPO) · Actor: AGR-009 agr_admin_pipeline · Solo lectura
BD IVR (CNST-003) · CNST: 003, 009.

**UC_PIP_02** (RST: Consultar Errores ETL) · legacy: (no documentado) ·
Actor: AGR-009 · CNST: 003, 009.

**UC_PIP_03** (RST: Consultar Disponibilidad) · legacy: (no documentado) ·
Actor: AGR-009 · CNST: 003.

**UC_PIP_04** (RST: Solicitar Reintento) · legacy: (no documentado) · Actor:
AGR-009 · RETRY_REQUEST CNST-009 · CNST: 003, 009.

### Módulo AUD — 4 UCs

NOTA: el catálogo asigna UC_AUD_02="Generar Reporte Compliance" pero el RST
ubica esa función en UC_AUD_04. UC_AUD_02 RST = "Buscar Auditoria"
(extensión de UC_AUD_01 con búsqueda avanzada). UC_AUD_04 RST = "Generar
Reporte Compliance" — el orden numérico difiere.

**UC_AUD_01** (RST: Consultar Auditoría) · legacy: (no documentado) · Actor:
AGR-006 agr_auditor (en RST AGR-006 es auditor, distinto del USR donde
AGR-006=admin_usuarios — diferencia de catálogo agrupadores) · Registros
inmutables (CNST-009), SoD (CNST-010) · CNST: 009, 010.

**UC_AUD_02** (RST: Buscar Auditoría) · catálogo dice "Generar Reporte
Compliance" pero contenido RST es búsqueda avanzada · Actor: AGR-006 · CNST:
009, 010. Discrepancia de mapping ID↔función entre catálogo y RST.

**UC_AUD_03** (RST: Exportar Auditoría) · Actor: AGR-006 · Límite 100k
(CNST-007) · CNST: 007, 009, 010.

**UC_AUD_04** (RST: Generar Reporte Compliance) · catálogo dice "Registrar
Evento" pero RST es generación de reporte de compliance con 7 secciones
(portada → resumen ejecutivo → estadísticas → gráficos tendencias → detalle
eventos → anomalías → conclusiones) · Actor: AGR-006 · CNST: 009, 010.

Discrepancia crítica AUD: el ID `UC_AUD_04 = Registrar Evento` del catálogo
del prompt no tiene archivo RST correspondiente; el sistema documentado en
RST cubre Registrar Evento implícitamente vía CNST-009 (auditoría inmutable
escrita por todos los UCs) sin UC dedicado.

## UCs sin contenido en inputs

Tras el cruce, **0 IDs del catálogo carecen de archivo RST**: los 40 archivos
existen. Sin embargo, los siguientes IDs presentan **contenido funcional
divergente** entre catálogo del prompt y RST canónico v4.0.0 — requieren
decisión del ejecutor sobre cuál es la fuente de verdad antes de poblar
`source/`:

- UC_RPT_01..UC_RPT_14 (14 UCs): títulos y semántica del catálogo
  (Reporte Trimestral, Problemas Menu, Transferencias, KPIs, Tendencias,
  Gráficos Hora/Día, Distribución Centro) **no aparecen** en RSTs (que
  documentan Dashboard, Métricas Tiempo Real, Reportes Históricos,
  Programación, etc.).
- UC_ALR_01, UC_ALR_03, UC_ALR_04, UC_ALR_05 (4 UCs): "Configurar Alerta /
  Pausar / Eliminar / Gestionar Destinatarios" del catálogo vs "Configurar
  Umbrales / Reconocer / Ver Historial / Gestionar Suscripciones" del RST.
- UC_AUD_02, UC_AUD_04 (2 UCs): semántica re-asignada (compliance ↔
  búsqueda; "Registrar Evento" sin RST dedicado).

Total: **20 UCs con contenido divergente**, 20 UCs alineados.

## Mapeo legacy v2.0 → v4.0.0 documentado

Solo cuatro pares confirmados en `PLAN_MAESTRO_Actualizacion_Referencias_v4_
0_0_SIN_EMOJIS.md`:

| v2.0 | v4.0.0 |
|------|--------|
| UC-010 | UC_ACC_01 |
| UC-011 | UC_ACC_03 |
| UC-043 | UC_ACC_05 |
| UC-050 | UC_PIP_01 |
| UC-001 / UC-002 / UC-003 | UC_AUTH_01 / UC_AUTH_02 / UC_AUTH_03 (fuera del catálogo de 40) |
| UC-006..UC-009 | UC_USR_XX (rango sin UC específico) |

El mapeo 1:1 exhaustivo legacy → v4.0.0 para los 40 UCs del catálogo **no
está documentado en los inputs analizados**.
