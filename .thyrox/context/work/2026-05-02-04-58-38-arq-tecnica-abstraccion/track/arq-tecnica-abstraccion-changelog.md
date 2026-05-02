```yml
created_at: 2026-05-02 05:00:00
project: IACT-docs
work_package: 2026-05-02-04-58-38-arq-tecnica-abstraccion
phase: Phase 11 — TRACK
author: NestorMonroy
status: Cerrado
```

# Changelog — arq-tecnica-abstraccion

## Changed

- `source/arquitectura-tecnica/modulos/arq-mod-001-auth.rst`:
  12 referencias de tecnología concreta abstractas:
  - JWT (×12 ocurrencias incluyendo diagrama ASCII) → token de autenticación /
    token / claims del token según contexto
  - "5.1 Apps Django" → "5.1 Componentes de Aplicación"
  - "bcrypt (minimo 12 rounds)" → "algoritmo de hash de contraseña"
  - "HS256" → "algoritmo de firma simétrica"
  - "Sesiones en PostgreSQL, no Redis" → "base de datos relacional, no caché en memoria"
  - "Seguridad DRF" → "Seguridad API REST"
  - "SimpleJWT. Blacklist de tokens" → "librería de tokens. Lista negra de tokens"
  - "(React)" en diagrama ASCII → "(Interfaz)"
  - "Generar_Token_JWT" (FR_002 nombre) → "Generar_Token_Autenticacion"

- `source/arquitectura-tecnica/modulos/arq-mod-003-rbac-core.rst`:
  4 referencias abstractas:
  - "6.1 Apps Django" → "6.1 Componentes de Aplicación"
  - "CNST_002: Sesiones en PostgreSQL" → "base de datos relacional"
  - "Seguridad DRF Checklist: Implementa permisos DRF" → "Seguridad API REST: Implementa permisos de API"
  - "IsAuthenticated, roles via JWT claims" → "autenticación requerida, roles via claims del token"

- `source/arquitectura-tecnica/modulos/arq-mod-004-etl-monitoring.rst`:
  2 referencias abstractas:
  - "5.1 Apps Django" → "5.1 Componentes de Aplicación"
  - Diagrama ASCII: "(MySQL) | | (PostgreSQL)" → "(BD operativa) | | (BD analítica)"

- `source/arquitectura-tecnica/modulos/arq-mod-002-user-identity.rst`:
  - "5.1 Apps Django" → "5.1 Componentes de Aplicación"

- `source/arquitectura-tecnica/modulos/arq-mod-005-vis-reports.rst`:
  - "6.1 Apps Django" → "6.1 Componentes de Aplicación"

- `source/arquitectura-tecnica/modulos/arq-mod-006-alerts.rst`:
  - "7.1 Apps Django" → "7.1 Componentes de Aplicación"

- `source/arquitectura-tecnica/modulos/arq-mod-007-audit.rst`:
  - "7.1 Apps Django" → "7.1 Componentes de Aplicación"

- `source/arquitectura-tecnica/modulos/arq-mod-008-sys-logs.rst`:
  - "8.1 Apps Django" → "8.1 Componentes de Aplicación"

- `source/arquitectura-tecnica/rbac/modelo-rbac-iact.rst`:
  - "**Implementación Django:**" (×2) → "**Implementación backend:**"

- `source/arquitectura-tecnica/rbac/raci-rbac-iact.rst`:
  - "backend (Django + SQL)" → "backend (framework web + base de datos)"

- `source/arquitectura-tecnica/rbac/index.rst`:
  - "implementacion SQL/Django" → "implementacion en base de datos y backend"

- `source/arquitectura-tecnica/matriz-dependencias-uc-iact.rst`:
  - "middleware HTTP que extrae JWT del header" → "el token de autenticación del header"
  - "Django models / services / middleware" → "modelos / servicios / middleware"
  - "ADRs de implementacion (Django apps, ...)" → "(módulos de aplicación, ...)"

## Decisiones auto-tomadas

### D-01: Escaneo de diagramas PlantUML previo a edición

**Trigger:** La corrección del usuario señaló que los diagramas violan el
principio de la máquina de gaseosa — tecnología visible en diagramas.

**Investigación:** Script Python de escaneo de bloques `@startuml..@enduml`
en `source/arquitectura-tecnica/` devolvió **sin resultados**: los diagramas
PlantUML del módulo arquitectónico no contienen identificadores de tecnología
en el código PlantUML en sí. Los identificadores tecnológicos están solo en
las secciones de prosa (texto plano y diagramas ASCII).

**Decisión:** Procedeer con edición de prosa + diagramas ASCII (code-block::text).
Los bloques PlantUML no requieren cambios.

### D-02: "Apps Django" en tabla → columna "App" → "Componente"

**Trigger:** El título de sección cambia de "Apps Django" a "Componentes de
Aplicación". La columna de la tabla que sigue decía "App" — coherente con la
terminología anterior.

**Decisión:** Cambiar también la cabecera de columna de "App" a "Componente"
para que sea coherente con el nuevo título de sección.

### D-03: JWT scan encontró 12 ocurrencias en arq-mod-001, no 9

**Trigger:** El task plan estimaba ×9 para JWT en arq-mod-001. El grep real
encontró 12 (incluyendo diagrama de contexto "claims JWT", tabla de ataques
"Tokens JWT", y el diagrama de flujo "Generar JWT").

**Decisión:** Aplicar abstracción a todas las 12 ocurrencias. El task plan
era estimación inicial; el scan definitivo es el grep ejecutado antes de editar.

### D-04: DRF en normativa (CNST-009) — no abstractizar

**Trigger:** CNST-009 menciona Django REST Framework como tecnología mandatoria.
¿Debería la normativa también abstractizarse?

**Decisión:** NO — la normativa en `source/normativa/` PRESCRIBE tecnologías
concretas como restricciones del sistema. CNST-009 es un constraint que dice
"debes usar DRF". Cambiar eso sería cambiar la restricción misma, no descripción.
Solo los archivos en `source/arquitectura-tecnica/` son el alcance del WP.

### D-05: Underlines RST ajustados al nuevo largo de título

**Trigger:** RST requiere que la línea de subrayado tenga al menos el mismo
largo que el título. "5.1 Componentes de Aplicación" = 29 chars > "5.1 Apps Django" = 15 chars.

**Decisión:** Cambiar `---------------` (15 dashes) por `------------------------------`
(30 dashes) en cada sección afectada.

## Status de promoción a CHANGELOG.md raíz

No aplica bump de versión en esta iteración — cambios son abstractización
de vocabulario sin cambios de funcionalidad pública.
Promover en el próximo release que incluya contenido nuevo.
