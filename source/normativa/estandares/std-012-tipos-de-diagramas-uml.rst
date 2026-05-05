.. meta::
 :artefacto: STD_012
 :tipo: Estándar
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
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
   - ``casos-uso/{cluster}/{uc}/diagramas-uml/caso-de-uso.rst``
     +
     ``arquitectura-tecnica/use-case-view/{cluster}/{uc}/caso-de-uso.rst``
   - 1 UC / archivo (spec) + 1 vista módulo
   - Spec del UC: actores + relaciones include/extend.
     Vista arq: módulo entero.
 * - **Secuencia**
   - ``casos-uso/{cluster}/{uc}/diagramas-uml/secuencia*.rst``
   - 1 escenario / archivo
   - Mostrar interacción cronológica entre componentes.
 * - **Actividad**
   - ``casos-uso/{cluster}/{uc}/diagramas-uml/actividad.rst``
   - 1 flujo / archivo
   - Flujo de control con decisiones (if/else) y forks.
 * - **Estados**
   - ``casos-uso/{cluster}/{uc}/diagramas-uml/estados-{entidad}.rst``
   - 1 entidad / archivo
   - Ciclo de vida de una entidad con state machine.
 * - **Componentes**
   - ``arquitectura-tecnica/{view}/*-componentes.rst``
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

7. Referencias
==============

- :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama/diagrama-de-clases`
- :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama/diagrama-de-objetos`
- :doc:`/base-cognitiva/_uml/uml-03-uso-orientacion-objetos/index`
- :doc:`/base-cognitiva/_uml/uml-04-uso-relaciones/index`
- :doc:`/normativa/estandares/std-011-alias-diagramas-uml`

----

8. Historial de Cambios
=======================

.. list-table::
 :widths: 15 20 65
 :header-rows: 1

 * - Versión
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-05-05
   - Versión inicial. Establece distinción clase vs. objeto y
     ubicación canónica de cada tipo de diagrama UML en el
     proyecto. Producto del WP
     ``2026-05-05-06-41-02-arq-tecnica-uml-deepening``
     ante necesidad de aclarar el alcance del domain-model.
