```yml
type: Architectural Decision Record
category: Política de Seguridad / Gobernanza
version: 1.0.0
purpose: Política de información sensible en repositorio
goal: Definir qué es sensible, dónde almacenarlo, cómo prevenir leaks
updated_at: 2026-05-06 20:30:00
```

# ADR: Política de Información Sensible en Repositorio

**Status:** Aprobado | **Fecha:** 2026-05-06 | **Owner:** NestorMonroy

**Origen:** TD-002 (`.thyrox/context/technical-debt.md`) — derivado del incidente TD-001 (2026-04-23: `PROJECT_CONFIGURATION_REVIEW.md` expuso info de configuración del sistema en git history).

---

## Contexto

El proyecto IACT-docs es **documentación pública del sistema** (RBAC v5.6.0, restricciones CNST, modelos de dominio, BReqs/BRs/UCs). Todo el contenido publicado en `source/` es intencionalmente compartible.

Sin embargo, hay categorías de información que **NO** deben entrar al repositorio:

1. Credenciales activas (API keys, passwords, tokens, secrets).
2. Detalles de infraestructura interna (IPs privadas, hostnames internos, paths de servidores).
3. Datos personales de usuarios reales (PII).
4. Configuración de instancias específicas (URLs de staging/prod con tokens en query).
5. Llaves criptográficas privadas.

El objetivo de este ADR es separar claramente lo **publicable** (corpus IACT-docs) de lo **sensible** (no commitear).

---

## Decisión

### 1. Qué es información sensible (no commitear)

| Categoría | Ejemplos | Almacenar en |
|---|---|---|
| Credenciales activas | API keys, passwords, tokens, JWT secrets | Variables de entorno, vault, `.env` (gitignored) |
| Infraestructura interna | IPs privadas, hostnames `*.internal`, paths absolutos de servidores prod | Wiki privada, runbooks no versionados |
| PII real | Nombres, emails, teléfonos de usuarios reales | Tests con fixtures sintéticas; nunca real |
| Config por instancia | URLs prod/staging con auth, connection strings | env vars + secret manager |
| Llaves criptográficas privadas | RSA, EC, SSH keys | Vault, no git |

### 2. Qué NO es información sensible (sí publicar)

- Modelo RBAC conceptual (roles, AGRs, funciones por nombre).
- Restricciones del sistema (CNST-001..033 con su descripción).
- Decisiones arquitectónicas (ADRs).
- Casos de uso, requisitos, reglas de negocio.
- Convenciones de naming, codenames de permisos.
- Estándares (STD-001..014).

Este es el contenido legítimo del corpus IACT-docs. El TD-001 original lo clasificó como "sensible" pero la decisión del proyecto es **publicarlo intencionalmente** como documentación; lo que sería verdaderamente sensible son las credenciales y la infraestructura **que ejecuta** este RBAC, no su definición conceptual.

### 3. Mecanismos de prevención

| Mecanismo | Implementación |
|---|---|
| `.gitignore` | Patrones para archivos de config local (`.env`, `*.pem`, `*credentials*`, `*secrets*`) |
| Pre-commit hook | `.githooks/pre-commit` detecta credentials markers en staged content (TD-003) |
| Code review | Checklist en PR template: "¿contiene info sensible?" |
| CI/CD | Job opcional con `gitleaks` o `detect-secrets` (futuro) |

### 4. Recuperación si ocurre un leak

1. **Identificar el alcance**: qué commits/archivos, si fue pusheado.
2. **Si es local-only**: `git reset --hard` al commit previo.
3. **Si fue pusheado**: discutir con stakeholders antes de history rewrite (`git filter-branch` / `bfg-repo-cleaner` + force-push). El force-push tiene impacto en clones existentes.
4. **Rotar credenciales** afectadas inmediatamente (precaución default si hubo cualquier exposición).
5. **Documentar** el incidente en `.thyrox/context/errors/` para aprender.

---

## Consecuencias

### Positivas

- Política clara sobre qué publicar.
- Pre-commit hook reduce probabilidad de leaks accidentales.
- TD-001 reclasificado como obsoleto: el contenido en cuestión es hoy parte legítima del corpus público.

### Negativas (aceptadas)

- Pre-commit hook puede generar falsos positivos en código que tiene patrones tipo `API_KEY=...` como ejemplos pedagógicos. Mitigación: keywords de exclusión (`example`, `placeholder`, `<your`, `TODO`) + bypass `--no-verify` documentado.

---

## Alternativas Consideradas

### Alternativa A — `git-crypt` para encriptar archivos sensibles

Encriptar selectivamente archivos en git via `git-crypt` con clave compartida via vault.

**Descartada:** complejidad de gestión de claves; los archivos verdaderamente sensibles deben estar fuera de git, no encriptados dentro.

### Alternativa B — Repositorio separado para info sensible

Tener `iact-secrets` repo privado para todo lo no-publicable.

**Aplicable parcialmente:** runbooks operativos sí pueden vivir en repo privado. Pero credenciales activas siguen en vault, no en otro git.

---

## Implementación

| Item | Status | Ubicación |
|---|---|---|
| `.gitignore` con patrones de archivos sensibles | ✅ Existente | `/.gitignore` |
| Pre-commit hook detección credentials | ✅ Implementado (TD-003) | `.githooks/pre-commit` |
| Política documentada | ✅ Este ADR | `.thyrox/context/decisions/adr-sensitive-info-policy.md` |
| `gitleaks` en CI | ⏳ Futuro (no urgente) | `.github/workflows/` |

---

## Trazabilidad

- **TDs cerradas por este ADR:** TD-001 (reclasificado obsoleto), TD-002 (este ADR), TD-003 (pre-commit hook).
- **Origen:** WP `2026-05-06-20-26-07-close-all-technical-debt`.
- **Refs:** `.thyrox/context/technical-debt.md` v1.0.0 (2026-04-23).
