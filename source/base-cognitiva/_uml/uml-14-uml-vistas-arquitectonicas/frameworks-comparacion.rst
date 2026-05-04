.. meta::
 :artefacto: UML_14_FRAMEWORKS
 :tipo: Referencia — Comparacion de Frameworks
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-frameworks:

=======================================================
Mapeo entre Rozanski et al. y otros frameworks
=======================================================

La siguiente tabla muestra cómo los seis viewpoints de Rozanski
et al. se corresponden con los viewpoints equivalentes en otros
frameworks de arquitectura de software ampliamente utilizados.

.. list-table:: Tabla 2 — Mapeo entre el framework Rozanski et al. y otros frameworks
 :header-rows: 2
 :stub-columns: 1
 :widths: 18 14 14 14 14 13 13

 * - Viewpoint Frameworks
   - Functional
   - Information
   - Concurrency
   - Development
   - Deployment
   - Operational
 * -
   - *(estructura funcional)*
   - *(datos: definición, almacenamiento, acceso)*
   - *(mapeo funcional → concurrente)*
   - *(proceso de desarrollo: código, build, release)*
   - *(estructura física del hardware)*
   - *(operación en producción)*
 * - **Kruchten [4]**
   - Logical
   -
   - Process
   - Development
   - Physical
   -
 * - **Soni et al. [5]**
   - Conceptual Architecture
   -
   - Execution Architecture
   - Code, Module
   -
   -
 * - **Clements et al. [6]**
   - Component & Connector
   - Component & Connector
   - Component & Connector
   - Module
   - Allocation
   -
 * - **Garland et al. [7]**
   - Component and Component Interaction
   - Logical Data, Data Model, Transaction
   - Process, Proc. State
   - Layered Subsys., Subsys. Interface, Dependency
   - Deployment and Physical Data
   -

Observaciones
==============

**Kruchten 4+1** es el framework con correspondencia más directa:

- **Logical** → Functional (estructura estática del sistema)
- **Process** → Concurrency (concurrencia y sincronización)
- **Development** → Development (organización del código)
- **Physical** → Deployment (distribución en hardware)
- La vista **Use Case (+1)** de Kruchten actúa como unificadora
  y no tiene equivalencia directa en Rozanski — es transversal.
- El viewpoint **Operational** de Rozanski no tiene equivalente
  en Kruchten 4+1 ni en los otros tres frameworks, lo que
  subraya su originalidad: los demás frameworks asumen que la
  operación del sistema en producción queda fuera del alcance
  del modelado arquitectónico.

**Clements et al.** usa Component & Connector para cubrir
Functional, Information y Concurrency simultáneamente — un solo
tipo de vista para tres preocupaciones distintas. Esto refleja
un enfoque más abstracto donde la distinción entre flujo de
datos, estructura funcional y concurrencia se resuelve con un
único mecanismo de composición.

**Garland et al.** es el framework más detallado en
Information (tres model types distintos: Logical Data, Data
Model, Transaction) y en Development (cuatro model types:
Layered Subsystems, Subsystem Interface, Dependency). Esto
indica una mayor granularidad para sistemas con arquitecturas
de capas complejas.

Relevancia para el modelo 5+1 de IACT
=======================================

El proyecto IACT usa el modelo **5+1 (variante DDD de
Kruchten)**, que extiende el 4+1 original de Kruchten con la
**Vista de Dominio** (*Domain Model*). Usando esta tabla como
referencia:

.. list-table::
 :header-rows: 1
 :widths: 25 25 50

 * - Vista 5+1 IACT
   - Rozanski et al.
   - Correspondencias con otros frameworks
 * - Domain Model
   - Information (parcial)
   - Garland: Logical Data, Data Model
 * - Use Case View
   - Functional
   - Kruchten: Logical · Clements: Component & Connector
 * - Design View
   - Development (parcial)
   - Kruchten: Development · Garland: Subsys. Interface
 * - Implementation View
   - Development
   - Soni: Code, Module · Clements: Module
 * - Process View
   - Concurrency
   - Kruchten: Process · Soni: Execution Architecture
 * - Deployment View (+1)
   - Deployment
   - Kruchten: Physical · Clements: Allocation

El viewpoint **Operational** de Rozanski no tiene cobertura
en el modelo 5+1 actual del proyecto — coincide con que
ninguno de los frameworks comparados (Kruchten, Soni, Clements,
Garland) lo incorpora explícitamente.

----

Referencias cruzadas
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Contexto empírico**
   - :doc:`contexto-empirico`
 * - **Meta-modelo (Figura 1)**
   - :doc:`metamodelo-descripcion`
 * - **Framework Rozanski — Tabla 1**
   - :doc:`framework-rozanski`
