.. meta::
   :artefacto: FND_03
   :tipo: Fundamento Conceptual
   :dominio: base_cognitiva
   :subdominio: _fundamentos_conceptuales
   :estado: Aprobado
   :version: 1.1.0
   :fecha_creacion: 2025-12-19
   :ultimo_cambio: 2025-12-21
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

Existen **cuatro tecnicas complementarias** para identificar Casos de Uso.

.. important::

   **GAP Fundamental BR vs Sistema Completo:**

   Las Business Rules solo generan aproximadamente el **22%** de los UC totales.
   El **78% restante** debe identificarse mediante tecnicas complementarias.

   Sin estas tecnicas adicionales, el sistema quedaria **78% incompleto**.

5.1 Tecnica 1: Derivacion desde Business Rules (22%)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Las Business Rules de tipo **Desencadenador (Trigger)** generan UC directamente.

.. code-block:: text

   BR (Trigger): "SI quimico vence en 30 dias,
                  ENTONCES notificar al responsable"
       |
       v
   UC-007: Notificar Vencimiento Proximo

   PORCENTAJE: 22% de los UC totales
   OUTPUT TIPICO: 10 UC en proyecto mediano

   NATURALEZA: Deductiva (BR explicita -> UC)

5.2 Tecnica 2: Analisis CRUD (40%)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Para cada entidad del dominio, considerar operaciones basicas segun su clasificacion.

**Clasificacion de Entidades:**

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Tipo Entidad
     - UC Generados
     - Ejemplo
   * - **Maestro**
     - CRUD completo (6 UC)
     - Usuario, Producto, Centro
   * - **Transaccional**
     - C + R solamente (3 UC)
     - Llamada, Auditoria, Sesion
   * - **Tecnica**
     - Sin UC directos
     - ConfiguracionSistema, Log

.. code-block:: text

   ENTIDAD MAESTRA: Usuario
       |
       +---> UC-006: Crear Usuario (Create)
       +---> UC-009: Listar Usuarios (Read - lista)
       +---> UC-xxx: Ver Detalle Usuario (Read - detalle)
       +---> UC-007: Modificar Usuario (Update)
       +---> UC-008: Eliminar Usuario (Delete logico)
       +---> UC-xxx: Buscar Usuario (Search)

   ENTIDAD TRANSACCIONAL: Llamada
       |
       +---> (sin Create - viene de IVR)
       +---> UC-017: Consultar Llamadas (Read)
       +---> UC-xxx: Ver Detalle Llamada (Read)
       +---> (sin Update/Delete - inmutable)

   PORCENTAJE: 40% de los UC totales
   OUTPUT TIPICO: 15-20 UC en proyecto mediano

5.3 Tecnica 3: Modelo de Larman - Eventos del Sistema (22%)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Identificar eventos externos que requieren respuesta del sistema.

**Definicion de Evento del Sistema (Larman):**

Un evento del sistema es una ocurrencia externa, detectable por el sistema,
que requiere una respuesta.

**4 Caracteristicas Obligatorias de un Evento Valido:**

.. code-block:: text

   1. EXTERNO:      Originado fuera del sistema (no interno)
   2. DETECTABLE:   Sistema puede "sentir" que ocurrio
   3. SIGNIFICATIVO: Tiene relevancia en el dominio de negocio
   4. ATOMICO:      Ocurrencia puntual e indivisible en el tiempo

**Ejemplos:**

.. code-block:: text

   EVENTO VALIDO: "Usuario solicita reporte"
     ✓ Externo (usuario lo inicia)
     ✓ Detectable (request HTTP)
     ✓ Significativo (operacion de negocio)
     ✓ Atomico (momento especifico)
     --> Genera UC-017: Consultar Reporte

   NO ES EVENTO: "Usuario navega por el sistema"
     ✗ No es atomico (actividad continua)
     ✗ No requiere respuesta especifica
     --> NO genera UC

   PORCENTAJE: 22% de los UC totales
   OUTPUT TIPICO: 10-15 UC en proyecto mediano

**Sub-tecnicas del Modelo de Larman:**

.. code-block:: text

   2.1 Eventos del Sistema
       Identificar cada interaccion significativa actor-sistema

   2.2 Operaciones del Sistema
       Para cada evento, definir la operacion que el sistema ejecuta

   2.3 Responsabilidades del Sistema
       Determinar que debe hacer el sistema en respuesta

5.4 Tecnica 4: Analisis de Interfaz UI-Driven (11%)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Identificar UC a partir de mockups, wireframes o necesidades de UI.

.. code-block:: text

   APLICA A:
   - Dashboards y visualizaciones complejas
   - Busquedas avanzadas con multiples filtros
   - Acciones en lote (batch operations)
   - Wizards multi-paso
   - Configuraciones de usuario

   EJEMPLO:

   Mockup: "Dashboard con 5 widgets configurables"
       |
       +---> UC-025: Ver Dashboard Principal
       +---> UC-030: Personalizar Dashboard
       +---> UC-xxx: Configurar Widget
       +---> UC-xxx: Reordenar Widgets

   PORCENTAJE: 11% de los UC totales
   OUTPUT TIPICO: 5-10 UC en proyecto mediano

5.5 Tecnica 5: Requerimientos Directos de Stakeholders (5%)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

UC que provienen de necesidades explicitas no capturadas como BR.

.. code-block:: text

   APLICA A:
   - Requisitos de compliance y auditoria
   - Integraciones con sistemas externos
   - Reporteria especifica de BI
   - Administracion tecnica del sistema

   EJEMPLO:

   Stakeholder Legal: "Necesitamos exportar auditoria para regulador"
       |
       +---> UC-xxx: Exportar Log Auditoria para Compliance

   Stakeholder TI: "Necesitamos monitorear estado del ETL"
       |
       +---> UC-xxx: Monitorear Estado ETL

   PORCENTAJE: 5% de los UC totales
   OUTPUT TIPICO: 2-5 UC en proyecto mediano

5.6 Matriz de Cobertura Completa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   COBERTURA TOTAL:

   +----------------------------------+------------+--------------+
   | Tecnica                          | Porcentaje | UC Tipicos   |
   +----------------------------------+------------+--------------+
   | 1. Business Rules (Deductiva)    |    22%     | 10 UC        |
   +----------------------------------+------------+--------------+
   | 2. CRUD (Inductiva)              |    40%     | 18 UC        |
   | 3. Larman/Eventos (Inductiva)    |    22%     | 10 UC        |
   | 4. UI-Driven (Inductiva)         |    11%     |  5 UC        |
   | 5. Stakeholders (Inductiva)      |     5%     |  2 UC        |
   +----------------------------------+------------+--------------+
   | TOTAL                            |   100%     | 45 UC        |
   +----------------------------------+------------+--------------+

   NATURALEZA:
   - Tecnica 1: DEDUCTIVA (BR explicita -> UC)
   - Tecnicas 2-5: INDUCTIVAS (necesidades implicitas -> UC)

   IMPLICACION CRITICA:
   Si solo se usa Tecnica 1, el sistema queda 78% incompleto.
   Las 4 tecnicas complementarias son OBLIGATORIAS.

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
   * - 1.1.0
     - 2025-12-21
     - Equipo IACT
     - Corregidos porcentajes de tecnicas UC (22/40/22/11/5). Agregadas tecnicas 4 (UI-Driven) y 5 (Stakeholders). Documentado GAP 22%/78%. Agregada clasificacion de entidades (Maestro/Transaccional/Tecnica). Agregadas 4 caracteristicas obligatorias de eventos.
   * - 1.0.0
     - 2025-12-19
     - Equipo IACT
     - Version inicial aprobada

----

**Trazabilidad:** Este artefacto define el concepto de UC que es el nivel
intermedio entre BR y FR en la jerarquia de requisitos. Referenciado por
FND_05, FND_06, FND_07 y todos los artefactos en requisitos/casos_uso/.