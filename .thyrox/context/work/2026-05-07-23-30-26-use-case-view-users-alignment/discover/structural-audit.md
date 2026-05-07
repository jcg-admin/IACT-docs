```yml
created_at: 2026-05-07 23:35:00
project: IACT-docs
work_package: 2026-05-07-23-30-26-use-case-view-users-alignment
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: Structural Audit
```

# Audit estructural use-case-view vs casos-uso

## 1. Modelo conceptual del proyecto

Segun `source/arquitectura-tecnica/use-case-view/index.rst` v3.0.0:

> "Cada modulo es un directorio que contiene su diagrama en
> `index.rst`. La organizacion refleja la de
> `source/requisitos/casos-uso/` (paridad estructural por
> directorio). 13 modulos, 1 diagrama por modulo, 83 UCs
> cubiertos en total."

**Hallazgo:** el index declara 83 UCs pero el conteo real
es 85 (delta +2 — probablemente uc-acc-08, uc-acc-09 no
contados originalmente).

## 2. Conteo actual

### use-case-view (85 archivos UC)

| Cluster | Archivos | Listado |
|---|---|---|
| access | 7 | uc-acc-01..05, 08, 09 |
| admin | 5 | uc-adm-01..05 |
| alerts | 5 | uc-alr-01..05 |
| audit | 4 | uc-aud-01..04 |
| auth | 5 | uc-auth-01..05 |
| caller | 5 | uc-cli-01..05 |
| logs | 7 | uc-log-01..07 |
| operator | 10 | uc-opr-01..10 |
| permissions | 10 | uc-perm-01..10 |
| pipeline | 4 | uc-pip-01..04 |
| reports | 16 | uc-inc-rpt-01, uc-rpt-01..04, 07..17 |
| supervision | 3 | uc-sup-01..03 |
| users | **4** | uc-usr-01..04 |

### casos-uso (88 directorios)

| Cluster | Directorios | Diff con use-case-view |
|---|---|---|
| access | 7 | OK |
| admin | 5 | OK |
| alerts | 5 | OK |
| audit | 4 | OK |
| auth | 5 | OK |
| caller | 5 | OK |
| logs | 7 | OK |
| operator | 10 | OK |
| permissions | 10 | OK |
| pipeline | 4 | OK |
| reports | 16 | OK |
| supervision | 3 | OK |
| users | **7** | **+3 (uc-usr-05/06/07)** |

## 3. Estructura de un UC

### En casos-uso (13 archivos por UC tipico)

```
source/requisitos/casos-uso/{cluster}/uc-{id}/
├── actores-precondiciones.rst
├── criterios-aceptacion.rst
├── datos-involucrados.rst
├── diagramas-uml/
│   ├── diagrama-de-caso-de-uso.rst
│   ├── diagrama-de-actividad.rst
│   ├── diagrama-de-secuencia.rst
│   └── ...
├── excepciones.rst
├── flujo-principal.rst
├── flujos-alternos.rst
├── implementacion-tecnica.rst
├── index.rst
├── informacion-general.rst
├── patrones-diseno.rst
├── requisitos-no-funcionales.rst
└── testing.rst
```

### En use-case-view (1 archivo .rst por UC)

```
source/arquitectura-tecnica/use-case-view/{cluster}/uc-{id}-{slug}.rst
```

Contenido tipico (ver uc-acc-01-asignar-funciones.rst):

- `.. meta::` con
  `:artefacto: AT_UC_{ID}_USECASE`,
  `:tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone`,
  `:dominio: arquitectura_tecnica`,
  `:subdominio: UseCaseView`,
  `:modulo: {cluster}`,
  `:estado: Vigente`,
  `:version: 1.0.0`.
- Anchor `.. _at_uc_{id}_{slug}:`.
- Titulo `UC_{ID} — {Nombre}`.
- Descripcion del UC (1-2 parrafos).
- Bloque `.. uml::` standalone (uml-07 actores-y-casos).
- `.. seealso::` con cross-ref al UC en casos-uso.

## 4. UCs Reservado en casos-uso (3 archivos)

### uc-usr-05 — Bloquear Usuario

```
.. meta::
 :artefacto: UC_USR_05
 :tipo: Caso de Uso (stub Reservado)
 :estado: Reservado
 :version: 0.1.0
 :origen: incierto — referenciado en uc-auth-03/04/05
          sin decision arquitectonica formal documentada
```

Estructura: solo `index.rst` (sin diagramas, sin
flujo-principal, etc.). Es un stub con warning.

### uc-usr-06 — Desbloquear Usuario

Counterpart de uc-usr-05. Mismo patron.

### uc-usr-07 — Editar Perfil Propio

Referenciado en uc-usr-02. Mismo patron.

## 5. Patron de toctree en casos-uso/users/index.rst

```rst
.. toctree::
 :maxdepth: 2

 uc-usr-01/index
 uc-usr-02/index
 uc-usr-03/index
 uc-usr-04/index

UCs Reservados (planificados, sin spec completa)
=================================================

Los siguientes UCs estan declarados como **Reservado** —
referenciados en otros UCs pero sin decision arquitectonica
formal sobre su scope ni capability RBAC. Requieren ADR
explicito antes de promover a Borrador / Vigente.

.. toctree::
 :maxdepth: 1

 uc-usr-05/index
 uc-usr-06/index
 uc-usr-07/index
```

## 6. Estado de use-case-view/users/index.rst

Solo lista los 4 UCs Vigente. **No menciona** los 3
Reservados ni en la tabla de UCs ni en toctree.

## 7. Conclusion

La desalineacion es de **3 UCs Reservado**, intencional o
incidentalmente excluidos de use-case-view. Para alinear
con el patron de casos-uso, hay 3 opciones:

### Opcion A: Crear placeholders Reservado en use-case-view

Crear 3 archivos `uc-usr-0{5,6,7}-{slug}.rst` con metadata
`:estado: Reservado`, sin diagrama plantuml, con warning y
cross-ref al stub en casos-uso. Actualizar
use-case-view/users/index.rst con seccion analoga.

**Ventaja:** paridad estructural completa. Mejor
descubribilidad de Reservados desde la vista
arquitectonica.

**Desventaja:** archivos placeholder son ruido — duplican
el warning ya presente en casos-uso.

### Opcion B: Solo actualizar use-case-view/users/index.rst

Agregar seccion "UCs Reservados" en el index sin crear
archivos individuales. Solo cross-refs a los stubs de
casos-uso.

**Ventaja:** sin duplicacion. La info de Reservados queda
visible en use-case-view.

**Desventaja:** paridad estructural NO completa
(directorio use-case-view/users/ tiene 4 archivos vs 7 en
casos-uso/users/). El conteo "1 archivo por UC en
use-case-view" no se cumple.

### Opcion C: Documentar exclusion explicita

Mantener la exclusion actual + documentar en el index.rst
de use-case-view la regla "Reservados se documentan
exclusivamente en casos-uso".

**Ventaja:** menor cambio. Politica explicita.

**Desventaja:** el ejecutor pidio paridad ("lo que se tiene
en casos-uso se debe tener en use-case-view"), por lo que
esta opcion contradice el trigger.

## 8. Recomendacion

**Opcion A** — paridad estructural completa con placeholders.

Razones:

- Cumple el requerimiento "lo que se tiene en casos-uso se
  tiene en use-case-view".
- Replica el patron observado en casos-uso/users/index.rst
  (toctree separado para Reservados).
- Permite evolucion futura: cuando un UC Reservado se
  promueva a Vigente, se modifica el archivo existente en
  vez de crearlo.

## Refs

- `source/arquitectura-tecnica/use-case-view/index.rst` v3.0.0.
- `source/arquitectura-tecnica/use-case-view/users/index.rst`.
- `source/requisitos/casos-uso/users/index.rst`.
- `source/requisitos/casos-uso/users/uc-usr-{05,06,07}/index.rst`.
