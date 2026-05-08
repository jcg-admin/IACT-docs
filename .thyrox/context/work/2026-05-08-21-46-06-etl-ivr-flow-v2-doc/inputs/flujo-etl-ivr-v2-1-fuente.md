# Flujo ETL IVR — Version 2.1 (documento completo)

**Fuente:** input del ejecutor el 2026-05-08 durante WP
`2026-05-08-21-46-06-etl-ivr-flow-v2-doc`.

**Proposito:** preservar el documento original tal cual lo
proveyo el ejecutor antes de adaptarlo al corpus IACT-docs
(formato RST, vocabulario STD-010, ubicacion en
arquitectura-tecnica/).

---

> **Fecha:** 2026-05-07
> **Version:** 2.1
> **Reemplaza:** `FLUJO-ETL-V2.md` (arquitectura) +
> `FLUJO-ETL-COMPLETO.md` (implementacion)
> **Por que:** V2.md tenia la arquitectura actualizada pero
> sin codigo real. COMPLETO.md tenia el codigo pero era v1
> con nombres obsoletos y sin checkpoints. Este documento
> fusiona ambos con la implementacion actual.

## Que cambio de v1 a v2

| Area | v1 | v2 | Por que |
|---|---|---|---|
| G-29 | CASE inline en cada SP | `fn_duracion_seg()` | Una sola version correcta para 38.8% de registros |
| NK90 / segmento / VACIO | CASE inline duplicado | `fn_normalizar_centro()`, `fn_did_segmento()`, `fn_normalizar_menu()` | Cambio en un lugar afecta a todos |
| Dias de semana | Pendiente del cliente | `ivr_es_dia_semana()` propias | Independencia del cliente — IVR opera 7 dias, criterio es lun-vie |
| Procesamiento | DELETE+INSERT de todo el quarter | Por mes (chunks ~4M filas) | Undo log manejable en MariaDB 10.1 |
| Orquestacion | Un SP sin checkpoints | Pipeline con checkpoint por paso en `job_execution_log` | Diagnostico preciso de fallos — saber exactamente que paso y que error |
| Crash MariaDB | `etl_runs` queda en `en_ejecucion` sin fin | Heartbeat Django + campo `timeout_at` | Deteccion automatica de timeout en 30 minutos |
| Dias de semana en reportes | Segundo scan a la fuente | Pre-computados en ETL (`llamadas_entre_semana`) | `sp_rpt_centros_xsegmento` sin scan adicional |

## Vision general (texto en bloque ASCII)

```
CLIENTE (solo lectura)          IACT — MariaDB mismo servidor
──────────────────────          ──────────────────────────────────────────────

tbl_historico_t1_2025           DISPARO
tbl_historico_t2_2025           evt_etl_diario (02:00 AM MySQL Event)
tbl_historico_t3_2025           manage.py run_etl (APScheduler Django)
tbl_historico_t4_2025               │
tbl_historico_t1_2026               ▼
tbl_historico_t2_2026           sp_etl_maestro()
         │                          │ checkpoint 'etl_base_detalle'
         └── scan mes a mes ──▶     ├── sp_etl_base_detalle() ──▶ base_ivr_detalle
         └── scan full quarter ──▶  ├── sp_etl_base_clientes() ──▶ base_ivr_clientes
                                    └── sp_etl_validar()
                                         │
                                    job_execution_log / etl_runs
                                         │
                                         ▼
                                  sp_rpt_centros_transferencia()
                                  sp_rpt_centros_xsegmento()
                                  sp_rpt_llamadas_abandonadas()   ◀── Django
                                  sp_rpt_menu_redirigidos()           cursor.callproc()
                                  sp_rpt_menu_centro()
                                  sp_rpt_cMENU_ERROR()
                                  sp_rpt_clientes()
```

## Niveles 0..5

(Resto del contenido truncado en este snapshot — ver
`wp-state.md` para extraccion estructurada por nivel y
ubicacion final en el corpus.)

## Restricciones que condicionan el diseno

CNST-ETL-001..008 + CNST-003 + ADR-BACK-012 + IVR-7-dias.

## Estado de componentes

Tabla con 17 componentes y su estado (Desplegado / Pendiente /
Creado).
