```yml
created_at: 2026-05-04 21:30:00
project: THYROX
work_package: 2026-05-04-20-56-44-alias-catalog
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Análisis de Conflictos de Aliases

Aliases que no pueden estar en el diccionario global porque tienen semántica
distinta según el archivo fuente. Requieren corrección individual por archivo.

## Conflicto 1 — A01..A05 (AUTH vs AUD)

| Alias | En archivo(s) | Corrección |
|-------|--------------|------------|
| `A01` | mod-auth.rst | `INICIAR_SESION` |
| `A01` | mod-audit.rst | `VER_AUDITORIA` |
| `A02` | mod-auth.rst | `CERRAR_SESION` |
| `A02` | mod-audit.rst | `BUSCAR_AUDITORIA` |
| `A03` | mod-auth.rst | `RECUPERAR_CONTRASENA` |
| `A03` | mod-audit.rst | `EXPORTAR_AUDITORIA` |
| `A04` | mod-auth.rst | `CAMBIAR_CONTRASENA` |
| `A04` | mod-audit.rst | `REPORTE_COMPLIANCE` |
| `A05` | mod-auth.rst | `GESTIONAR_SESIONES` |

## Conflicto 2 — P01..P04 (PERM vs PIP)

| Alias | En archivo(s) | Corrección |
|-------|--------------|------------|
| `P01` | uc-perm-*.rst | `ASIGNAR_GRUPO` |
| `P01` | uc-pip-*.rst | `VER_ESTADO_ETL` |
| `P02` | uc-perm-*.rst | `REVOCAR_GRUPO` |
| `P02` | uc-pip-*.rst | `VER_ERRORES_ETL` |
| `P03` | uc-perm-*.rst | `CONCEDER_PERMISO_EXCEPCIONAL` |
| `P03` | uc-pip-*.rst | `VER_DISPONIBILIDAD_DATOS` |
| `P04` | uc-perm-*.rst | `REVOCAR_PERMISO_EXCEPCIONAL` |
| `P04` | uc-pip-*.rst | `REINTENTAR_ETL` |

## Conflicto 3 — U01..U14 (USR vs RPT)

| Alias | En archivo(s) | Corrección |
|-------|--------------|------------|
| `U01` | uc-usr-*.rst | `CREAR_USUARIO` |
| `U01` | uc-rpt-*.rst | `VER_DASHBOARD_IVR` |
| `U02` | uc-usr-*.rst | `CONSULTAR_USUARIOS` |
| `U02` | uc-rpt-*.rst | `VER_METRICAS_TIEMPO_REAL` |
| `U03` | uc-usr-*.rst | `MODIFICAR_USUARIO` |
| `U03` | uc-rpt-*.rst | `VER_REPORTES_HISTORICOS` |
| `U04` | uc-usr-*.rst | `ELIMINAR_USUARIO` |
| `U04` | uc-rpt-*.rst | `EXPORTAR_REPORTE` |

## Conflicto 4 — UC01..UC09 (multi-módulo)

Cada módulo reutiliza UC01..UC09 para sus propios UCs.
Requieren prefijo de módulo en la corrección:

| Alias en | Corrección sugerida |
|----------|-------------------|
| mod-access | `UC01` → `ASIGNAR_FUNCIONES_A_USUARIO` |
| mod-alerts | `UC01` → `CONFIGURAR_UMBRALES_ALERTAS` |
| mod-audit  | `UC01` → `VER_AUDITORIA` |
| etc. | Por archivo |

## Conflicto 5 — IVR (sistema vs BD)

| Contexto | Corrección |
|----------|------------|
| Diagrama de contexto (sistema externo) | `SISTEMA_IVR` |
| Diagrama deployment (base de datos) | `BD_IVR` |

## Conflicto 6 — AUDIT / AUD (servicio vs tabla)

| Contexto | Corrección |
|----------|------------|
| Diagrama de secuencia (servicio) | `SERVICIO_AUDITORIA` |
| Diagrama de deployment (artefacto) | `TABLA_AUDIT_LOG` |

## Conflicto 7 — PE (ETL vs Permisos)

| Contexto | Corrección |
|----------|------------|
| Módulos (Pipeline ETL) | `MODULO_ETL` |
| Servicios (Permissions Engine) | `MOTOR_PERMISOS` |
