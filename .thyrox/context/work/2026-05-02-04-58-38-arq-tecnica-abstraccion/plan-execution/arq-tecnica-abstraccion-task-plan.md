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
- [ ] Sección "5.1 Apps Django" → "5.1 Componentes de Aplicación"
- [ ] JWT (×9): según contexto →
  - "token de autenticación" (cuando describe el objeto)
  - "token de acceso" (cuando describe el flujo)
  - "token firmado" (cuando describe la seguridad)
- [ ] "bcrypt (minimo 12 rounds)" → "algoritmo de hash de contraseña"
- [ ] "HS256" → "algoritmo de firma simétrica"
- [ ] "PostgreSQL, no Redis" → "base de datos relacional, no caché en memoria"
- [ ] "DRF" → "framework de API REST"
- [ ] "SimpleJWT. Blacklist de tokens" → "librería de tokens. Lista negra de tokens"
- [ ] "React" (en diagrama) → "Interfaz de Usuario"

### T-002 — arq-mod-002-user-identity.rst
- [ ] Sección "5.1 Apps Django" → "5.1 Componentes de Aplicación"

### T-003 — arq-mod-003-rbac-core.rst (4 ocurrencias)
- [ ] Sección "6.1 Apps Django" → "6.1 Componentes de Aplicación"
- [ ] "CNST_002: Sesiones en PostgreSQL" → "CNST_002: Sesiones en base de datos relacional"
- [ ] "Seguridad DRF Checklist: Implementa permisos DRF" → "Seguridad API REST: Implementa permisos de API"
- [ ] "IsAuthenticated, roles via JWT claims" → "autenticación requerida, roles via claims del token"

### T-004 — arq-mod-004-etl-monitoring.rst (2 ocurrencias)
- [ ] Sección "5.1 Apps Django" → "5.1 Componentes de Aplicación"
- [ ] "(MySQL) | | (PostgreSQL)" → "(base de datos operativa) | | (base de datos analítica)"

### T-005 — arq-mod-005-vis-reports.rst
- [ ] Sección "6.1 Apps Django" → "6.1 Componentes de Aplicación"

### T-006 — arq-mod-006-alerts.rst
- [ ] Sección "7.1 Apps Django" → "7.1 Componentes de Aplicación"

### T-007 — arq-mod-007-audit.rst
- [ ] Sección "7.1 Apps Django" → "7.1 Componentes de Aplicación"

### T-008 — arq-mod-008-sys-logs.rst
- [ ] Sección "8.1 Apps Django" → "8.1 Componentes de Aplicación"

---

## Fase B — Archivos RBAC

### T-009 — rbac/modelo-rbac-iact.rst (4 ocurrencias)
- [ ] Dos secciones "**Implementación Django:**" → "**Implementación backend:**"
- [ ] Verificar si hay JWT u otras referencias adicionales en el archivo

### T-010 — rbac/raci-rbac-iact.rst
- [ ] "backend (Django + SQL)" → "backend (framework web + base de datos)"

### T-011 — rbac/index.rst
- [ ] "implementacion SQL/Django" → "implementacion en base de datos y backend"

---

## Fase C — Archivos de matriz y raíz

### T-012 — matriz-dependencias-uc-iact.rst (3 ocurrencias)
- [ ] "middleware HTTP que extrae JWT del header" → "middleware HTTP que extrae el token de autenticación del header"
- [ ] "guia de diseno tecnico (Django models / services / middleware)" → "guia de diseno tecnico (modelos / servicios / middleware)"
- [ ] "ADRs de implementacion (Django apps, ...)" → "ADRs de implementacion (módulos de aplicación, ...)"

---

## Fase D — Verificación build

### T-013 — Build y validación
- [ ] Ejecutar `sphinx-build -b html source build/html`
- [ ] Verificar 0 warnings (no deben aumentar por los cambios de texto)
- [ ] Verificar que las referencias RST (`:doc:`, `:ref:`) siguen resolviendo

### T-014 — Commit y push
- [ ] Commit por fase (A, B, C) o único consolidado
- [ ] Push a `feature/arquitectura-tecnica-content`

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
