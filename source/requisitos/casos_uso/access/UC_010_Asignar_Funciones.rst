.. meta::
   :artefacto: UC_010
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-010:

==============================================================================
UC-010: Asignar Funciones a Usuario
==============================================================================

.. contents:: Contenido
   :local:
   :depth: 2

----

1. Resumen
----------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **ID**
     - UC-010
   * - **Nombre**
     - Asignar Funciones a Usuario
   * - **Actor Primario**
     - Administrador de Seguridad
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Alta
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

2. Descripcion
--------------

Permite asignar funciones atomicas del catalogo RBAC a un usuario. Las funciones
determinan que acciones puede realizar el usuario en el sistema. Se validan
restricciones de Segregacion de Funciones (SoD) antes de confirmar la asignacion
y se registra en auditoria (BR_008).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-010 Asignar Funciones
   :align: center
   :scale: 90%

   @startuml
   left to right direction
   skinparam actorStyle awesome
   skinparam backgroundColor #FAFAFA
   skinparam usecase {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
       BorderThickness 2
   }
   skinparam rectangle {
       BackgroundColor #ECEFF1
       BorderColor #455A64
   }

   actor "Administrador\nSeguridad" as ADM
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Access" {
       usecase "UC-010:\nAsignar\nFunciones" as UC010
       usecase "Validar\nSoD" as VSOD
       usecase "Buscar\nUsuario" as BU
       usecase "Seleccionar\nFunciones" as SF
       usecase "Registrar\nEvento" as REG
       usecase "UC-043:\nConfigurar\nSoD" as UC043
   }

   ADM --> UC010
   UC010 ..> BU : <<include>>
   UC010 ..> SF : <<include>>
   UC010 ..> VSOD : <<include>>
   UC010 ..> REG : <<include>>
   UC010 --> SA
   VSOD ..> UC043 : usa reglas
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene sesion activa
2. Administrador tiene funcion ACC-001 (Asignar Funciones)
3. Usuario destino existe y esta ACTIVO
4. Catalogo de funciones disponible

4.2 Trigger
^^^^^^^^^^^

Administrador selecciona "Asignar Funciones" desde perfil de usuario o menu RBAC.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Funciones asignadas al usuario en tabla user_functions
2. Validacion SoD pasada (sin conflictos)
3. Evento FUNCTIONS_ASSIGNED registrado (BR_008)
4. Usuario puede usar las nuevas funciones inmediatamente

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Asignaciones previas se mantienen si hay error
2. Conflictos SoD siempre se detectan antes de confirmar
3. Auditoria registra intento incluso si falla

----

5. Flujo Normal
---------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a "Gestion de Permisos"
     -
   * - 2
     -
     - Verifica permiso ACC-001
   * - 3
     - Busca y selecciona usuario
     -
   * - 4
     -
     - Muestra funciones actuales del usuario
   * - 5
     -
     - Muestra catalogo de funciones disponibles
   * - 6
     - Selecciona funciones a asignar
     -
   * - 7
     - Presiona "Asignar Funciones"
     -
   * - 8
     -
     - Valida restricciones SoD
   * - 9
     -
     - Si SoD OK, inserta en user_functions
   * - 10
     -
     - Registra FUNCTIONS_ASSIGNED en auditoria
   * - 11
     -
     - Muestra mensaje de exito
   * - 12
     -
     - Actualiza vista de funciones del usuario

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-010 Asignar Funciones
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center
   skinparam participant {
       BackgroundColor #E8F5E9
       BorderColor #388E3C
   }
   skinparam database {
       BackgroundColor #FFF3E0
       BorderColor #F57C00
   }

   actor "Admin\nSeguridad" as ADM
   participant "Frontend\n(React)" as FE #E3F2FD
   participant "AccessController\n(DRF)" as AC #E8F5E9
   participant "RBACService" as RBAC #E8F5E9
   participant "SoDValidator" as SOD #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a Gestion Permisos
   activate FE

   FE -> AC: 2. GET /api/users/{userId}/functions
   activate AC
   AC -> DB: SELECT f.* FROM functions f\nJOIN user_functions uf ON...\nWHERE uf.user_id = ?
   DB --> AC: [currentFunctions]
   AC --> FE: 3. {currentFunctions}
   deactivate AC

   FE -> AC: 4. GET /api/functions/catalog
   activate AC
   AC -> DB: SELECT * FROM functions\nWHERE active = true
   DB --> AC: [allFunctions]
   AC --> FE: 5. {catalog}
   deactivate AC

   FE --> ADM: 6. Muestra funciones actuales\ny catalogo disponible

   ADM -> FE: 7. Selecciona funciones\na asignar [F1, F2, F3]

   FE -> AC: 8. POST /api/users/{userId}/functions\n{functions: [F1, F2, F3]}
   activate AC

   AC -> RBAC: 9. checkPermission(adminId, 'ACC-001')
   RBAC --> AC: authorized

   AC -> SOD: 10. validateSoD(userId, newFunctions)
   activate SOD
   SOD -> DB: SELECT * FROM sod_rules\nWHERE function_a IN (...)\nOR function_b IN (...)
   DB --> SOD: [sodRules]

   SOD -> DB: SELECT function_id FROM user_functions\nWHERE user_id = ?
   DB --> SOD: [existingFunctions]

   SOD -> SOD: 11. checkConflicts(\nexisting + new, rules)
   note right: Verifica que ninguna\ncombinacion viole SoD
   SOD --> AC: 12. {valid: true, conflicts: []}
   deactivate SOD

   AC -> DB: 13. INSERT INTO user_functions\n(user_id, function_id, assigned_by, assigned_at)\nVALUES (?, ?, ?, NOW())
   note right: Para cada funcion\nseleccionada
   DB --> AC: OK

   AC -> AUD: 14. logEvent(FUNCTIONS_ASSIGNED,\nadminId, userId, {functions})
   activate AUD
   AUD -> DB: INSERT INTO audit_log
   note right: BR_008
   AUD --> AC: OK
   deactivate AUD

   AC --> FE: 15. 200 OK {assigned: [F1,F2,F3]}
   deactivate AC

   FE --> ADM: 16. "Funciones asignadas exitosamente"
   FE -> FE: 17. Actualizar vista
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Conflicto SoD Detectado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 8 del flujo normal

**Condicion:** Combinacion de funciones viola regla SoD

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 8.1
     - Sistema detecta conflicto SoD
   * - 8.2
     - Sistema muestra funciones en conflicto
   * - 8.3
     - Sistema muestra regla SoD violada
   * - 8.4
     - Admin debe deseleccionar una de las funciones conflictivas

**Retorno:** Paso 6 del flujo normal

7.2 FA-2: Funcion Ya Asignada
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 9 del flujo normal

**Condicion:** Usuario ya tiene alguna de las funciones seleccionadas

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 9.1
     - Sistema detecta duplicados
   * - 9.2
     - Sistema omite funciones ya asignadas
   * - 9.3
     - Sistema solo inserta las nuevas
   * - 9.4
     - Sistema informa cuales se omitieron

**Retorno:** Paso 10 del flujo normal

7.3 FA-3: Asignacion por Agrupador
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 6 del flujo normal

**Condicion:** Admin selecciona un agrupador completo en lugar de funciones individuales

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 6.1
     - Admin selecciona agrupador (ej: "Analista")
   * - 6.2
     - Sistema expande a todas las funciones del agrupador
   * - 6.3
     - Sistema muestra funciones que se asignaran
   * - 6.4
     - Admin confirma

**Retorno:** Paso 7 del flujo normal

----

8. Excepciones
--------------

8.1 EX-1: Usuario No Encontrado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** userId no existe o fue dado de baja

**Accion del Sistema:** Retorna 404 Not Found

**Mensaje al Usuario:** "Usuario no encontrado"

8.2 EX-2: Sin Permiso de Asignacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Administrador no tiene funcion ACC-001

**Accion del Sistema:** Retorna 403 Forbidden

**Mensaje al Usuario:** "No tiene permisos para asignar funciones"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-010 Asignar Funciones
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam activity {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
       DiamondBackgroundColor #FFF9C4
       DiamondBorderColor #F57C00
   }

   start

   :Admin accede a\nGestion de Permisos;

   :Verificar permiso ACC-001;

   if (Tiene permiso?) then (si)

       :Buscar y seleccionar usuario;
       :Mostrar funciones actuales;
       :Mostrar catalogo disponible;

       :Admin selecciona funciones;

       if (Selecciono agrupador?) then (si)
           :Expandir a funciones\nindividuales;
       else (no)
       endif

       :Validar restricciones SoD;

       if (Hay conflicto SoD?) then (si)
           #FFCDD2:Mostrar conflicto;
           :Mostrar regla violada;
           :Admin debe corregir;
       else (no)

           :Filtrar funciones ya asignadas;

           if (Hay nuevas funciones?) then (si)
               :Insertar en user_functions;
               #C8E6C9:Registrar en auditoria\n(BR_008);
               #C8E6C9:Mostrar confirmacion;
           else (no)
               #FFE0B2:Todas ya estaban asignadas;
           endif

       endif

       :Actualizar vista;
       stop

   else (no)
       #FFCDD2:403 Forbidden;
       stop
   endif

   @enduml

----

10. Reglas de Negocio
---------------------

.. list-table::
   :widths: 12 25 63
   :header-rows: 1

   * - BR
     - Nombre
     - Aplicacion en este UC
   * - BR_008
     - Auditoria de Accesos
     - Paso 10: FUNCTIONS_ASSIGNED registra admin, usuario y funciones asignadas
   * - BR_010
     - Segregacion de Funciones
     - Paso 8: Se validan reglas SoD antes de confirmar asignacion

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-010.01
     - Sistema DEBE verificar permiso ACC-001 antes de permitir asignacion
   * - FR-010.02
     - Sistema DEBE mostrar funciones actuales del usuario
   * - FR-010.03
     - Sistema DEBE mostrar catalogo de funciones disponibles
   * - FR-010.04
     - Sistema DEBE permitir seleccion multiple de funciones
   * - FR-010.05
     - Sistema DEBE permitir seleccion por agrupador
   * - FR-010.06
     - Sistema DEBE validar reglas SoD antes de confirmar
   * - FR-010.07
     - Sistema DEBE mostrar conflictos SoD con detalle de regla
   * - FR-010.08
     - Sistema DEBE omitir funciones ya asignadas (sin error)
   * - FR-010.09
     - Sistema DEBE registrar asignacion en auditoria (BR_008)
   * - FR-010.10
     - Sistema DEBE actualizar permisos inmediatamente

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_008 (Auditoria), BR_010 (SoD)
   * - **FR Derivados**
     - FR-010.01 a FR-010.10 (10 requerimientos)
   * - **UC Relacionados**
     - UC-011 (Revocar), UC-043 (Configurar SoD), UC-044 (Consultar)
   * - **Actores RBAC**
     - AGR-008: admin_seguridad
   * - **Funciones RBAC**
     - ACC-001: Asignar Funciones

----

13. Historial de Cambios
------------------------

.. list-table::
   :widths: 12 12 20 56
   :header-rows: 1

   * - Version
     - Fecha
     - Autor
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Equipo IACT
     - Version con PlantUML embebido (Sphinx). 3 diagramas.
   * - 1.0.0
     - 2026-01-05
     - Equipo IACT
     - Version inicial sin diagramas