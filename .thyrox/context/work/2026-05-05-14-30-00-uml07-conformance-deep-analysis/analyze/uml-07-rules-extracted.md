```yml
created_at: 2026-05-05 14:32:00
project: IACT-docs
work_package: 2026-05-05-14-30-00-uml07-conformance-deep-analysis
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Reglas canónicas de uml-07 (cita literal)

12 reglas extraídas de los 11 archivos en
``source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/``.

## R-01 — Actor iniciador a la izquierda; beneficiario a la derecha

**Fuente:** ``representacion-de-un-modelo-de-caso-de-uso.rst``.

> Un actor es quien **inicia** un caso de uso, y otro actor
> (posiblemente el que inició, pero no necesariamente) es
> quien **recibe** algo de valor de él.
>
> El actor que **inicia** se encuentra a la izquierda del
> caso de uso, y el que **recibe** a la derecha.

**Sintaxis canónica:**

```
A --> UC      (iniciador)
UC --> B      (beneficiario)
```

## R-02 — Actor = stick figure; UC = elipse

**Fuente:** ``representacion-de-un-modelo-de-caso-de-uso.rst``.

> Una **elipse** representa a un caso de uso y una
> **figura agregada** (stick figure) representa a un
> actor.

PlantUML: ``actor`` y ``usecase`` keywords.

## R-03 — Sistema = rectangle envuelve los UCs

**Fuente:** ``representacion-de-un-modelo-de-caso-de-uso.rst``.

> Se utiliza un **rectángulo** (con el nombre del sistema
> dentro) para representar el confín del sistema; el
> rectángulo envuelve a los casos de uso.

## R-04 — Línea asociativa actor↔UC sin estereotipo

**Fuente:** ``representacion-de-un-modelo-de-caso-de-uso.rst``.

> En UML una **línea asociativa** conecta a un actor con
> el caso de uso, y representa la comunicación entre
> ambos.

PlantUML: `-->` simple, sin `<<...>>`.

## R-05 — Actores en jerarquía de generalización

**Fuente:** ``comprension-de-los-usuarios.rst``.

> Sería conveniente mostrar a los usuarios en una
> **jerarquía de generalización**.

PlantUML: ``Empleado <|-- Consultor``.

## R-06 — `<<include>>` con línea discontinua + flecha

**Fuente:** ``inclusion.rst``.

> Para representar la inclusión utilizará el símbolo que
> usó para la dependencia entre clases: una **línea
> discontinua con una punta de flecha** que conecta los
> casos de uso apuntando hacia el caso de uso
> dependiente; sobre la línea agregará un estereotipo:
> la palabra ``<<incluir>>`` (o ``<<include>>``)
> bordeada por dos pares de paréntesis angulares.

**Sintaxis canónica:** ``UC_BASE ..> UC_INCLUIDO : <<include>>``.

## R-07 — UC incluido NUNCA aparece solo

**Fuente:** ``inclusion.rst``.

> Un caso de uso incluido **nunca aparecerá solo**:
> funciona como parte de un caso de uso que lo incluya.

**Implicación:** un UC marcado como `<<include>>`-only
(ej: UC_INC_RPT_01 Resolver Segmento) NO debe tener
diagrama standalone propio, NO debe ser invocado por
actor directamente.

## R-08 — `<<extend>>` con línea discontinua + flecha

**Fuente:** ``extension.rst``.

> Podrá concebir la extensión con una línea de
> dependencia (línea discontinua con punta de flecha),
> junto con un estereotipo que muestra ``<<extender>>``
> (o ``<<extend>>``) entre paréntesis angulares.

**Sintaxis canónica:** ``UC_EXTENSION ..> UC_BASE : <<extend>>``.

Nota: la flecha del extends apunta al **UC base** (al
revés del include cognitive — extends "aporta a"
otro UC).

## R-09 — UC base con extends muestra extension points

**Fuente:** ``extension.rst``.

> el punto de extensión aparecerá debajo del nombre del
> caso de uso

**Sintaxis canónica:**

```
usecase "Reabastecer\n.. extension points ..\nLlenar los compartimientos" as UC2
```

## R-10 — Generalización entre UCs y entre actores

**Fuente:** ``generalizacion.rst``.

> Modelará la generalización de casos de uso con líneas
> continuas y una **punta de flecha en forma de
> triángulo sin rellenar** que apunta hacia el caso de
> uso primario.
>
> La relación también se puede establecer entre
> **actores**, así como entre casos de uso.

**Sintaxis canónica:** ``UC_HIJO --|> UC_PADRE`` o
``Actor_HIJO <|-- Actor_PADRE``.

## R-11 — UCs de alto nivel con detalle de pasos incluidos

**Fuente:** ``profundizacion.rst``.

> Determinar cuáles son los casos de uso de alto nivel y
> a partir de ellos, generar el modelo detallado.
>
> Ciertos pasos se repetirán de un caso de uso a otro, y
> ello le llevará a otros casos de uso (posiblemente
> incluidos)

**Implicación:** el diagrama de un UC operativo
**SIEMPRE muestra** los UCs incluidos que detallan sus
pasos. NO es un singleton.

## R-12 — Análisis describe comportamiento, NO implementación

**Fuente:** ``profundizacion.rst``.

> Recuerde que **el análisis del caso de uso describe el
> comportamiento de un sistema, nunca toca a la
> implementación**.

**Implicación:** PROHIBIDO en diagramas de uml-07:

- Nombres de servicios concretos (``ServicioReportes``,
  ``AbandonmentReportService``).
- Codenames RBAC (``view_dashboard``).
- Nombres de SP/tablas SQL (``sp_rpt_centros_xsegmento``,
  ``etl_runs``).
- Nombres de tecnologías (``PostgreSQL``, ``Redis``).
- Endpoints HTTP, paths URL, tipos de archivos.

----

## Reglas adicionales emergentes (no canónicas pero coherentes)

R-X (Clean Code, no en uml-07 directo): nombres
descriptivos para UCs (intention-revealing) — el libro
usa "Reabastecer", "Comprar gaseosa", "Crear una
propuesta", NUNCA "UC-001" o "UC_X_01" como label
visible.

**Cita relacionada (extension.rst):**

```
usecase "Reabastecer\n.. extension points ..\nLlenar los compartimientos"
```

El UC label es la acción descriptiva, no un identificador.
