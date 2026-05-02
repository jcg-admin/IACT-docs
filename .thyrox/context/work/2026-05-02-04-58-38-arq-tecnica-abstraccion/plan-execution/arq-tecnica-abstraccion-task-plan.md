```yml
created_at: 2026-05-02 04:58:38
project: IACT-docs
work_package: 2026-05-02-04-58-38-arq-tecnica-abstraccion
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Borrador
```

# Task Plan — Abstracción source/arquitectura-tecnica

## Principio de abstracción

Reemplazar todo identificador de tecnología concreta por su equivalente
abstracto según el mapa en `wp-state.md`. El documento debe describir
QUÉ hace cada componente, no con QUÉ stack tecnológico específico.

**Patrón principal a reemplazar en todos los módulos:**
- Títulos de sección `X.Y Apps Django` → `X.Y Componentes de Aplicación`
- Referencias inline a frameworks/librerías → terminología abstracta

---

## Fase A — Módulos de aplicación (arq-mod-*.rst)

### T-001 — arq-mod-001-auth.rst (16 ocurrencias)
- [x] Sección "5.1 Apps Django" → "5.1 Componentes de Aplicación"
- [x] JWT (×9+3 adicionales encontrados en scan): según contexto →
  - "token de autenticación" (cuando describe el objeto)
  - "token de acceso" (cuando describe el flujo)
  - "token firmado" (cuando describe la seguridad)
- [x] "bcrypt (minimo 12 rounds)" → "algoritmo de hash de contraseña"
- [x] "HS256" → "algoritmo de firma simétrica"
- [x] "PostgreSQL, no Redis" → "base de datos relacional, no caché en memoria"
- [x] "DRF" → "framework de API REST"
- [x] "SimpleJWT. Blacklist de tokens" → "librería de tokens. Lista negra de tokens"
- [x] "React" (en diagrama) → "Interfaz"

### T-002 — arq-mod-002-user-identity.rst
- [x] Sección "5.1 Apps Django" → "5.1 Componentes de Aplicación"

### T-003 — arq-mod-003-rbac-core.rst (4 ocurrencias)
- [x] Sección "6.1 Apps Django" → "6.1 Componentes de Aplicación"
- [x] "CNST_002: Sesiones en PostgreSQL" → "CNST_002: Sesiones en base de datos relacional"
- [x] "Seguridad DRF Checklist: Implementa permisos DRF" → "Seguridad API REST: Implementa permisos de API"
- [x] "IsAuthenticated, roles via JWT claims" → "autenticación requerida, roles via claims del token"

### T-004 — arq-mod-004-etl-monitoring.rst (2 ocurrencias)
- [x] Sección "5.1 Apps Django" → "5.1 Componentes de Aplicación"
- [x] "(MySQL) | | (PostgreSQL)" → "(BD operativa) | | (BD analítica)"

### T-005 — arq-mod-005-vis-reports.rst
- [x] Sección "6.1 Apps Django" → "6.1 Componentes de Aplicación"

### T-006 — arq-mod-006-alerts.rst
- [x] Sección "7.1 Apps Django" → "7.1 Componentes de Aplicación"

### T-007 — arq-mod-007-audit.rst
- [x] Sección "7.1 Apps Django" → "7.1 Componentes de Aplicación"

### T-008 — arq-mod-008-sys-logs.rst
- [x] Sección "8.1 Apps Django" → "8.1 Componentes de Aplicación"

---

## Fase B — Archivos RBAC

### T-009 — rbac/modelo-rbac-iact.rst (4 ocurrencias)
- [x] Dos secciones "**Implementación Django:**" → "**Implementación backend:**"
- [x] No hay JWT u otras referencias adicionales en el archivo (verificado con grep)

### T-010 — rbac/raci-rbac-iact.rst
- [x] "backend (Django + SQL)" → "backend (framework web + base de datos)"

### T-011 — rbac/index.rst
- [x] "implementacion SQL/Django" → "implementacion en base de datos y backend"

---

## Fase C — Archivos de matriz y raíz

### T-012 — matriz-dependencias-uc-iact.rst (3 ocurrencias)
- [x] "middleware HTTP que extrae JWT del header" → "middleware HTTP que extrae el token de autenticación del header"
- [x] "guia de diseno tecnico (Django models / services / middleware)" → "guia de diseno tecnico (modelos / servicios / middleware)"
- [x] "ADRs de implementacion (Django apps, ...)" → "ADRs de implementacion (módulos de aplicación, ...)"

---

## Fase D — Verificación build

### T-013 — Build y validación
- [x] Ejecutar `sphinx-build -b html source build/html`
- [x] Verificar 0 warnings (no deben aumentar por los cambios de texto)
- [x] Verificar que las referencias RST (`:doc:`, `:ref:`) siguen resolviendo

### T-014 — Commit y push
- [x] Commit consolidado (fases A+B+C en un solo commit `aa1b4a4`)
- [x] Push a `feature/arquitectura-tecnica-content`

---

## Notas de ejecución

### Sobre JWT
JWT aparece 9 veces en arq-mod-001. No todas son iguales:
- Como objeto: "token JWT" → "token de autenticación"
- En código/función: `Generar_Token_JWT` → `Generar_Token_Autenticacion`
- En diagrama: `200 + JWT` → `200 + token`
- En configuración: `JWT firmado con HS256` → `token firmado con algoritmo simétrico`

### Sobre "Apps Django" (sección 5.1/6.1/7.1/8.1)
Este es el único patrón idéntico en los 8 módulos. Se puede aplicar
con sed de forma masiva al título y contenido.

### Sobre HS256
Técnicamente HS256 es un algoritmo estándar (HMAC-SHA256), no un
identificador de tecnología. Pero nombra un algoritmo específico
donde el documento debería solo decir "algoritmo de firma simétrica"
para no prescribir la implementación.
