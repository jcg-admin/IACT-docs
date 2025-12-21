.. meta::
   :artefacto: FND_03
   :tipo: Fundamento Conceptual
   :dominio: base_cognitiva
   :subdominio: _fundamentos_conceptuales
   :estado: Aprobado
   :version: 1.0.0
   :fecha_creacion: 2025-12-19
   :ultimo_cambio: 2025-12-19
   :autor: Equipo IACT
   :clasificacion: Interno

.. _fnd-03:

==============================================================================
FND_03: Casos de Uso
==============================================================================

.. contents:: Contenido
   :local:
   :depth: 2

----

Proposito
---------

Este documento define QUE ES un Caso de Uso (Use Case) en el contexto del
proyecto IACT, su estructura, componentes y relacion con otros artefactos
de requisitos.

----

1. Definicion Formal
--------------------

1.1 Que es un Caso de Uso
^^^^^^^^^^^^^^^^^^^^^^^^^

Un **Caso de Uso (Use Case - UC)** es una descripcion de una secuencia de
interacciones entre un actor y el sistema para lograr un objetivo especifico.
Describe comportamientos del sistema desde la perspectiva del usuario.

.. note::

   **Definicion operativa para IACT:**

   Un UC es una narrativa que describe COMO un usuario interactua con el
   sistema para completar una tarea de negocio, incluyendo el flujo normal
   y los flujos alternativos.

1.2 Caracteristicas de un Caso de Uso
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Caracteristica
     - Descripcion
   * - **Narrativo**
     - Cuenta una historia: "El usuario hace X, sistema responde Y"
   * - **Alto nivel**
     - Describe interaccion completa, no detalles atomicos
   * - **Orientado a actor**
     - Perspectiva del usuario, no del sistema
   * - **Secuencial**
     - Pasos ordenados en flujo temporal
   * - **Contextualizado**
     - Incluye precondiciones y postcondiciones
   * - **Multi-camino**
     - Flujo normal mas flujos alternativos

1.3 UC vs FR: Diferencia Fundamental
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspecto
     - Caso de Uso (UC)
     - Requisito Funcional (FR)
   * - Vista
     - Narrativa (historia)
     - Atomica (declaracion)
   * - Nivel
     - Alto (interaccion completa)
     - Bajo (comportamiento especifico)
   * - Orientacion
     - Actor (usuario)
     - Sistema (implementacion)
   * - Dependencia
     - Secuencia importa
     - Independiente
   * - Verificacion
     - Escenario end-to-end
     - Test unitario/aislado
   * - Ejemplo
     - "UC-40: Registrar Producto"
     - "FR-40.6: Validar formato CAS"

**Analogia:**

.. code-block:: text

   CASO DE USO = PLANO ARQUITECTONICO
     - Muestra habitaciones, distribucion, flujo
     - Alto nivel, comprensible por cliente
     - No especifica tamaño de cada ladrillo

   REQUISITO FUNCIONAL = ESPECIFICACION DE CONSTRUCCION
     - Ladrillo debe ser de 10cm x 20cm
     - Bajo nivel, comprensible por constructor
     - Cada especificacion es verificable

   AMBOS SE NECESITAN:
     - Plano sin especificaciones: Constructor adivina
     - Especificaciones sin plano: No sabe como ensamblar

----

2. Estructura de un Caso de Uso
-------------------------------

2.1 Componentes Obligatorios
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   UC-NNN: [Nombre del Caso de Uso]

   IDENTIFICACION:
     ID:              UC-NNN
     Nombre:          [Verbo + Objeto]
     Actor Primario:  [Rol que inicia]
     Actores Secundarios: [Otros roles involucrados]

   CONTEXTO:
     Objetivo:        [Meta del actor]
     Precondiciones:  [Que debe ser verdad ANTES]
     Postcondiciones: [Que sera verdad DESPUES - exito]
     Trigger:         [Evento que inicia el UC]

   FLUJOS:
     Flujo Normal:    [Pasos 1, 2, 3... secuencia exitosa]
     Flujos Alternos: [Variaciones del flujo normal]
     Excepciones:     [Errores y como manejarlos]

   TRAZABILIDAD:
     Business Rules:  [BR que aplican]
     FR Derivados:    [FR que se generan de este UC]

2.2 Ejemplo Completo
^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   UC-010: Asignar Rol a Usuario

   IDENTIFICACION:
     ID:              UC-010
     Nombre:          Asignar Rol a Usuario
     Actor Primario:  Administrador de Usuarios (R001)
     Actores Secundarios: Ninguno

   CONTEXTO:
     Objetivo:        Otorgar permisos a un usuario mediante asignacion de rol
     Precondiciones:
       - Administrador autenticado con rol R001
       - Usuario destino existe y esta activo
       - Rol a asignar existe en el catalogo
     Postcondiciones:
       - Usuario tiene el nuevo rol asignado
       - Permisos del rol estan activos para el usuario
       - Registro de auditoria creado
     Trigger:         Administrador selecciona "Asignar Rol" en gestion usuarios

   FLUJO NORMAL:
     1. Administrador busca usuario por nombre o email
     2. Sistema muestra informacion del usuario y roles actuales
     3. Administrador selecciona "Agregar Rol"
     4. Sistema muestra lista de roles disponibles
     5. Administrador selecciona rol a asignar
     6. Sistema valida compatibilidad SoD (Separacion de Funciones)
     7. Sistema solicita justificacion de la asignacion
     8. Administrador ingresa justificacion
     9. Sistema registra la asignacion con timestamp
    10. Sistema notifica al usuario via buzon interno
    11. Sistema muestra confirmacion de exito

   FLUJO ALTERNO 6a: Conflicto SoD
     6a.1. Sistema detecta conflicto con rol existente
     6a.2. Sistema muestra mensaje: "Rol incompatible con [rol_existente]"
     6a.3. Sistema bloquea asignacion
     6a.4. Retorna a paso 4

   EXCEPCION 1: Usuario no encontrado
     1a.1. Sistema muestra "Usuario no encontrado"
     1a.2. Caso de uso termina

   TRAZABILIDAD:
     Business Rules:  BR_015 (Separacion de Funciones SoD)
     FR Derivados:    FR-010.1 a FR-010.15

----

3. Actores
----------

3.1 Definicion de Actor
^^^^^^^^^^^^^^^^^^^^^^^

Un **actor** es una entidad externa al sistema que interactua con el.
Puede ser una persona (rol), otro sistema, o el tiempo.

3.2 Tipos de Actores
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Tipo
     - Descripcion
     - Ejemplo IACT
   * - Humano
     - Persona con rol especifico
     - DASHBOARD_VIEWER (R008)
   * - Sistema
     - Sistema externo que interactua
     - Sistema IVR MySQL
   * - Tiempo
     - Eventos programados
     - Scheduler ETL (medianoche)

3.3 Actor Primario vs Secundario
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   ACTOR PRIMARIO:
     - Inicia el caso de uso
     - Tiene el objetivo principal
     - Ejemplo: Administrador que asigna rol

   ACTOR SECUNDARIO:
     - Participa pero no inicia
     - Proporciona informacion o recibe notificacion
     - Ejemplo: Usuario que recibe notificacion de nuevo rol

3.4 Actores en IACT
^^^^^^^^^^^^^^^^^^^

Los actores en IACT corresponden a los 18 roles del modelo RBAC:

.. code-block:: text

   CATEGORIA: Gestion de Usuarios
     - R001: USERS_FULL_MANAGER
     - R002: USERS_VIEWER
     - R003: USERS_TEAM_MANAGER

   CATEGORIA: Reportes
     - R004: REPORTS_VIEWER
     - R005: REPORTS_EXPORTER
     - R006: REPORTS_ADVANCED_VIEWER
     - R007: REPORTS_CREATOR

   CATEGORIA: Visualizacion
     - R008: DASHBOARD_VIEWER
     - R009: DASHBOARD_CUSTOMIZER

   CATEGORIA: Analisis
     - R010: DATA_ANALYST

   CATEGORIA: Alertas
     - R011: ALERTS_VIEWER
     - R012: ALERTS_CONFIGURATOR
     - R013: ALERTS_TEAM_MANAGER
     - R014: ALERTS_GLOBAL_ADMIN

   CATEGORIA: Administracion
     - R015: MODULES_ADMIN
     - R016: SYSTEM_ADMIN
     - R017: AUDIT_VIEWER
     - R018: SECURITY_ADMIN

   ACTOR ESPECIAL:
     - TIEMPO: Para procesos batch (ETL nocturno)

----

4. Flujos
---------

4.1 Flujo Normal (Happy Path)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

El flujo normal describe la secuencia de pasos cuando TODO sale bien.

**Caracteristicas:**

- Secuencia exitosa de principio a fin
- Sin errores ni excepciones
- Representa el 80% de las ejecuciones tipicas

**Formato de pasos:**

.. code-block:: text

   N. [Actor|Sistema] [verbo] [objeto] [complemento opcional]

   Ejemplos:
   1. Usuario ingresa credenciales de acceso
   2. Sistema valida formato de email
   3. Sistema verifica credenciales contra base de datos
   4. Sistema genera token JWT
   5. Sistema redirige a dashboard principal

4.2 Flujos Alternos
^^^^^^^^^^^^^^^^^^^

Los flujos alternos son variaciones VALIDAS del flujo normal.

**Caracteristicas:**

- Caminos alternativos pero exitosos
- Decisiones del usuario o condiciones del sistema
- Se reincorporan al flujo normal

**Formato:**

.. code-block:: text

   FLUJO ALTERNO Na: [Nombre descriptivo]
     Na.1. [Condicion que dispara el alterno]
     Na.2. [Paso alternativo]
     Na.3. Retorna a paso N+1 del flujo normal

   Ejemplo:
   FLUJO ALTERNO 3a: Usuario olvido password
     3a.1. Usuario selecciona "Olvide mi password"
     3a.2. Sistema muestra formulario de recuperacion
     3a.3. Usuario ingresa email registrado
     3a.4. Sistema envia pregunta de seguridad (NO email externo)
     3a.5. Retorna a paso 1

4.3 Excepciones
^^^^^^^^^^^^^^^

Las excepciones son situaciones de ERROR que impiden completar el UC.

**Caracteristicas:**

- El objetivo NO se cumple
- Requiere manejo especial
- Puede terminar el UC o permitir reintento

**Formato:**

.. code-block:: text

   EXCEPCION N: [Nombre del error]
     N.1. [Condicion de error]
     N.2. Sistema muestra mensaje de error
     N.3. [Accion: termina UC | permite reintento]

   Ejemplo:
   EXCEPCION 3: Credenciales invalidas
     3.1. Sistema detecta password incorrecto
     3.2. Sistema incrementa contador de intentos fallidos
     3.3. Sistema muestra "Credenciales invalidas"
     3.4. SI intentos >= 5 ENTONCES
            Sistema bloquea cuenta
            Caso de uso termina
          SINO
            Retorna a paso 1

----

5. Tecnicas de Identificacion de UC
-----------------------------------

Existen tres tecnicas complementarias para identificar Casos de Uso:

5.1 Tecnica 1: Derivacion desde Business Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Las Business Rules de tipo **Desencadenador (Trigger)** generan UC directamente.

.. code-block:: text

   BR (Trigger): "SI quimico vence en 30 dias,
                  ENTONCES notificar al responsable"
       |
       v
   UC-007: Notificar Vencimiento Proximo

   Cobertura: ~38% de los UC

5.2 Tecnica 2: Analisis CRUD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Para cada entidad del dominio, considerar operaciones basicas.

.. code-block:: text

   ENTIDAD: Producto
       |
       +---> UC-040: Registrar Nuevo Producto (Create)
       +---> UC-041: Consultar Producto (Read)
       +---> UC-042: Modificar Producto (Update)
       +---> UC-043: Eliminar Producto (Delete)

   Cobertura: ~40% de los UC

5.3 Tecnica 3: Eventos del Sistema (Larman)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Identificar eventos externos que requieren respuesta del sistema.

**Definicion de Evento del Sistema (Larman):**

Un evento del sistema es una ocurrencia externa, detectable por el sistema,
que requiere una respuesta.

**Caracteristicas de un evento valido:**

.. code-block:: text

   1. EXTERNO:     Originado fuera del sistema
   2. DETECTABLE:  Sistema puede "sentir" que ocurrio
   3. SIGNIFICATIVO: Tiene relevancia en el dominio
   4. ATOMICO:     Ocurrencia puntual en el tiempo

**Ejemplos:**

.. code-block:: text

   EVENTO VALIDO: "Usuario solicita reporte"
     - Externo (usuario lo inicia)
     - Detectable (request HTTP)
     - Significativo (operacion de negocio)
     - Atomico (momento especifico)
     --> Genera UC-017: Consultar Reporte

   NO ES EVENTO: "Usuario navega por el sistema"
     - No es atomico (actividad continua)
     - No requiere respuesta especifica
     --> NO genera UC

   Cobertura: ~22% de los UC

5.4 Complementariedad de Tecnicas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   COBERTURA TOTAL:

   +------------------+------------+
   | Tecnica          | Cobertura  |
   +------------------+------------+
   | Business Rules   |    38%     |
   | CRUD             |    40%     |
   | Eventos (Larman) |    22%     |
   +------------------+------------+
   | TOTAL            |   100%     |
   +------------------+------------+

   Las tres tecnicas son NECESARIAS para cobertura completa

----

6. Contratos de Operacion
-------------------------

6.1 Definicion
^^^^^^^^^^^^^^

Un **contrato de operacion** describe QUE debe lograr una operacion del
sistema, sin especificar COMO lo hace. Define precondiciones y postcondiciones.

6.2 Formato
^^^^^^^^^^^

.. code-block:: text

   Operacion: nombreOperacion(parametros)

   Precondiciones:
     - [Condicion que DEBE ser verdad ANTES]
     - [Otra condicion requerida]

   Postcondiciones:
     - [Estado que SERA verdad DESPUES]
     - [Cambio realizado en el sistema]

6.3 Ejemplo
^^^^^^^^^^^

.. code-block:: text

   Operacion: asignarRol(userId, roleId, justificacion)

   Precondiciones:
     - Usuario con userId existe en sistema
     - Usuario esta en estado ACTIVO
     - Rol con roleId existe en catalogo
     - Rol no tiene conflicto SoD con roles actuales del usuario
     - Actor tiene permiso roles.assign

   Postcondiciones:
     - Registro user_roles creado (userId, roleId)
     - Timestamp de asignacion registrado
     - Justificacion almacenada
     - Notificacion enviada a usuario via buzon interno
     - Registro de auditoria creado

6.4 Relacion UC - Contrato
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Caso de Uso: Define COMO interactua usuario con sistema
   Contrato:    Define QUE debe pasar tecnicamente

   UC es mas NARRATIVO (flujo de trabajo)
   Contrato es mas TECNICO (cambios de estado)

   Ambos se complementan:
     - Contrato asegura completitud tecnica
     - UC asegura usabilidad y flujo de trabajo

----

7. Casos de Uso en el Contexto IACT
-----------------------------------

7.1 Nomenclatura
^^^^^^^^^^^^^^^^

Los Casos de Uso en IACT siguen la convencion:

.. code-block:: text

   FORMATO: UC_NNN_Nombre_Descriptivo.rst

   Donde:
   - UC: Prefijo fijo (Use Case)
   - NNN: Numero secuencial de 3 digitos
   - Nombre_Descriptivo: Verbo + Objeto con guiones bajos

   Ejemplos:
   - UC_006_Crear_Usuario.rst
   - UC_010_Asignar_Roles.rst
   - UC_017_Consultar_Reporte.rst

7.2 Ubicacion en el Modelo IACT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   requisitos/
       |
       +--- casos_uso/
                |
                +--- index.rst
                +--- UC_001_xxx.rst
                +--- UC_002_xxx.rst
                +--- ...

7.3 Relacion con Otros Artefactos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   BR (Regla de Negocio)
       |
       v
   UC (Caso de Uso) <---- Desencadenadores generan UC
       |                  Restricciones son precondiciones
       v
   FR (Requisito Funcional) <---- Cada paso UC deriva FR

----

8. Lista de UC Identificados en IACT
------------------------------------

Basado en el analisis del modelo RBAC, se han identificado 38 Casos de Uso:

8.1 Gestion de Usuarios (7 UC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   UC-005: Gestion de Sesiones Seguras
   UC-006: Crear Usuario
   UC-007: Modificar Usuario
   UC-008: Eliminar Usuario (baja logica)
   UC-009: Listar Usuarios
   UC-010: Asignar Roles
   UC-011: Gestionar Permisos por Rol

8.2 Reportes (8 UC)
^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   UC-017: Consultar Reporte Trimestral
   UC-018: Consultar Problemas de Menu
   UC-019: Consultar Transferencias por Centro
   UC-020: Filtrar Reportes por Fecha
   UC-021: Filtrar Reportes por Centro
   UC-022: Exportar CSV
   UC-023: Exportar Excel
   UC-024: Exportar PDF

8.3 Dashboards (6 UC)
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   UC-025: Ver Dashboard Principal
   UC-026: Ver Graficos de Llamadas por Hora
   UC-027: Ver Graficos de Llamadas por Dia
   UC-028: Ver Distribucion de Llamadas por Centro
   UC-029: Ver Tendencias Temporales
   UC-030: Personalizar Dashboard

8.4 Analisis (5 UC)
^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   UC-031: Analisis Exploratorio de Datos
   UC-032: Comparar Periodos
   UC-033: Identificar Patrones de Llamadas
   UC-034: Analisis de Inconsistencias de Navegacion
   UC-035: Analisis de Tiempos de Espera

8.5 Alertas (5 UC)
^^^^^^^^^^^^^^^^^^

.. code-block:: text

   UC-036: Configurar Alerta por Umbral
   UC-037: Recibir Notificacion de Alerta
   UC-038: Ver Historial de Alertas
   UC-039: Desactivar Alerta
   UC-040: Configurar Destinatarios

8.6 Administracion (7 UC)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   UC-012: Asignar Modulos a Usuario
   UC-013: Crear Perfil de Modulos
   UC-014: Asignar Perfil a Usuario
   UC-015: Ver Modulos Disponibles
   UC-016: Configurar Permisos de Modulo
   UC-041: Gestionar Segmentos de Datos
   UC-042: Gestionar Permisos Directos

----

9. Referencias
--------------

Documentos Relacionados
^^^^^^^^^^^^^^^^^^^^^^^

- :ref:`fnd-01` - Concepto de Requisito
- :ref:`fnd-02` - Reglas de Negocio
- :ref:`fnd-05` - Jerarquia de 4 Niveles
- :ref:`fnd-07` - Requerimientos Funcionales

Fuentes Externas
^^^^^^^^^^^^^^^^

- Craig Larman: "Applying UML and Patterns" (3rd Edition)
- Alistair Cockburn: "Writing Effective Use Cases"
- Ivar Jacobson: "Object-Oriented Software Engineering"

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

**Trazabilidad:** Este artefacto define el concepto de UC que es el nivel
intermedio entre BR y FR en la jerarquia de requisitos. Referenciado por
FND_05, FND_06, FND_07 y todos los artefactos en requisitos/casos_uso/.