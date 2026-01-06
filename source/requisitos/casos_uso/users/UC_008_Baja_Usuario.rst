.. meta::
   :artefacto: UC_008
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/users
   :modulo: MOD_Users
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-008:

==============================================================================
UC-008: Dar de Baja Usuario
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
     - UC-008
   * - **Nombre**
     - Dar de Baja Usuario
   * - **Actor Primario**
     - Administrador de Usuarios
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Users
   * - **Complejidad**
     - Baja
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

2. Descripcion
--------------

Permite a un administrador dar de baja logica a un usuario, cambiando su
estado a INACTIVO. No es eliminacion fisica; el usuario y su historial
permanecen para auditoria. Todas las sesiones activas se invalidan y
el usuario no puede volver a autenticarse hasta ser reactivado.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-008 Dar de Baja Usuario
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

   actor "Administrador\nUsuarios" as ADM
   actor "Sistema\nAuditoria" as SA #LightGray
   actor "Usuario\nAfectado" as UA #LightGray

   rectangle "MOD_Users" {
       usecase "UC-008:\nDar de Baja\nUsuario" as UC008
       usecase "Invalidar\nSesiones" as INV
       usecase "Revocar\nPermisos" as RP
       usecase "Registrar\nEvento" as REG
       usecase "UC-009:\nListar\nUsuarios" as UC009
   }

   ADM --> UC008
   UC008 ..> INV : <<include>>
   UC008 ..> RP : <<include>>
   UC008 ..> REG : <<include>>
   UC009 .> UC008 : <<extends>>
   UC008 --> SA
   UC008 --> UA : afecta
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene sesion activa
2. Administrador tiene funcion USR-003 (Dar de Baja Usuario)
3. Usuario a dar de baja existe y tiene estado ACTIVO
4. Usuario a dar de baja no es el propio administrador

4.2 Trigger
^^^^^^^^^^^

Administrador selecciona "Dar de Baja" en un usuario desde la lista.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Usuario con estado INACTIVO
2. Todas las sesiones del usuario invalidadas
3. Permisos revocados temporalmente (no eliminados)
4. Evento USER_DEACTIVATED registrado (BR_008)
5. Usuario no puede autenticarse

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Baja es logica, no fisica (datos preservados)
2. Historial de auditoria intacto
3. Usuario puede ser reactivado posteriormente

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
     - Selecciona usuario de la lista
     -
   * - 2
     - Hace clic en "Dar de Baja"
     -
   * - 3
     -
     - Verifica permiso USR-003
   * - 4
     -
     - Verifica que usuario no sea el admin actual
   * - 5
     -
     - Muestra modal de confirmacion con datos del usuario
   * - 6
     -
     - Solicita motivo de baja (campo obligatorio)
   * - 7
     - Ingresa motivo de baja
     -
   * - 8
     - Confirma la baja
     -
   * - 9
     -
     - Invalida todas las sesiones activas del usuario
   * - 10
     -
     - Suspende permisos (marca como inactivos)
   * - 11
     -
     - Actualiza status = INACTIVO en BD
   * - 12
     -
     - Registra USER_DEACTIVATED con motivo (BR_008)
   * - 13
     -
     - Muestra mensaje "Usuario dado de baja"
   * - 14
     -
     - Actualiza lista de usuarios

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-008 Dar de Baja Usuario
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

   actor "Admin\nUsuarios" as ADM
   participant "Frontend\n(React)" as FE #E3F2FD
   participant "UserController\n(DRF)" as UC #E8F5E9
   participant "RBACService" as RBAC #E8F5E9
   participant "UserService" as US #E8F5E9
   participant "SessionService" as SS #E8F5E9
   participant "PermissionService" as PS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Selecciona usuario,\nclic "Dar de Baja"
   activate FE

   FE --> ADM: 2. Modal: "¿Dar de baja a {user}?"\nCampo: Motivo (obligatorio)

   ADM -> FE: 3. Ingresa motivo y confirma

   FE -> UC: 4. DELETE /api/users/{userId}\n{reason: "Motivo de baja"}\nAuthorization: Bearer {token}
   activate UC

   UC -> RBAC: 5. checkPermission(adminId, 'USR-003')
   activate RBAC
   RBAC --> UC: authorized
   deactivate RBAC

   UC -> UC: 6. Verificar userId != adminId
   note right: Admin no puede\ndarse de baja a si mismo

   UC -> US: 7. deactivateUser(userId, adminId, reason)
   activate US

   US -> DB: 8. SELECT * FROM users WHERE id=?
   DB --> US: {user, status='ACTIVO'}

   US -> SS: 9. invalidateAllSessions(userId)
   activate SS
   SS -> DB: UPDATE sessions SET active=false\nWHERE user_id=?
   SS -> DB: INSERT INTO token_blacklist\n(SELECT token FROM sessions\nWHERE user_id=?)
   SS --> US: sessionsInvalidated
   deactivate SS

   US -> PS: 10. suspendPermissions(userId)
   activate PS
   PS -> DB: UPDATE user_functions\nSET suspended=true, suspended_at=NOW()\nWHERE user_id=?
   note right: Permisos suspendidos,\nno eliminados
   PS --> US: permissionsSuspended
   deactivate PS

   US -> DB: 11. UPDATE users SET\nstatus='INACTIVO',\ndeactivated_at=NOW(),\ndeactivated_by=?,\ndeactivation_reason=?
   DB --> US: OK

   US -> AUD: 12. logEvent(USER_DEACTIVATED,\nadminId, userId, reason)
   activate AUD
   AUD -> DB: INSERT INTO audit_log\n(action, performed_by, target_user,\ndetails={reason})
   note right: BR_008:\nIncluye motivo
   AUD --> US: OK
   deactivate AUD

   US --> UC: 13. {deactivated: true}
   deactivate US

   UC --> FE: 14. 200 OK {message}
   deactivate UC

   FE -> FE: 15. Actualizar lista usuarios
   FE --> ADM: 16. "Usuario dado de baja exitosamente"
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Cancelar Baja
^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 5 del flujo normal

**Condicion:** Admin hace clic en "Cancelar" en modal de confirmacion

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 5.1
     - Sistema cierra modal de confirmacion
   * - 5.2
     - No se realiza ninguna accion
   * - 5.3
     - Admin permanece en lista de usuarios

**Retorno:** Fin del caso de uso (sin cambios)

7.2 FA-2: Usuario Ya Inactivo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 8 del flujo normal (verificacion BD)

**Condicion:** Usuario ya tiene status INACTIVO

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 8.1
     - Sistema detecta usuario ya inactivo
   * - 8.2
     - Sistema muestra "El usuario ya esta dado de baja"
   * - 8.3
     - Ofrece opcion "Reactivar Usuario"

**Retorno:** Fin del caso de uso

7.3 FA-3: Reactivar Usuario
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Opcion en lugar de dar de baja

**Condicion:** Admin selecciona "Reactivar" en usuario INACTIVO

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Admin selecciona "Reactivar"
   * - 2
     - Sistema solicita confirmacion
   * - 3
     - Sistema cambia status a ACTIVO
   * - 4
     - Sistema reactiva permisos suspendidos
   * - 5
     - Sistema registra USER_REACTIVATED en auditoria

**Retorno:** Fin del caso de uso

----

8. Excepciones
--------------

8.1 EX-1: Intento de Auto-Baja
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Admin intenta darse de baja a si mismo

**Accion del Sistema:** Rechaza la operacion

**Mensaje al Usuario:** "No puede darse de baja a si mismo"

8.2 EX-2: Sin Motivo de Baja
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Admin no ingresa motivo (campo obligatorio)

**Accion del Sistema:** No permite confirmar

**Mensaje al Usuario:** "Debe ingresar un motivo de baja"

8.3 EX-3: Usuario Con Procesos Pendientes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario tiene reportes o alertas asignadas

**Accion del Sistema:** Muestra advertencia, permite continuar

**Mensaje al Usuario:** "Usuario tiene X procesos asignados. ¿Continuar?"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-008 Dar de Baja Usuario
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

   :Admin selecciona usuario\ny hace clic en "Dar de Baja";

   :Verificar permiso USR-003;

   if (Tiene permiso?) then (si)

       if (Es el propio admin?) then (si)
           #FFCDD2:Error: "No puede darse\nde baja a si mismo";
           stop
       else (no)
       endif

       :Obtener datos del usuario;

       if (Ya esta INACTIVO?) then (si)
           #FFE0B2:Mostrar "Ya esta\ndado de baja";
           :Ofrecer Reactivar;
           stop
       else (no)
       endif

       :Mostrar modal confirmacion;
       :Solicitar motivo de baja;

       if (Admin confirma?) then (si)

           if (Motivo ingresado?) then (si)

               #C8E6C9:Invalidar todas las sesiones;
               :Suspender permisos;
               :Actualizar status = INACTIVO;
               #C8E6C9:Registrar USER_DEACTIVATED\n(BR_008) con motivo;
               :Actualizar lista;
               #C8E6C9:Mostrar confirmacion;
               stop

           else (no)
               #FFE0B2:Error: "Motivo obligatorio";
           endif

       else (no)
           :Cancelar operacion;
           stop
       endif

   else (no)
       #FFCDD2:403 Forbidden;
       stop
   endif

   stop
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
     - Paso 12: USER_DEACTIVATED registra admin, usuario y motivo de baja

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-008.01
     - Sistema DEBE verificar permiso USR-003 antes de permitir baja
   * - FR-008.02
     - Sistema DEBE impedir que admin se de de baja a si mismo
   * - FR-008.03
     - Sistema DEBE mostrar modal de confirmacion con datos del usuario
   * - FR-008.04
     - Sistema DEBE requerir motivo de baja (obligatorio)
   * - FR-008.05
     - Sistema DEBE invalidar todas las sesiones del usuario
   * - FR-008.06
     - Sistema DEBE suspender permisos (no eliminar)
   * - FR-008.07
     - Sistema DEBE cambiar status a INACTIVO
   * - FR-008.08
     - Sistema DEBE registrar evento con motivo en auditoria (BR_008)
   * - FR-008.09
     - Sistema DEBE permitir reactivar usuarios dados de baja

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
     - FR-008.01 a FR-008.09 (9 requerimientos)
   * - **UC Relacionados**
     - UC-006 (Crear), UC-007 (Modificar), UC-009 (Listar)
   * - **Actores RBAC**
     - AGR-007: admin_usuarios
   * - **Funciones RBAC**
     - USR-003: Dar de Baja Usuario

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
