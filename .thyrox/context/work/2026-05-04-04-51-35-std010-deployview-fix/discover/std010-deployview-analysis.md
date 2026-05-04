```yml
created_at: 2026-05-04 04:51:35
project: IACT-docs
work_package: 2026-05-04-04-51-35-std010-deployview-fix
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# DISCOVER — STD_010 Violaciones Restantes (DeployView + otros)

## Problema

Después de limpiar MariaDB, Redis, Celery, Django/DRF en UC narrativa y FRs,
quedan 90 archivos con violaciones STD_010. El grueso está en DeployView.

## Hallazgos (PROVEN)

### Grupo 1 — DeployView (80 archivos)

Patrón uniforme en todos los diagramas de despliegue:

```
node "Apache + mod_wsgi" as WebServer {
  artifact "Django App" as App
```

Fuente verificada:
```
grep -rh "Django\|mod_wsgi" source/arquitectura-tecnica/DeployView/ | sort -u
→ 2 patrones: "Apache + mod_wsgi" (WebServer) y "Django App" (artifact)
→ Afecta los 80 archivos .rst del DeployView
```

**Reemplazo correcto:**
- `node "Apache + mod_wsgi"` → `node "Servidor Web"` (o mantener Apache si es en deploy diagram)
- `artifact "Django App"` → `artifact "Aplicacion Backend"`

> Nota: En diagramas de despliegue (DeployView) los nombres de tecnología
> concretos son más aceptables que en spec narrativa — pero STD_010 aplica
> universalmente. Reemplazar con nombres abstractos consistentes.

### Grupo 2 — Arch files restantes (7 archivos)

- `database "Redis"` en PlantUML → `database "Cache"` o `database "Almacen de Sesiones"`
- `database "Redis\n[Sesiones + throttling]"` → `database "Cache\n[Sesiones + throttling]"`
- `Auth -> Redis : crear sesion` → `Auth -> Cache : crear sesion`
- `- Seguridad DRF` / `- Todos los modulos DRF` / `- Django REST Framework` en narrativa
- `DjangoModelFactory` en testing (excluir — testing.rst permitido)

Archivos afectados:
- `arquitectura-tecnica/modulos/sys-logs/diagramas/componentes-mod-logs.rst`
- `arquitectura-tecnica/modulos/operator/diagramas/componentes-mod-operator.rst`
- `arquitectura-tecnica/modulos/etl-monitoring/diagramas/componentes-mod-pipeline.rst`
- `arquitectura-tecnica/modulos/vis-reports/diagramas/componentes-mod-reports.rst`
- `arquitectura-tecnica/modulos/etl-monitoring/componentes.rst`
- `arquitectura-tecnica/modulos/vis-reports/componentes.rst`
- `requisitos/casos-uso/auth/uc-auth-02/patrones-diseno.rst`

### Grupo 3 — index.rst (página de inicio)

```
21: backend (Django REST Framework) servido por Apache + mod_wsgi sobre
36:     - Django REST Framework (Python 3.11+)
38:     - Ubuntu + Apache (mod_wsgi)
```

Reemplazo: → `Framework de API REST`, `Servidor de Aplicaciones`, `Ubuntu + Servidor Web`

### Grupo 4 — breq-004 y otros

- `requisitos/business-requirements/breq-004-cumplimiento-seguridad-auditoria.rst`

## Scope excluido

- `implementacion-tecnica/*.rst` — permitido (notas de implementación)
- `testing.rst` — permitido (código de test)
- `devops/adr-devops-001*` — ADR de infraestructura, menciona tecnologías explícitamente
- `base-cognitiva/` — base cognitiva/educativa
- `normativa/` — documentos normativos
- `databases/` — modelo de datos (ya tratado)
- `backend/` — ADRs backend (permitido mencionar stack)
