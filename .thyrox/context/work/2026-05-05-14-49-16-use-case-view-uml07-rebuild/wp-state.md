```yml
project: IACT-docs
work_package: 2026-05-05-14-49-16-use-case-view-uml07-rebuild
created_at: 2026-05-05 14:49:16
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-validation
predecessor_wp: 2026-05-05-14-30-00-uml07-conformance-deep-analysis
target: Construir 83 diagramas per-UC en use-case-view conforme a uml-07, con nombres auto-explicativos
```

# WP — Use Case View UML-07 Rebuild

## Trigger

El predecesor cerró las violaciones de uml-07 a nivel
módulo, pero **NO produjo diagramas per-UC útiles**
(los 83 stubs de Phase 1 fueron eliminados por triviales).

El usuario pide ahora la versión correcta:

> en source/arquitectura-tecnica/use-case-view/* es
> source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/*
> ... los nombres de los diagramas van a ser
> auto explicativos, ejemplo
> uc-acc-01-{nombre-del diagrama}
> ... te vas a basar de lo que tiene
> source/requisitos/casos-uso/*

## Distinción clarificada

| Artefacto | Reference uml | Contiene |
|-----------|---------------|----------|
| ``source/requisitos/casos-uso/<module>/<uc>/`` | uml-06 (introduccion) | Specs textuales de 12-13 partes (informacion-general, flujo-principal, excepciones, criterios-aceptacion, etc.) |
| ``source/arquitectura-tecnica/use-case-view/<module>/`` | uml-07 (diagramas) | **Diagramas** de casos de uso conforme uml-07 con `<<include>>`, `<<extend>>`, actor beneficiario, extension points |

## Inventario (83 UCs)

| Módulo | UCs | Con src diagram en casos-uso | Nuevos |
|--------|-----|------------------------------|--------|
| access | 7 | 7 | 0 |
| admin | 3 | 0 | 3 |
| alerts | 5 | 0 | 5 |
| audit | 4 | 0 | 4 |
| auth | 5 | 5 | 0 |
| caller | 5 | 0 | 5 |
| logs | 7 | 0 | 7 |
| operator | 10 | 0 | 10 |
| permissions | 10 | 7 | 3 |
| pipeline | 4 | 0 | 4 |
| reports | 16 | 7 | 9 |
| supervision | 3 | 0 | 3 |
| users | 4 | 4 | 0 |
| **TOTAL** | **83** | **30** | **53** |

Inventario completo (machine-readable):
``discover/inventory.json``.

## Convenciones de naming aplicadas

**Formato:** ``<uc-id-kebab>-<slug-descriptivo>.rst``

| Antes (stub) | Ahora (auto-explicativo) |
|--------------|--------------------------|
| ``uc-acc-01/index.rst`` | ``uc-acc-01-asignar-funciones.rst`` |
| ``uc-rpt-04/index.rst`` | ``uc-rpt-04-exportar-reporte.rst`` |
| ``uc-auth-03/index.rst`` | ``uc-auth-03-recuperar-contrasena.rst`` |

Reglas:

- Prefijo ``uc-XXX-NN-`` preserva trazabilidad al ID
  canónico de casos-uso.
- Slug en kebab-case en castellano (titulo del UC en
  casos-uso).
- Sin acentos, sin caracteres especiales.
- Sin sub-directorio: archivo directo en ``<module>/``.

**Ubicación final:**

```
use-case-view/<module>/uc-XXX-NN-<slug>.rst
```

## Reglas uml-07 aplicables (de WP predecesor)

| ID | Regla | Aplica per-UC |
|----|-------|---------------|
| R-01 | Actor iniciador izq, beneficiario der | ✓ donde semántica exista |
| R-02 | Stick figure + elipse | ✓ todos |
| R-03 | Rectangle = sistema (MOD_X) | ✓ todos |
| R-04 | Línea asociativa sin estereotipo | ✓ todos |
| R-05 | Jerarquía actores | ✗ — BR-006 Flat NIST prohíbe |
| R-06 | `<<include>>` con `..>` | ✓ donde aplique |
| R-07 | UC included nunca solo | ✓ — uc-inc-rpt-01 NO recibirá archivo standalone |
| R-08 | `<<extend>>` con `..>` (ext → base) | ✓ donde aplique |
| R-09 | Extension points en label del UC base | ✓ |
| R-10 | Generalización UCs `--|>` | △ — opcional, evaluar caso por caso |
| R-11 | UCs alto nivel con detalle | ✓ |
| R-12 | NO detalles implementación | ✓ — sin SP/SQL/codenames como UC |

## Restricciones IACT

- **BR-006 RBAC Flat NIST + CNST-005**: NO `<|--` entre
  actores. Ningún diagrama tendrá jerarquía.
- **CNST-033**: identificadores de actor en inglés
  (``Operator``, ``Supervisor``, ``Caller``).
- **STD-008**: identifiers en inglés.

## Estrategia de generación

### Opción A — Aprovechar src diagram donde exista (30 UCs)

Para los 30 UCs que ya tienen
``casos-uso/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst``:

1. Leer el `@startuml` block existente.
2. **Sanitizar**:
   - Reemplazar codename actors (``view_reports``,
     ``assign_functions``) por roles canónicos
     (``Operator``, ``AccessAdmin``, etc.).
   - Eliminar ``<|--`` entre actores (BR-006).
   - Verificar/corregir dirección de `<<extend>>`.
   - Eliminar nombres de SP/SQL del label de UCs.
3. Guardar en ``use-case-view/<module>/<uc>-<slug>.rst``.

### Opción B — Generar desde cero (53 UCs)

Para los 53 sin src diagram:

1. Leer ``casos-uso/<uc>/index.rst`` + ``flujo-principal``
   + ``actores-precondiciones`` para extraer:
   - Actor primario.
   - UCs incluidos (de "PASO X — Validar...", llamadas a
     otros UCs, etc.).
   - UCs que extienden este (buscar refs cruzados).
2. Construir el `@startuml` con uml-07 estricto.
3. Guardar.

## Output esperado

- 83 archivos en ``use-case-view/<module>/uc-XXX-NN-<slug>.rst``.
- Cada module index actualizado con xref table que linkea
  a esos archivos (en lugar de la xref a casos-uso que
  está actualmente).
- 0 errores de pre-render.
- Auditoría final con script: 0 violaciones de uml-07
  rules + 0 violaciones de BR-006.

## Riesgos

- **R1**: 53 UCs sin src diagram requieren inferencia
  desde flujo-principal — riesgo de imprecisión.
  Mitigación: marcarlos como ``draft`` v0.9 hasta
  revisión humana.
- **R2**: los 30 src diagrams tienen errores conocidos
  (codename actors, posibles `<|--`, dirección extends).
  Sanitización podría perder semántica si no se hace
  carefully.
- **R3**: 83 archivos × tiempo de revisión humana
  = mucho effort downstream. Solución: scripted
  generation con plantilla deterministica.

## Stopping points

- **SP-01**: validar plan antes de ejecutar (este
  documento).
- **SP-02**: tras generar 5 archivos sample (uno por
  módulo principal), validar pattern con ejecutor.
- **SP-03**: tras generación masiva, audit script
  verificar 0 violaciones.
- **SP-04**: pre-merge, build limpio.

## Decisiones pendientes del ejecutor

1. ¿Aprobar el formato de naming
   ``uc-XXX-NN-<slug-descriptivo>.rst``?
2. ¿Aprobar Opción A para los 30 + Opción B para los 53?
3. ¿Marcar los 53 nuevos como ``draft v0.9`` hasta
   revisión humana, o como ``v1.0.0 Vigente``?
4. ¿Ejecutar masivamente o por módulos (validar uno antes
   del siguiente)?
