.. meta::
   :artefacto: FND_05
   :tipo: Fundamento Conceptual
   :dominio: base_cognitiva
   :subdominio: _fundamentos_conceptuales
   :estado: Aprobado
   :version: 1.0.0
   :fecha_creacion: 2025-12-19
   :ultimo_cambio: 2025-12-19
   :autor: Equipo IACT
   :clasificacion: Interno

.. _fnd-05:

==============================================================================
FND_05: Jerarquia de 4 Niveles
==============================================================================

.. contents:: Contenido
   :local:
   :depth: 2

----

Proposito
---------

Este documento describe la **jerarquia de abstraccion de requisitos** que
fundamenta el modelo IACT. Explica los 4 niveles desde Business Rules hasta
Functional Requirements y como se relacionan entre si.

----

1. Vision General
-----------------

1.1 Principio Fundamental
^^^^^^^^^^^^^^^^^^^^^^^^^

Los requisitos NO son planos. Existen en **niveles de abstraccion** que van
desde lo mas general y estable (reglas de negocio) hasta lo mas especifico
y cambiante (requisitos funcionales).

.. code-block:: text

   MAS ABSTRACTO                              MAS CONCRETO
   MAS ESTABLE                                MAS CAMBIANTE
   MAYOR ALCANCE                              MENOR ALCANCE
        |                                           |
        v                                           v

   +------------+    +------------+    +--------+    +--------+
   | Nivel 0    | -> | Nivel 1    | -> | Nivel 2| -> | Nivel 3|
   | BR         |    | BReq       |    | UC     |    | FR     |
   | (Reglas)   |    | (Objetivos)|    | (Casos)|    | (Func.)|
   +------------+    +------------+    +--------+    +--------+

1.2 Preguntas por Nivel
^^^^^^^^^^^^^^^^^^^^^^^

Cada nivel responde una pregunta diferente:

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Nivel
     - Pregunta
     - Descripcion
   * - Nivel 0 (BR)
     - POR QUE esta restriccion?
     - Origen de las politicas y regulaciones
   * - Nivel 1 (BReq)
     - POR QUE este proyecto?
     - Justificacion y objetivos del proyecto
   * - Nivel 2 (UC)
     - QUE hace el usuario?
     - Comportamientos observables del sistema
   * - Nivel 3 (FR)
     - COMO lo hace el sistema?
     - Especificaciones atomicas implementables

----

2. Nivel 0: Business Rules (BR)
-------------------------------

2.1 Definicion
^^^^^^^^^^^^^^

Las **Business Rules** son declaraciones sobre como opera la organizacion.
No son creadas por el proyecto de software; existen independientemente y
el software debe conformarse a ellas.

2.2 Caracteristicas
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Caracteristica
     - Descripcion
   * - **Externas**
     - Provienen de fuera del sistema (politicas, regulaciones)
   * - **Obligatorias**
     - No son opcionales ni negociables
   * - **Estables**
     - Cambian menos frecuentemente que otros requisitos
   * - **Influyentes**
     - Afectan multiples partes del sistema

2.3 Fuentes
^^^^^^^^^^^

.. code-block:: text

   FUENTES EXTERNAS (Obligatorias):
   +------------------+
   | Leyes            |
   | Regulaciones     |
   | Estandares       |
   | Contratos        |
   +------------------+
           |
           v
   +------------------+
   |     SISTEMA      |  <-- El sistema CUMPLE las reglas
   +------------------+      El sistema NO CREA las reglas
           ^
           |
   +------------------+
   | Politicas        |
   | Procedimientos   |
   | Mejores Practicas|
   +------------------+
   FUENTES INTERNAS (Organizacionales)

2.4 Ejemplo
^^^^^^^^^^^

.. code-block:: text

   BR-028:
     Definicion: "Solicitudes de compra que excedan $500 requieren
                  aprobacion del gerente de departamento"
     Tipo:       Restriccion (Constraint)
     Fuente:     Politica Financiera Corporativa v2.3, Seccion 4.2
     Razon:      Control de gastos y cumplimiento de auditoria
     Estatica:   No (puede cambiar por decision del CFO)

----

3. Nivel 1: Business Requirements (BReq)
----------------------------------------

3.1 Definicion
^^^^^^^^^^^^^^

Los **Business Requirements** expresan los objetivos de alto nivel que
justifican la existencia del proyecto. Responden: "Por que estamos
construyendo este sistema?"

3.2 Caracteristicas
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Caracteristica
     - Descripcion
   * - **Estrategicos**
     - Vision de negocio, no tecnica
   * - **Justificativos**
     - Explican el ROI del proyecto
   * - **Influenciados**
     - Por BR, pero no son reiteracion de ellas
   * - **Alcance**
     - Definen limites del proyecto

3.3 Relacion con BR
^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Business Rules INFLUYEN en Business Requirements:

   BR-087 (OSHA 1910.1200)  ----+
   BR-088 (EPA 40 CFR)      ----+---> BReq: "El sistema debe permitir
   BR-089 (State Safety)    ----+      cumplimiento de regulaciones
                                       de quimicos peligrosos"

3.4 Ejemplo
^^^^^^^^^^^

.. code-block:: text

   Business Requirement (IACT):

   "El Sistema IACT Dashboard Analytics debe proporcionar
    visibilidad en tiempo real de las metricas de llamadas
    del IVR, permitiendo a los supervisores identificar
    problemas operacionales y tomar decisiones informadas,
    reduciendo el tiempo de resolucion de incidentes en 40%."

   Influenciado por:
     - BR_001: Fuente operacional inmutable
     - BR_002: Sincronizacion ETL nocturna
     - Objetivo de negocio: Mejora operacional

----

4. Nivel 2: User Requirements / Use Cases (UC)
----------------------------------------------

4.1 Definicion
^^^^^^^^^^^^^^

Los **User Requirements** describen comportamientos del sistema desde la
perspectiva del usuario. Se expresan tipicamente como **Casos de Uso** que
especifican interacciones completas entre actores y sistema.

4.2 Caracteristicas
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Caracteristica
     - Descripcion
   * - **Narrativos**
     - Cuentan una historia de interaccion
   * - **Observables**
     - Describen lo que el usuario VE
   * - **Completos**
     - Flujo de principio a fin
   * - **Sin implementacion**
     - NO especifican el COMO interno

4.3 Relacion con BR
^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Business Rules determinan flujos en Casos de Uso:

   BR-028: "Compras >$500 requieren aprobacion"
       |
       v
   UC-04: Solicitar Producto
     ...
     Paso 6: SI monto >$500 ENTONCES
               Sistema solicita aprobacion de gerente
     ...

4.4 Ejemplo
^^^^^^^^^^^

.. code-block:: text

   UC-010: Asignar Rol a Usuario

   Actor Primario: Administrador de Usuarios (R001)
   Objetivo:       Otorgar permisos mediante asignacion de rol

   Flujo Normal:
     1. Administrador busca usuario
     2. Sistema muestra usuario y roles actuales
     3. Administrador selecciona "Agregar Rol"
     4. Sistema muestra roles disponibles
     5. Administrador selecciona rol
     6. Sistema valida compatibilidad SoD
     7. Sistema solicita justificacion
     8. Administrador ingresa justificacion
     9. Sistema registra asignacion
    10. Sistema notifica al usuario

   Business Rules aplicadas: BR_015 (SoD)

----

5. Nivel 3: Functional Requirements (FR)
----------------------------------------

5.1 Definicion
^^^^^^^^^^^^^^

Los **Functional Requirements** son especificaciones detalladas y atomicas
de lo que el sistema debe hacer. Se derivan directamente de los pasos de
los Casos de Uso.

5.2 Caracteristicas
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Caracteristica
     - Descripcion
   * - **Atomicos**
     - Una sola funcionalidad por FR
   * - **Verificables**
     - Se puede probar si se cumple o no
   * - **Independientes**
     - No dependen de secuencia para verificarse
   * - **Implementables**
     - Suficientemente especificos para codificar

5.3 Relacion con UC
^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Cada paso de UC deriva multiples FR:

   UC-04, Paso 5: "Sistema valida datos ingresados"
       |
       +---> FR-04.6: Validar formato CAS Number
       +---> FR-04.7: Validar checksum CAS
       +---> FR-04.8: Validar nombre no vacio
       +---> FR-04.9: Validar nombre <= 200 caracteres
       +---> FR-04.10: Validar categoria existe
       +---> FR-04.11: Validar clase peligrosidad 1-5

   1 paso UC -> 6 FR atomicos

5.4 Ejemplo
^^^^^^^^^^^

.. code-block:: text

   Derivados de UC-010, Paso 6:

   FR-10.6: "Sistema DEBE validar que el rol seleccionado
             no tenga conflicto SoD con roles actuales del usuario"

   FR-10.7: "SI existe conflicto SoD, sistema DEBE mostrar mensaje:
             'Rol [X] incompatible con rol existente [Y]'"

   FR-10.8: "SI existe conflicto SoD, sistema DEBE bloquear
             la asignacion y retornar a seleccion de rol"

----

6. Flujo de Influencia
----------------------

6.1 Influencia Multinivel
^^^^^^^^^^^^^^^^^^^^^^^^^

Las Business Rules no solo generan un nivel; influyen en multiples aspectos
del sistema simultaneamente:

.. code-block:: text

   BR-028 (Restriccion de aprobacion)
       |
       +---> Business Requirements (justifica proyecto)
       |
       +---> User Requirements (determina flujos UC)
       |
       +---> Functional Requirements (define logica)
       |
       +---> Quality Attributes (tiempo de respuesta)
       |
       +---> External Interfaces (notificaciones)
       |
       +---> Constraints (sistemas involucrados)

6.2 Diagrama de Relaciones
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   +----------------+
   | Business Rules | .........(influye en todo)..........
   +----------------+                                     :
          |                                               :
          | influye                                       :
          v                                               :
   +--------------------+                                 :
   | Business           |                                 :
   | Requirements       |                                 :
   +--------------------+                                 :
          |                                               :
          | genera                                        :
          v                                               v
   +--------------------+     +------------------+  +-----------+
   | User Requirements  |     | Quality          |  | External  |
   | (Casos de Uso)     |     | Attributes       |  | Interfaces|
   +--------------------+     +------------------+  +-----------+
          |                          |                    |
          | deriva                   |                    |
          v                          v                    v
   +--------------------+     +------------------+  +-----------+
   | Functional         |---->| Software Requirements           |
   | Requirements       |     | Specification (SRS)             |
   +--------------------+     +--------------------------------+

----

7. Resumen Comparativo
----------------------

7.1 Tabla de Niveles
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 12 18 18 18 18 16

   * - Nivel
     - Nombre
     - Pregunta
     - Contenido
     - Artefacto
     - Prefijo
   * - 0
     - Business Rules
     - Por que restriccion?
     - Politicas, regulaciones
     - BR_NNN.rst
     - BR_
   * - 1
     - Business Req.
     - Por que proyecto?
     - Objetivos, alcance
     - BReq_NNN.rst
     - BReq_
   * - 2
     - User Req.
     - Que hace usuario?
     - Casos de Uso
     - UC_NNN.rst
     - UC_
   * - 3
     - Functional Req.
     - Como sistema?
     - Especificaciones
     - FR_NNN.rst
     - FR_

7.2 Gradiente de Abstraccion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   NIVEL 0 (BR)    NIVEL 1 (BReq)   NIVEL 2 (UC)    NIVEL 3 (FR)

   Mas abstracto ---------------------------------> Mas concreto
   Mas estable -----------------------------------> Mas cambiante
   Mayor alcance ---------------------------------> Menor alcance
   Menos cantidad -------------------------------> Mas cantidad

   Ejemplo de cantidad tipica:

   5-20 BR  ->  3-10 BReq  ->  30-100 UC  ->  200-1000 FR

7.3 Responsabilidad por Nivel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Nivel
     - Responsable de Crear
     - Responsable de Aprobar
   * - BR
     - Stakeholders, Legal, Compliance
     - Sponsor, Legal
   * - BReq
     - Product Owner, BA
     - Sponsor, Stakeholders
   * - UC
     - Business Analyst
     - Product Owner, Usuarios
   * - FR
     - Business Analyst, Arquitecto
     - Tech Lead, QA

----

8. Aplicacion en IACT
---------------------

8.1 Ubicacion en Estructura
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   requisitos/
       |
       +--- reglas_negocio/      <- Nivel 0 (BR)
       |       +--- BR_001_xxx.rst
       |       +--- BR_002_xxx.rst
       |
       +--- objetivos/           <- Nivel 1 (BReq)
       |       +--- BReq_001_xxx.rst
       |
       +--- casos_uso/           <- Nivel 2 (UC)
       |       +--- UC_001_xxx.rst
       |       +--- UC_002_xxx.rst
       |
       +--- funcionales/         <- Nivel 3 (FR)
               +--- FR_001_xxx.rst
               +--- FR_002_xxx.rst

8.2 Ejemplos IACT por Nivel
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   NIVEL 0 - BR:
   BR_001: "La BD MySQL operacional es de SOLO LECTURA para IACT"

   NIVEL 1 - BReq:
   BReq_001: "Proporcionar dashboard de metricas de llamadas IVR"

   NIVEL 2 - UC:
   UC_025: "Ver Dashboard Principal"
   UC_017: "Consultar Reporte Trimestral"

   NIVEL 3 - FR:
   FR-025.1: "Sistema DEBE mostrar grafico de llamadas por hora"
   FR-025.2: "Sistema DEBE actualizar datos cada 5 minutos"
   FR-017.1: "Sistema DEBE filtrar por rango de fechas"

----

9. Referencias
--------------

Documentos Relacionados
^^^^^^^^^^^^^^^^^^^^^^^

- :ref:`fnd-01` - Concepto de Requisito
- :ref:`fnd-02` - Reglas de Negocio
- :ref:`fnd-03` - Casos de Uso
- :ref:`fnd-04` - Trazabilidad
- :ref:`fnd-06` - Derivacion vs Transformacion
- :ref:`fnd-07` - Requerimientos Funcionales

Fuentes Externas
^^^^^^^^^^^^^^^^

- Karl Wiegers: "Software Requirements" (3rd Edition)
- IEEE 830-1998: Software Requirements Specifications
- IREB CPRE Foundation Level Syllabus

----

Historial de Cambios
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 20 50

   * - Version
     - Fecha
     - Autor
     - Cambios
   * - 1.0.0
     - 2025-12-19
     - Equipo IACT
     - Version inicial aprobada

----

**Trazabilidad:** Este artefacto define la estructura jerarquica que
organiza todo el dominio requisitos/. Es la base conceptual para entender
las relaciones BR -> UC -> FR documentadas en FND_04 (Trazabilidad).