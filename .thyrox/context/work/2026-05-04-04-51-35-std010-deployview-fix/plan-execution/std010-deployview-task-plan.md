```yml
created_at: 2026-05-04 04:51:35
project: IACT-docs
work_package: 2026-05-04-04-51-35-std010-deployview-fix
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En progreso
```

# Task Plan — STD_010 Violaciones Restantes (DeployView + otros)

Eliminar todas las menciones de tecnologías concretas fuera de los archivos
permitidos (implementacion-tecnica, testing, devops ADRs, backend ADRs).

---

## Bloque A — index.rst (landing page)

- [x] **T-001** Abstraer stack en `source/index.rst`
  - `Django REST Framework` → `Framework de API REST`
  - `Apache + mod_wsgi` → `Servidor Web`
  - Commit: "Abstract tech stack in index.rst (STD_010)"

---

## Bloque B — DeployView (80 archivos)

- [x] **T-002** Reemplazar en todos los `DeployView/*.rst`:
  - `node "Apache + mod_wsgi" as WebServer {` → `node "Servidor Web" as WebServer {`
  - `node "Apache + mod_wsgi" {` → `node "Servidor Web" {`
  - `artifact "Django App" as App` → `artifact "Aplicacion Backend" as App`
  - `iact.wsgi\n[Django + mod_wsgi]` → `iact.wsgi\n[Aplicacion Backend]`
  - `iact.wsgi\n[Django + mod_wsgi sobre Apache]` → `iact.wsgi\n[Aplicacion Backend sobre Servidor Web]`
  - Script Python bulk replace
  - Commit: "Abstract deployment tech names in DeployView (STD_010)"

---

## Bloque C — Arch files con Redis + DRF

- [x] **T-003** Reemplazar en modulos diagramas:
  - `database "Redis"` → `database "Cache"`
  - `database "Redis\n[...]"` → `database "Cache\n[...]"`
  - `-> Redis :` → `-> Cache :`
  - `activate CacheRedis` / `deactivate CacheRedis` → `CacheServicio`
  - `- Seguridad DRF` → `- Seguridad de API REST`
  - `- Todos los modulos DRF` → `- Todos los modulos de API`
  - `- Django REST Framework` → `- Framework de API REST`
  - `- Apps Django` → `- Modulos de la aplicacion`
  - `- ADR_DEVOPS_001 (Vagrant + Apache + mod_wsgi + Django + MySQL + Redis)` → abstract
  - Commit: "Abstract Redis and DRF references in arch diagrams (STD_010)"

---

## Bloque D — breq-004 y uc-auth-02/patrones-diseno

- [x] **T-004** Revisar y corregir:
  - `requisitos/business-requirements/breq-004-cumplimiento-seguridad-auditoria.rst`
  - `requisitos/casos-uso/auth/uc-auth-02/patrones-diseno.rst`
  - Commit: "Abstract tech names in breq-004 and patrones-diseno (STD_010)"

---

## Bloque E — Validación final

- [x] **T-005** Verificar 0 violaciones restantes:
  ```bash
  grep -rn "Django\|MariaDB\|Redis\|Celery\|bcrypt\|mod_wsgi\|DRF" source/ \
    | grep -v "implementacion-tecnica|testing|devops|backend/|normativa|adr-|databases|gestion|_metodologia|base-cognitiva|std-010"
  ```
  Resultado esperado: 0 líneas
  - Commit changelog

---

## Orden de ejecución

```
A (T-001) → B (T-002) → C (T-003) → D (T-004) → E (T-005)
```

Cada bloque = 1 commit. Push después de cada bloque.
