```yml
created_at: 2026-04-28 09:00:00
project: IACT-docs
work_package: 2026-04-28-05-28-43-source-rebuild-normativa-restricciones
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Mapeo Viejo → Nuevo (CNST)

> Tabla canónica para que WP #6 requisitos migre referencias desde el
> set anterior al set rebuild. Cubre los tres "viejos": backup canónico,
> temp-holding, y la nomenclatura corta `CNST-XXX`.

## Tabla de mapeo

| Viejo (backup) | Viejo (temp-holding) | Nuevo (rebuild) | Nota |
|----------------|----------------------|-----------------|------|
| CNST_001 Comunicaciones_Prohibidas | CNST_001 No_Email_Sistema | **CNST_001 Comunicaciones_Prohibidas** | Sin cambio |
| CNST_002 Gestion_Sesiones_BD | CNST_002 Sesiones_BD_Timeout | **CNST_002 Gestion_Sesiones_BD** | Sin cambio |
| CNST_003 Base_Datos_Dual_Inmutable | CNST_003 BD_IVR_Readonly_ETL (1ª mitad) | **CNST_003 Base_Datos_Dual_Inmutable** | Sin cambio |
| CNST_004 Actualizacion_Datos_ETL | CNST_003 BD_IVR_Readonly_ETL (2ª mitad) | **CNST_004 Actualizacion_Datos_ETL** | Sin cambio |
| CNST_005 Seguridad_DRF_Checklist | (no presente) | **CNST_005 Seguridad_DRF_Checklist** | Sin cambio |
| CNST_006 Antipatrones_Arquitectura | (no presente) | **CNST_006 Antipatrones_Arquitectura** | Sin cambio |
| CNST_007 Limites_Performance_SLA | CNST_006 Reportes + CNST_007 Throttling | **CNST_007 Limites_Performance_SLA** | Sin cambio |
| CNST_008 Infraestructura_Deployment | (no presente) | **CNST_008 Infraestructura_Deployment** | Sin cambio |
| CNST_009 Logging_Auditoria_Inmutable | CNST_008 Audit_Inmutable_Logs_PII | **CNST_009 Logging_Auditoria_Inmutable** | Sin cambio |
| CNST_010 Clasificacion_Proteccion_Datos | (no presente) | **CNST_010 Clasificacion_Proteccion_Datos** | Sin cambio |
| **CNST_012 RBAC_Flat_SoD_Permisos** | CNST_005 RBAC_Flat_SoD_Permisos | **CNST_011 RBAC_Flat_SoD_Permisos** | **Renumerado 012→011 (cierra gap)** |
| (no presente — temp-holding CNST_004) | CNST_004 Alertas_Buzon_Interno | (subsumido en CNST_001) | No incorporado (D-CNST-2) |

## Cambios de referencia obligatorios para WP #6

| Referencia anterior | Referencia nueva |
|---------------------|------------------|
| `CNST-012`, `CNST_012`, `:ref:\`cnst-012\`` | `CNST-011`, `CNST_011`, `:ref:\`cnst-011\`` |

Para cualquier otra CNST, la referencia permanece estable (001–010).

## CNSTs no incorporadas (decisión D-CNST-3)

- `CNST_05_Restriccion_Creacion_Iterativa_2_0_0.rst` — descartado del cajón
  de restricciones. Cabe en procedimientos / lineamientos metodológicos.
  Diferido a iteración futura.

## Versión y estado del set canónico

- Set: 11 CNST (001–011), gap eliminado.
- Versión metadata: 1.1.0 (consolida la propuesta de descongelamiento de
  ACTUALIZACION_DEL_ARBOL_SECCION_RESTRICCIONES.md).
- Estado: Vigente.
- Build: 0 warnings, 0 errors al cierre del WP.
