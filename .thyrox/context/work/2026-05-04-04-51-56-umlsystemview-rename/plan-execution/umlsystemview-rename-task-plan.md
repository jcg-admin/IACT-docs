```yml
created_at: 2026-05-04 04:51:56
project: IACT-docs
work_package: 2026-05-04-04-51-56-umlsystemview-rename
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Pendiente
```

# Task Plan — Nombres Genéricos UMLSystemView

Renombrar 7 archivos con nombres genéricos en UMLSystemView a nombres
auto-descriptivos que reflejen el contenido del diagrama.

---

## Bloque A — Verificar headings y definir nombres finales

- [x] **T-001** Leer heading principal de cada archivo genérico para confirmar
  nombre correcto:
  - `casos-uso.rst`, `clases.rst`, `componentes.rst`, `comunicacion.rst`
  - `despliegue.rst`, `maquina-estados.rst`, `secuencia.rst`

---

## Bloque B — Renombrar archivos

- [x] **T-002** `git mv` de los 7 archivos:
  - `casos-uso.rst` → `casos-uso-sistema-iact.rst`
  - `clases.rst` → `clases-sistema-iact.rst`
  - `componentes.rst` → `componentes-sistema-iact.rst`
  - `comunicacion.rst` → `comunicacion-sistema-iact.rst`
  - `despliegue.rst` → `despliegue-sistema-iact.rst`
  - `maquina-estados.rst` → `maquina-estados-sistema-iact.rst`
  - `secuencia.rst` → `secuencia-sistema-iact.rst`

---

## Bloque C — Actualizar referencias

- [x] **T-003** Actualizar `UMLSystemView/index.rst` toctree con nuevos nombres
- [x] **T-004** Buscar y actualizar cualquier `:doc:` referencia a estos archivos
  en el resto del repo

---

## Bloque D — Verificación

- [x] **T-005** Confirmar que no queden archivos con nombres genéricos:
  ```bash
  ls source/arquitectura-tecnica/UMLSystemView/ | grep -E "^(casos-uso|clases|componentes|comunicacion|despliegue|maquina-estados|secuencia)\.rst"
  ```
  Resultado esperado: 0 archivos

---

## Orden de ejecución

```
A (T-001) → B (T-002) → C (T-003, T-004) → D (T-005)
```
