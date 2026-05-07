.. meta::
 :artefacto: STD_012
 :tipo: Estándar
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.1.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno

.. _std-012:

=================================================================
STD_012: Tipos de Diagramas UML — Cuándo y Dónde Usar Cada Uno
=================================================================

.. contents:: Contenido
 :depth: 3
 :local:

----

1. Propósito
============

Este estándar define **qué tipo de diagrama UML va en qué
artefacto** del proyecto IACT, evitando ambigüedad y duplicación
entre artefactos arquitectónicos y de requisitos.

**Confusión más común:** distinguir un *diagrama de clases*
(``class``) de un *diagrama de objetos* (``object``). Ambos
viven en UML pero responden a preguntas distintas y van en
ubicaciones distintas del proyecto.

Referencia metodológica:
:doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama/diagrama-de-clases`,
:doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama/diagrama-de-objetos`.

----

2. Distinción Clase vs. Objeto
==============================

2.1 Definición canónica
-----------------------

.. list-table::
 :widths: 20 40 40
 :header-rows: 1

 * - Eje
   - Diagrama de clases
   - Diagrama de objetos
 * - Pregunta que responde
   - ¿Qué tipos existen?
   - ¿Qué hay en este momento concreto?
 * - Granularidad
   - Categoría (molde genérico)
   - Instancia específica (caso concreto)
 * - Notación PlantUML
   - ``class User { ... }``
   - ``object "juan : User" { username = "juan.perez" }``
 * - Atributos
   - Tipos sin valores
   - Valores concretos
 * - Operaciones
   - Firmas (parámetros + retorno)
   - No aplican (los objetos solo tienen estado)
 * - Relaciones
   - Asociación, agregación, herencia, dependencia
   - Links concretos entre instancias

2.2 Ejemplo lado a lado
-----------------------

**Clase** (estructura genérica):

.. code-block:: text

   class User {
     - id : UUID
     - username : String
     - state : UserState
     + deactivate(reason : String) : void
     + block(reason : String) : void
   }

**Objeto** (instancia concreta del caso):

.. code-block:: text

   object "juan : User" as juan {
     id = "550e8400-e29b-41d4-a716-446655440000"
     username = "juan.perez"
     state = ACTIVE
     last_login_at = "2026-05-04T10:30:00Z"
   }

   object "session-9a3f : Session" as s {
     user_id = "550e8400-..."
     expires_at = "2026-05-04T18:30:01Z"
   }

   juan --> s : posee

----

3. Catálogo de Diagramas UML del Proyecto
=========================================

3.1 Tabla maestra: dónde va cada tipo
-------------------------------------

.. list-table::
 :widths: 18 30 22 30
 :header-rows: 1

 * - Tipo de diagrama
   - Ubicación canónica
   - Granularidad
   - Cuándo usar
 * - **Clases (estructura)**
   - ``arquitectura-tecnica/domain-model/{class}.rst``
   - 1 clase / archivo
   - Documentar el catálogo de tipos del dominio.
 * - **Objetos (instancias)**
   - ``casos-uso/{cluster}/{uc}/diagramas-uml/escenario-*.rst``
     (opcional, ad-hoc)
   - 1 escenario / archivo
   - Ilustrar un flujo concreto, una violación específica,
     un fixture de prueba.
 * - **Casos de uso**
   - ``casos-uso/{cluster}/{uc}/diagramas-uml/diagrama-de-caso-de-uso.rst``
     +
     ``arquitectura-tecnica/use-case-view/{cluster}/{uc}-{nombre}.rst``
   - 1 UC / archivo (spec) + 1 vista módulo
   - Spec del UC: actores + relaciones include/extend.
     Vista arq: módulo entero.
 * - **Secuencia**
   - ``casos-uso/{cluster}/{uc}/diagramas-uml/diagrama-de-secuencia*.rst``
   - 1 escenario / archivo
   - Mostrar interacción cronológica entre componentes.
 * - **Actividad**
   - ``casos-uso/{cluster}/{uc}/diagramas-uml/diagrama-de-actividad.rst``
   - 1 flujo / archivo
   - Flujo de control con decisiones (if/else) y forks.
 * - **Estados**
   - ``casos-uso/{cluster}/{uc}/diagramas-uml/diagrama-de-estados-{entidad}.rst``
   - 1 entidad / archivo
   - Ciclo de vida de una entidad con state machine.
 * - **Componentes**
   - ``arquitectura-tecnica/{view}/diagrama-de-componentes-*.rst``
   - 1 vista / archivo
   - Bloques arquitectónicos y sus dependencias.
 * - **Distribución (deployment)**
   - ``arquitectura-tecnica/deployment-view/*.rst``
   - 1 vista / archivo
   - Nodos físicos / containers / runtimes.
 * - **Colaboración**
   - raro (preferir secuencia)
   - 1 escenario / archivo
   - Variante de secuencia con énfasis en estructura.

3.2 Una clase por archivo (regla específica del domain-model)
-------------------------------------------------------------

En ``arquitectura-tecnica/domain-model/`` la regla es estricta:

- **1 archivo = 1 clase** del catálogo.
- **No mezclar** múltiples clases en un mismo ``.rst`` salvo en
  ``index.rst`` y ``overview.rst`` (que son catálogos).
- El nombre del archivo debe ser ``{name}.rst`` en kebab-case
  derivado del PascalCase de la clase
  (``AccessGroupFunction`` → ``access-group-function.rst``).

3.3 Un diagrama por archivo (regla general)
-------------------------------------------

Para los demás diagramas del proyecto (casos-uso,
arquitectura-tecnica), la regla es:

- **1 archivo = 1 diagrama** salvo excepción documentada.
- **Excepción permitida**: variantes muy próximas del mismo
  escenario (ej. flujo principal + flujo alterno cortos en
  el mismo archivo si están explícitamente etiquetadas).
- En toda excepción, agregar al inicio del archivo una nota
  justificando por qué no se separó.

----

4. Reglas de Ubicación
======================

4.1 Domain model: solo clases
-----------------------------

Los archivos de ``arquitectura-tecnica/domain-model/`` contienen
**únicamente diagramas de clases**. Nunca diagramas de objetos.

Razón: el dominio se modela por tipos. Las instancias son
runtime, no diseño. Si necesitas ilustrar instancias de una
clase, hazlo en el contexto de un UC o un escenario.

4.2 Casos de uso: clases solo si son nuevas en el UC
----------------------------------------------------

En ``casos-uso/{cluster}/{uc}/diagramas-uml/`` evitar duplicar
diagramas de clases del domain-model. Si el UC necesita
referenciar una clase, usar ``:doc:`` link al archivo del
domain-model:

.. code-block:: rst

   La operación ``deactivate()`` de :doc:`/arquitectura-tecnica/domain-model/user`
   se invoca en el PASO 7.

Excepción: si el UC introduce una clase de uso interno (helper,
DTO) que no pertenece al dominio canónico, puede tener su
diagrama de clase localmente.

4.3 Diagramas de objetos: opcionales y locales al UC
----------------------------------------------------

Cuando un UC tiene un escenario complejo donde mostrar el
estado concreto del sistema aporta claridad, agregar un
``escenario-*.rst`` con el diagrama de objetos. Casos típicos:

- Violación de SoD ilustrada con instancias concretas.
- Estado del sistema antes/después de un flujo crítico.
- Fixtures de pruebas para reproducir un bug.

**No es obligatorio.** Solo cuando aporta valor explicativo
no cubierto por los demás diagramas.

----

5. Plantilla Mínima por Tipo
============================

5.1 Diagrama de clases (domain-model)
-------------------------------------

.. code-block:: rst

   .. uml::
    :caption: Clase Foo — descripción breve.

    @startuml
    class Foo {
      - id : UUID
      - name : String
      + operate(arg : Type) : ReturnType
    }

    Foo "1" -- "*" Bar : associates
    @enduml

5.2 Diagrama de objetos (escenario)
-----------------------------------

.. code-block:: rst

   .. uml::
    :caption: Escenario X — estado en momento Y.

    @startuml
    object "fooInstance : Foo" as foo {
      id = "uuid-here"
      name = "concrete-value"
    }

    object "barInstance : Bar" as bar {
      id = "another-uuid"
    }

    foo --> bar : associated_with
    @enduml

----

6. Consecuencias y Anti-patrones
================================

6.1 Anti-patrón: clase con valores
----------------------------------

**PROHIBIDO** en domain-model:

.. code-block:: text

   class User {
     - id : UUID = "550e8400-..."        ← anti-patrón
     - username : String = "juan.perez"  ← anti-patrón
   }

Si quieres mostrar valores concretos, usa diagrama de objetos.

6.2 Anti-patrón: objeto sin clase
---------------------------------

**PROHIBIDO** en domain-model y casos-uso:

.. code-block:: text

   object "miUser" as u {           ← falta : Class
     username = "juan"
   }

Sin la parte ``: Class`` el objeto no se ancla al modelo.
Siempre escribir ``object "alias : Class" as alias``.

6.3 Anti-patrón: dos diagramas en un archivo de domain-model
------------------------------------------------------------

**PROHIBIDO**:

.. code-block:: rst

   === user.rst ===

   .. uml::
    @startuml
    class User { ... }
    @enduml

   .. uml::
    @startuml
    class Session { ... }
    @enduml

Cada clase va en su propio archivo (``user.rst``, ``session.rst``).

----

7. Convención de nomenclatura de archivos (v1.1.0)
===================================================

7.1 Prefijo ``diagrama-de-`` obligatorio
----------------------------------------

Todo archivo dentro de ``diagramas-uml/`` que contiene un
diagrama UML DEBE iniciar con el prefijo ``diagrama-de-``.

**Razones:**

(a) **Inequivocidad:** ``caso-de-uso.rst`` puede confundirse
    con un archivo textual del UC. ``diagrama-de-caso-de-uso.rst``
    es inequivoco.

(b) **Alineamiento con STD-011:** los ejemplos canonicos de
    aliases en ``STD-011`` ya usan el prefijo en sus
    snippets (``diagrama-de-secuencia.rst``, etc.).

(c) **Consistencia con la practica reciente:** los UCs
    nuevos creados desde ``2026-05-04`` adoptaron el prefijo
    organicamente.

7.2 Tabla canonica de nombres
-----------------------------

.. list-table::
 :widths: 30 50 20
 :header-rows: 1

 * - Tipo de diagrama
   - Nombre canonico (con prefijo)
   - Variantes
 * - Caso de uso
   - ``diagrama-de-caso-de-uso.rst``
   - ``diagrama-de-caso-de-uso-{contexto}.rst`` (ej:
     ``-relacion-de-inclusion``)
 * - Secuencia
   - ``diagrama-de-secuencia.rst``
   - ``diagrama-de-secuencia-{escenario}.rst`` (ej:
     ``-detalle``, ``-listado``, ``-export``)
 * - Actividad
   - ``diagrama-de-actividad.rst``
   - ``diagrama-de-actividad-{escenario}.rst`` (ej:
     ``-aplicar``, ``-cold``, ``-warm``)
 * - Estados
   - ``diagrama-de-estados-{entidad}.rst``
   - singular: ``diagrama-de-estado-{entidad}.rst``
 * - Clases
   - ``diagrama-de-clases.rst``
   - ``diagrama-de-clases-{contexto}.rst``
 * - Componentes
   - ``diagrama-de-componentes.rst``
   - ``diagrama-de-componentes-{escenario}.rst``

7.3 Excepciones
---------------

**Documentos auxiliares de texto en ``diagramas-uml/``** que
NO contienen un diagrama UML (e.g., ``notas-sobre-los-diagramas.rst``)
no aplican el prefijo. La regla aplica solo a archivos que
contienen ``.. uml::`` o ``@startuml``.

----

8. Referencias
==============

- :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama/diagrama-de-clases`
- :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama/diagrama-de-objetos`
- :doc:`/base-cognitiva/_uml/uml-03-uso-orientacion-objetos/index`
- :doc:`/base-cognitiva/_uml/uml-04-uso-relaciones/index`
- :doc:`/normativa/estandares/std-011-alias-diagramas-uml`

----

9. Historial de Cambios
=======================

.. list-table::
 :widths: 15 20 65
 :header-rows: 1

 * - Versión
   - Fecha
   - Cambios
 * - 1.1.0
   - 2026-05-07
   - Formaliza el prefijo ``diagrama-de-`` obligatorio para
     todos los archivos UML en ``diagramas-uml/`` (seccion 7
     nueva). Alinea STD-012 con la convencion ya usada en
     STD-011 y con la practica adoptada organicamente en los
     UCs nuevos desde 2026-05-04. Razon: eliminar ambiguedad
     entre archivos textuales y archivos de diagrama, y
     resolver la inconsistencia normativa STD-011/STD-012
     detectada en WP
     ``2026-05-07-04-08-13-use-case-view-analysis`` (G-CU-06).
     Producto del WP
     ``2026-05-07-04-50-49-std-012-prefix-normalization``.
     Actualiza tabla maestra (§3.1) con nombres canonicos.
     **Nota operativa:** el cambio normativo se aplica en commit
     dedicado (este); las operaciones de archivo (renames +
     deletes) se aplican en commits posteriores por UC.
 * - 1.0.0
   - 2026-05-05
   - Versión inicial. Establece distinción clase vs. objeto y
     ubicación canónica de cada tipo de diagrama UML en el
     proyecto. Producto del WP
     ``2026-05-05-06-41-02-arq-tecnica-uml-deepening``
     ante necesidad de aclarar el alcance del domain-model.
