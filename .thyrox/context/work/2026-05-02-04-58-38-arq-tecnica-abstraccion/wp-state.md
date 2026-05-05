```yml
project: IACT-docs
work_package: 2026-05-02-04-58-38-arq-tecnica-abstraccion
created_at: 2026-05-02 04:58:38
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: thyrox
methodology_step: thyrox:discover
predecessor_wp: 2026-05-02-02-34-35-plantuml-warnings-fix
branch: feature/arquitectura-tecnica-content
```

# WP — Abstracción de Identificadores de Tecnología en source/arquitectura-tecnica

## Motivo

Los archivos de `source/arquitectura-tecnica/` contienen identificadores
de tecnología concretos (Django, JWT, PostgreSQL, DRF, bcrypt, React,
MySQL, SimpleJWT, Redis). La arquitectura técnica del sistema debe
describirse en términos abstractos e independientes de implementación,
de acuerdo con el principio de las referencias metodológicas:

- `source/requisitos/_metodologia-aplicacion/` — vocabulario y estilo
- `source/base-cognitiva/_uml/` — principios de abstracción UML

## Alcance

12 archivos en `source/arquitectura-tecnica/` con ~35 ocurrencias
de identificadores tecnológicos concretos.

## Archivos afectados (por volumen)

| Archivo | Ocurrencias | Tecnologías |
|---------|-------------|-------------|
| modulos/arq-mod-001-auth.rst | 16 | JWT(×9), Django(×1), PostgreSQL, Redis, DRF, SimpleJWT, bcrypt, React |
| rbac/modelo-rbac-iact.rst | 4 | Django(×2), reactivate verb |
| modulos/arq-mod-003-rbac-core.rst | 4 | PostgreSQL, Django, DRF, JWT |
| matriz-dependencias-uc-iact.rst | 3 | JWT, Django(×2) |
| modulos/arq-mod-004-etl-monitoring.rst | 2 | Django, MySQL+PostgreSQL |
| modulos/arq-mod-002-user-identity.rst | 1 | Django |
| modulos/arq-mod-005-vis-reports.rst | 1 | Django |
| modulos/arq-mod-006-alerts.rst | 1 | Django |
| modulos/arq-mod-007-audit.rst | 1 | Django |
| modulos/arq-mod-008-sys-logs.rst | 1 | Django |
| rbac/raci-rbac-iact.rst | 1 | Django + SQL |
| rbac/index.rst | 1 | SQL/Django |

## Mapa de abstracción

| Tecnología concreta | Abstracción canónica |
|--------------------|----------------------|
| Django / "Apps Django" | framework web / módulos de aplicación |
| JWT | token de autenticación / token de acceso |
| bcrypt | algoritmo de hash de contraseña |
| PostgreSQL (sesiones) | base de datos relacional |
| PostgreSQL (ETL destino) | base de datos analítica |
| MySQL (ETL origen) | base de datos operativa |
| Redis | almacén en memoria / caché |
| DRF | framework de API REST |
| SimpleJWT | librería de gestión de tokens |
| React | interfaz de usuario / cliente web |
| HS256 | algoritmo de firma de token |

## Referencias metodológicas

- `source/requisitos/_metodologia-aplicacion/` — estilo de descripción
  de comportamiento sin nombrar tecnologías de implementación
- `source/base-cognitiva/_uml/` — principios de abstracción en modelos UML

## Tareas

Ver `plan-execution/arq-tecnica-abstraccion-task-plan.md`
