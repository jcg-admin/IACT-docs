.. meta::
   :artefacto: SBVR_02
   :tipo: Ontologia
   :dominio: base_cognitiva
   :subdominio: _ontologia_sbvr
   :estado: Aprobado
   :version: 1.0.0
   :fecha_creacion: 2025-12-18
   :ultimo_cambio: 2025-12-18
   :autor: Business Analyst Lead
   :clasificacion: Interno

.. _sbvr_02_tipos_regla_negocio:

==========================================================
SBVR_02 · Tipos de Regla de Negocio
==========================================================

.. contents:: Contenido
   :local:
   :depth: 2

------------------------------------------------------------
1. Propósito
------------------------------------------------------------

Este documento establece la clasificación formal de reglas de negocio según
el estándar SBVR (Semantics of Business Vocabulary and Business Rules),
proporcionando la base teórica para escribir correctamente los artefactos
BR_xxx en el dominio requisitos/reglas_negocio/.

------------------------------------------------------------
2. Fundamento SBVR
------------------------------------------------------------

2.1. Qué es una Regla de Negocio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Una regla de negocio es una declaración que define o restringe algún aspecto
del negocio. Según SBVR, las reglas de negocio:

- Se expresan en lenguaje natural estructurado
- Son atómicas (una regla, una restricción)
- Son declarativas (qué, no cómo)
- Son independientes de implementación técnica

2.2. Modalidad en SBVR
^^^^^^^^^^^^^^^^^^^^^^

SBVR utiliza lógica modal para clasificar reglas según su naturaleza:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Modalidad
     - Significado
     - Ejemplo
   * - Necesidad
     - Lo que debe ser verdadero siempre
     - "Un Cliente tiene exactamente un identificador único"
   * - Posibilidad
     - Lo que puede ser verdadero
     - "Un Usuario puede tener múltiples roles"
   * - Obligación
     - Lo que debe hacerse
     - "El Sistema debe registrar toda acción de usuario"
   * - Permiso
     - Lo que está permitido hacer
     - "Un Analista puede exportar reportes"

------------------------------------------------------------
3. Clasificación de Reglas
------------------------------------------------------------

3.1. Reglas Estructurales (Aléticas)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Las reglas aléticas definen la estructura del dominio. Expresan verdades
necesarias sobre los conceptos y sus relaciones.

**Características:**

- Definen qué ES algo (no qué debe hacerse)
- No pueden violarse (si se violan, el modelo es incorrecto)
- Usan verbos como: es, tiene, pertenece, contiene

**Subtipos:**

.. list-table::
   :widths: 25 35 40
   :header-rows: 1

   * - Subtipo
     - Descripción
     - Ejemplo IACT
   * - Definición
     - Establece significado de un concepto
     - "Una Llamada es una interacción telefónica iniciada por un Cliente"
   * - Cardinalidad
     - Define multiplicidad de relaciones
     - "Cada Usuario pertenece a exactamente un Segmento de Datos"
   * - Clasificación
     - Establece taxonomías
     - "Un Evento IVR es de tipo: Entrada, Navegación, Transferencia o Abandono"
   * - Derivación
     - Define cómo se calcula un valor
     - "La Duración de una Llamada es la diferencia entre hora_fin y hora_inicio"

**Palabras clave aléticas:**

::

   es, son, tiene, tienen, pertenece, contiene
   cada, todo, ningún, exactamente, al menos, como máximo
   se define como, se calcula como, se deriva de

3.2. Reglas Operativas (Deónticas)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Las reglas deónticas definen obligaciones, prohibiciones y permisos.
Expresan lo que los actores deben, pueden o no pueden hacer.

**Características:**

- Definen comportamiento esperado
- Pueden violarse (generan errores o excepciones)
- Usan verbos modales: debe, puede, no puede, está prohibido

**Subtipos:**

.. list-table::
   :widths: 25 35 40
   :header-rows: 1

   * - Subtipo
     - Descripción
     - Ejemplo IACT
   * - Obligación
     - Acción requerida
     - "El Sistema debe autenticar al Usuario antes de permitir acceso"
   * - Prohibición
     - Acción no permitida
     - "Un Usuario no puede acceder a datos fuera de su Segmento"
   * - Permiso
     - Acción permitida
     - "Un Usuario con rol REPORTS_EXPORTER puede exportar reportes a CSV"
   * - Restricción
     - Límite sobre valores o acciones
     - "Las exportaciones diarias no deben exceder el límite del Perfil"

**Palabras clave deónticas:**

::

   debe, deben, no debe, no deben
   puede, pueden, no puede, no pueden
   está obligado a, está prohibido
   solo si, únicamente cuando, siempre que
   requiere, necesita, exige

------------------------------------------------------------
4. Niveles de Enforcement
------------------------------------------------------------

Las reglas de negocio se implementan con diferentes niveles de enforcement
según su criticidad:

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Nivel
     - Descripción
     - Comportamiento
     - Ejemplo
   * - Estricto
     - Violación imposible
     - Sistema previene la acción
     - Constraint de BD, validación bloqueante
   * - Rechazable
     - Violación rechazada
     - Sistema rechaza con error
     - Validación de API, regla de formulario
   * - Advertencia
     - Violación advertida
     - Sistema advierte pero permite
     - Confirmación de usuario requerida
   * - Auditable
     - Violación registrada
     - Sistema permite pero registra
     - Log de auditoría, alerta posterior

------------------------------------------------------------
5. Formato de Especificación
------------------------------------------------------------

5.1. Plantilla para Reglas de Negocio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cada regla BR_xxx debe documentarse con la siguiente estructura:

::

   BR_NNN: [Nombre descriptivo]

   Tipo: [Alética | Deóntica]
   Subtipo: [Definición | Cardinalidad | Obligación | Prohibición | ...]

   Declaración:
   [Enunciado de la regla en lenguaje natural estructurado]

   Términos:
   - término1: referencia a SBVR_01
   - término2: referencia a SBVR_01

   Enforcement: [Estricto | Rechazable | Advertencia | Auditable]

   Origen: [Stakeholder, documento o decisión que origina la regla]

   Trazabilidad:
   - Deriva en: UC_xxx, UC_yyy
   - Relacionada con: BR_mmm

5.2. Ejemplos de Especificación
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Ejemplo 1: Regla Alética de Cardinalidad**

::

   BR_001: Usuario pertenece a un Segmento

   Tipo: Alética
   Subtipo: Cardinalidad

   Declaración:
   Cada Usuario pertenece a exactamente un Segmento de Datos.

   Términos:
   - Usuario: ver SBVR_01 sección 3.1
   - Segmento de Datos: ver SBVR_01 sección 4.3

   Enforcement: Estricto

   Origen: Modelo RBAC v0.0.1, sección Arquitectura de Seguridad

   Trazabilidad:
   - Deriva en: UC_006 (Crear Usuario)
   - Relacionada con: BR_002

**Ejemplo 2: Regla Deóntica de Obligación**

::

   BR_015: Sistema registra acciones de usuario

   Tipo: Deóntica
   Subtipo: Obligación

   Declaración:
   El Sistema debe registrar toda acción realizada por un Usuario
   en el log de auditoría, incluyendo timestamp, usuario, acción y resultado.

   Términos:
   - Sistema: ver SBVR_01 sección 5.1
   - Usuario: ver SBVR_01 sección 3.1
   - Sesión: ver SBVR_01 sección 8.1

   Enforcement: Estricto

   Origen: Requisito de auditoría, Modelo RBAC sección Capas de Seguridad

   Trazabilidad:
   - Deriva en: UC_045 (Consultar Log de Auditoría)
   - Relacionada con: BR_016, BR_017

**Ejemplo 3: Regla Deóntica de Prohibición**

::

   BR_022: Restricción de acceso por Segmento

   Tipo: Deóntica
   Subtipo: Prohibición

   Declaración:
   Un Usuario no puede acceder a datos de un Segmento de Datos
   diferente al asignado, excepto si tiene rol con permiso cross-segment.

   Términos:
   - Usuario: ver SBVR_01 sección 3.1
   - Segmento de Datos: ver SBVR_01 sección 4.3
   - Rol Funcional: ver SBVR_01 sección 4.1

   Enforcement: Estricto

   Origen: Modelo RBAC, sección Segregación de Datos

   Trazabilidad:
   - Deriva en: UC_017 (Consultar Reporte)
   - Relacionada con: BR_001, BR_023

------------------------------------------------------------
6. Relación con Casos de Uso
------------------------------------------------------------

Las reglas de negocio se relacionan con casos de uso de la siguiente manera:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Relación
     - Descripción
   * - BR deriva UC
     - La regla genera necesidad de un caso de uso para cumplirla
   * - UC implementa BR
     - El caso de uso es el mecanismo para ejecutar la regla
   * - BR restringe UC
     - La regla limita cómo puede ejecutarse el caso de uso
   * - BR es precondición de UC
     - La regla debe cumplirse antes de ejecutar el caso de uso

**Flujo de derivación:**

::

   Regla de Negocio (BR)
          │
          ▼
   Caso de Uso (UC)
          │
          ▼
   Requisito Funcional (FR)

------------------------------------------------------------
7. Validación de Reglas
------------------------------------------------------------

7.1. Checklist de Calidad
^^^^^^^^^^^^^^^^^^^^^^^^^

Antes de aprobar una regla de negocio, verificar:

- La regla es atómica (una sola restricción)
- La regla es declarativa (no describe procedimiento)
- Los términos están definidos en SBVR_01 o SBVR_03
- El tipo y subtipo están correctamente clasificados
- El nivel de enforcement es apropiado
- La trazabilidad está documentada

7.2. Antipatrones a Evitar
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Antipatrón
     - Ejemplo Incorrecto
   * - Regla procedural
     - "Primero validar usuario, luego verificar permisos, luego..."
   * - Regla compuesta
     - "El usuario debe autenticarse Y tener rol activo Y pertenecer a segmento"
   * - Término ambiguo
     - "El administrador puede gestionar usuarios" (¿qué administrador?)
   * - Implementación expuesta
     - "El campo user_id debe ser NOT NULL en la tabla users"

------------------------------------------------------------
8. Referencias
------------------------------------------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Documento
     - Referencia
   * - Conceptos Nucleares
     - :doc:`SBVR_01_Conceptos_Nucleares`
   * - Vocabulario Controlado
     - :doc:`SBVR_03_Vocabulario_Controlado`
   * - Modelo RBAC
     - Modelo_RBAC_Completo_Sistema_IACT_v_0_0_1
   * - Especificación SBVR
     - SBVR 1.5 (OMG, 2019)
   * - Fundamentos de Reglas
     - :doc:`/base_cognitiva/fundamentos_conceptuales/FND_02_Reglas_de_Negocio`

------------------------------------------------------------
Historial de Cambios
------------------------------------------------------------

.. list-table::
   :widths: 15 15 20 50
   :header-rows: 1

   * - Versión
     - Fecha
     - Autor
     - Cambios
   * - 1.0.0
     - 2025-12-18
     - BA Lead
     - Versión inicial con clasificación SBVR de reglas

----

**Trazabilidad:** Base teórica para escribir BR correctamente. Define
estructura y clasificación usada en requisitos/reglas_negocio/.