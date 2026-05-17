```yml
created_at: 2026-05-04 04:51:35
project: IACT-docs
work_package: 2026-05-04-04-51-35-std010-deployview-fix
phase: Phase 11 — TRACK
author: NestorMonroy
```

# Changelog — STD_010 DeployView Fix

## Added

## Changed

- `source/index.rst`: abstraido stack técnico (`Django REST Framework` →
  `Framework de API REST`, `Apache + mod_wsgi` → `Servidor Web`)
  (T-001, STD_010)
- `source/arquitectura-tecnica/DeployView/*.rst` (80 archivos): reemplazado
  `node "Apache + mod_wsgi"` → `node "Servidor Web"` y
  `artifact "Django App"` → `artifact "Aplicacion Backend"` (T-002, STD_010)
- `source/arquitectura-tecnica/modulos/**` (9 archivos): abstraidos
  `Django`, `Django ORM`, `DRF views`, `DRF`, `ETLScheduler (Django background task)`,
  `Apps Django` → vocabulario neutro (T-003, STD_010)
- `source/arquitectura-tecnica/UMLSystemView/componentes.rst`: abstraido
  `Backend IACT (Django)` → `Backend IACT` (T-003, STD_010)
- `source/arquitectura-tecnica/UMLSystemView/despliegue.rst`: abstraido
  `datos operacionales Django` → `datos operacionales del sistema`,
  referencias a `Django settings` → `configuracion de bases de datos` (T-003, STD_010)
- `source/requisitos/business-requirements/breq-004-cumplimiento-seguridad-auditoria.rst`:
  `Autenticación DRF` → `Autenticación de API`, `excepciones DRF` → `excepciones de API`
  (T-004, STD_010)
- `source/requisitos/casos-uso/auth/uc-auth-02/patrones-diseno.rst`:
  `RedisBlacklistStrategy` → `CacheBlacklistStrategy` (T-004, STD_010)

## Status de promoción a CHANGELOG.md raíz

WP completado — pendiente merge a main para promover al CHANGELOG raíz.
