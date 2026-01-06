.. meta::
   :artefacto: UC_011
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-011:

==============================================================================
UC-011: Revocar Funciones a Usuario
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
     - UC-011
   * - **Nombre**
     - Revocar Funciones a Usuario
   * - **Actor Primario**
     - Administrador de Seguridad
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

2. Descripcion
--------------

Permite revocar funciones previamente asignadas a un usuario. Las funciones
revocadas dejan de estar disponibles inmediatamente. Se registra en auditoria
(BR_008) con motivo de revocacion para trazabilidad.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-011 Revocar Funciones
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
   actor "Usuario\nAfectado" as UA #LightGray

   rectangle "MOD_Access" {
       usecase "UC-011:\nRevocar\nFunciones" as UC011
       usecase "Buscar\nUsuario" as BU
       usecase "Seleccionar\nFunciones" as SF
       usecase "Registrar\nEvento" as REG
   }

   ADM --> UC011
   UC011 ..> BU : <<include>>
   UC011 ..> SF : <<include>>
   UC011 ..> REG : <<include>>
   UC011 --> SA
   UC011 --> UA : afecta
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene sesion activa
2. Administrador tiene funcion ACC-002 (Revocar Funciones)
3. Usuario destino tiene al menos una funcion asignada

4.2 Trigger
^^^^^^^^^^^

Administrador selecciona "Revocar Funciones" desde perfil de usuario.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Funciones eliminadas de tabla user_functions
2. Evento FUNCTIONS_REVOKED registrado (BR_008)
3. Usuario pierde acceso a funcionalidades inmediatamente

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Revocacion es blanda (se puede reasignar)
2. Historial de asignacion se mantiene en auditoria

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
     - Accede a funciones del usuario
     -
   * - 2
     -
     - Verifica permiso ACC-002
   * - 3
     -
     - Muestra funciones asignadas al usuario
   * - 4
     - Selecciona funciones a revocar
     -
   * - 5
     - Presiona "Revocar Funciones"
     -
   * - 6
     -
     - Muestra modal de confirmacion
   * - 7
     -
     - Solicita motivo de revocacion
   * - 8
     - Ingresa motivo y confirma
     -
   * - 9
     -
     - Elimina registros de user_functions
   * - 10
     -
     - Registra FUNCTIONS_REVOKED en auditoria
   * - 11
     -
     - Muestra mensaje de exito
   * - 12
     -
     - Actualiza vista de funciones

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-011 Revocar Funciones
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
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a funciones del usuario
   activate FE

   FE -> AC: 2. GET /api/users/{userId}/functions
   activate AC
   AC -> DB: SELECT f.*, uf.assigned_at\nFROM functions f\nJOIN user_functions uf ON...
   DB --> AC: [assignedFunctions]
   AC --> FE: 3. {functions}
   deactivate AC

   FE --> ADM: 4. Lista de funciones con checkbox

   ADM -> FE: 5. Selecciona [F1, F2] a revocar
   ADM -> FE: 6. Clic "Revocar"

   FE --> ADM: 7. Modal: "¿Revocar funciones?"\nCampo: Motivo

   ADM -> FE: 8. Ingresa motivo, confirma

   FE -> AC: 9. DELETE /api/users/{userId}/functions\n{functions: [F1, F2], reason: "..."}
   activate AC

   AC -> RBAC: 10. checkPermission(adminId, 'ACC-002')
   RBAC --> AC: authorized

   AC -> DB: 11. DELETE FROM user_functions\nWHERE user_id = ?\nAND function_id IN (F1, F2)
   DB --> AC: {deleted: 2}

   AC -> AUD: 12. logEvent(FUNCTIONS_REVOKED,\nadminId, userId, {functions, reason})
   activate AUD
   AUD -> DB: INSERT INTO audit_log\n(action, performed_by, target_user,\ndetails={functions, reason})
   note right: BR_008:\nIncluye motivo
   AUD --> AC: OK
   deactivate AUD

   AC --> FE: 13. 200 OK {revoked: [F1, F2]}
   deactivate AC

   FE --> ADM: 14. "Funciones revocadas exitosamente"
   FE -> FE: 15. Actualizar lista
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Revocar Todas las Funciones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 4 del flujo normal

**Condicion:** Admin selecciona "Revocar Todas"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 4.1
     - Admin hace clic en "Seleccionar Todas"
   * - 4.2
     - Sistema selecciona todas las funciones
   * - 4.3
     - Sistema muestra advertencia especial
   * - 4.4
     - Admin confirma revocacion total

**Retorno:** Paso 5 del flujo normal

7.2 FA-2: Cancelar Revocacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 6 del flujo normal

**Condicion:** Admin cancela en modal de confirmacion

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 6.1
     - Admin hace clic en "Cancelar"
   * - 6.2
     - Sistema cierra modal
   * - 6.3
     - No se realiza ninguna accion

**Retorno:** Paso 3 del flujo normal

----

8. Excepciones
--------------

8.1 EX-1: Usuario Sin Funciones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario no tiene funciones asignadas

**Accion del Sistema:** Muestra mensaje informativo

**Mensaje al Usuario:** "El usuario no tiene funciones asignadas"

8.2 EX-2: Sin Motivo de Revocacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Admin no ingresa motivo (campo obligatorio)

**Accion del Sistema:** No permite confirmar

**Mensaje al Usuario:** "Debe ingresar un motivo de revocacion"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-011 Revocar Funciones
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

   :Admin accede a funciones\ndel usuario;

   :Verificar permiso ACC-002;

   if (Tiene permiso?) then (si)

       :Obtener funciones asignadas;

       if (Tiene funciones?) then (si)

           :Mostrar lista con checkboxes;

           :Admin selecciona funciones;

           :Mostrar modal confirmacion;
           :Solicitar motivo;

           if (Admin confirma?) then (si)

               if (Motivo ingresado?) then (si)
                   :Eliminar de user_functions;
                   #C8E6C9:Registrar FUNCTIONS_REVOKED\n(BR_008) con motivo;
                   :Actualizar vista;
                   #C8E6C9:Mostrar confirmacion;
               else (no)
                   #FFE0B2:Error: Motivo obligatorio;
               endif

           else (no)
               :Cancelar operacion;
           endif

       else (no)
           #FFE0B2:Usuario sin funciones;
       endif

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
     - Paso 10: FUNCTIONS_REVOKED registra admin, usuario, funciones y motivo

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-011.01
     - Sistema DEBE verificar permiso ACC-002 antes de permitir revocacion
   * - FR-011.02
     - Sistema DEBE mostrar funciones asignadas con opcion de seleccion
   * - FR-011.03
     - Sistema DEBE permitir seleccion multiple
   * - FR-011.04
     - Sistema DEBE permitir "Seleccionar Todas"
   * - FR-011.05
     - Sistema DEBE solicitar confirmacion antes de revocar
   * - FR-011.06
     - Sistema DEBE requerir motivo de revocacion (obligatorio)
   * - FR-011.07
     - Sistema DEBE eliminar registros de user_functions
   * - FR-011.08
     - Sistema DEBE registrar evento con motivo en auditoria (BR_008)
   * - FR-011.09
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
     - BR_008 (Auditoria de Accesos)
   * - **FR Derivados**
     - FR-011.01 a FR-011.09 (9 requerimientos)
   * - **UC Relacionados**
     - UC-010 (Asignar), UC-044 (Consultar)
   * - **Actores RBAC**
     - AGR-008: admin_seguridad
   * - **Funciones RBAC**
     - ACC-002: Revocar Funciones

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