```yml
project: IACT-docs
work_package: 2026-05-08-03-56-35-tdd6-std010-scope-extension
created_at: 2026-05-08 03:56:35
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeño (4 exenciones normativas + bump version STD-010 → v1.3.0)
target: TD-D6 — extender STD-010 §2.5 con cuatro clausulas adicionales (§2.5.4 a §2.5.7) cubriendo los grupos de archivos que generan falsos positivos por su naturaleza documental: procedimientos operativos, ADRs de gobernanza, plantillas tecnicas, y analisis de arquitectura modular. Mismo patron que TD-D5 (mecanismo §2.5 ya establecido en v1.2.0).
predecessor_wp: 2026-05-08-03-38-01-tdd5-std010-scope-clarification (cerrado)
trigger: directiva del ejecutor "Abre TD-D6 con ese scope exacto."
```

# TD-D6 — STD-010 §2.5.4 a §2.5.7 scope extension

## Origen del WP

TD-D5 v1.2.0 establecio §2.5 con tres exenciones por
**circularidad semantica** (identity files, landing page,
testing). El reporte de cierre identifico honestamente 230 refs
adicionales en cuatro grupos que generan los mismos falsos
positivos por la misma razon: son archivos que por su naturaleza
documental necesitan nombrar tecnologias concretas.

El ejecutor decidio cubrirlos con cuatro clausulas adicionales
para cerrar el roadmap CLEAN_CODE remediation sin deuda activa.

## Conteo verificado de refs

| Grupo | Refs |
|---|---|
| `normativa/procedimientos/**` | 127 |
| `normativa/gobernanza/adr-*` | 46 |
| `normativa/estandares/plantillas/**` | 51 |
| `gestion/evidencia/arquitectura-modular/**` | 6 |
| **Total** | **230** |

Diferencia con conteo de TD-D5 (155 + 50 + 19 + 6 = 230):
plantillas resulta mayor (51 vs 19) porque cuenta refs en sub-
plantillas anidadas; procedimientos menor (127 vs 155) por
trabajo de WPs intermedios.

## Cuatro exenciones a agregar en STD-010 §2.5

### §2.5.4 Procedimientos operativos — instrucciones ejecutables

Archivos en `normativa/procedimientos/` documentan procesos
operativos del proyecto: DevOps automation, gobernanza SDLC,
generacion de artefactos, despliegue. Son **instrucciones
ejecutables** que requieren nombres tecnologicos concretos
para ser ejecutables.

Ejemplo legitimo:

  "Configurar el job de CI con `runs-on: ubuntu-latest`
  ejecutando `pytest --django-settings=...`"

Abstraerlo a "el Procesador Asincrono ejecutando el Framework
de Tests" elimina la utilidad operativa del documento.

### §2.5.5 ADRs (Architecture Decision Records)

Archivos en `normativa/gobernanza/adr-*` y `arquitectura-tecnica/
modulos/*/decisiones/adr-*` registran **decisiones tecnologicas
documentadas**: por que se eligio Redis vs Memcached, por que
PostgreSQL para audit log, por que Django REST Framework vs
FastAPI. El proposito del ADR es nombrar la tecnologia y la
alternativa descartada — abstraerlo elimina la decision.

Ejemplo legitimo:

  "Decision: usar PostgreSQL para audit_log, no MySQL,
  porque PostgreSQL soporta CHECK constraints sobre row
  immutability y MySQL no lo hace consistentemente."

### §2.5.6 Plantillas tecnicas con ejemplos concretos

Archivos en `normativa/estandares/plantillas/**` proveen
**plantillas con ejemplos concretos** que el usuario rellena.
Los ejemplos requieren nombres tecnologicos para ilustrar el
patron correctamente:

  "Plantilla de UC implementacion-tecnica:
   ## Stack
   - Backend: Django REST Framework con FunctionAccessPolicy
   - Cache: Redis (TTL 300s)
   ..."

El usuario que rellena la plantilla copia el patron; abstraer
los ejemplos lo deja sin guia.

### §2.5.7 Analisis de arquitectura modular

Archivos en `gestion/evidencia/arquitectura-modular/**` son
**evidencia de analisis arquitectonico real** del sistema:
documentan cuales tecnologias se uso, como se modularizo el
codigo, cuales librerias se importaron donde. Tienen el mismo
caracter que los identity files (§2.5.1) pero a granularidad
de modulo.

## Output esperado

- `STD-010 v1.2.0 → v1.3.0` (MINOR: amplia ambito).
- Nuevas secciones §2.5.4, §2.5.5, §2.5.6, §2.5.7.
- Tabla §2.1 actualizada con cuatro filas adicionales.
- Historial v1.3.0 en §8.
- 230 refs movidas a estado "exento normativamente".

## Refs

- TD-D5 `2026-05-08-03-38-01-tdd5-std010-scope-clarification`
  (mecanismo §2.5 establecido).
- WP-G `2026-05-08-03-08-21-wpg-std010-cleanup` (origen del
  diferimiento).
- STD-010 v1.2.0 §2.5 (template para §2.5.4-§2.5.7).
