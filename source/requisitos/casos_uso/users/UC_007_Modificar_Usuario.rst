.. meta::
   :artefacto: UC_007
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/users
   :modulo: MOD_Users
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-007:

==============================================================================
UC-007: Modificar Usuario
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
     - UC-007
   * - **Nombre**
     - Modificar Usuario
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

Permite a un administrador modificar los datos de un usuario existente,
incluyendo nombre, apellido, email, telefono y estado. Los cambios se
registran en auditoria (BR_008) con valores anteriores y nuevos para
trazabilidad completa.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-007 Modificar Usuario
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

   rectangle "MOD_Users" {
       usecase "UC-007:\nModificar\nUsuario" as UC007
       usecase "Validar\nDatos" as VD
       usecase "Registrar\nCambios" as RC
       usecase "UC-009:\nListar\nUsuarios" as UC009
   }

   ADM --> UC007
   UC007 ..> VD : <<include>>
   UC007 ..> RC : <<include>>
   UC009 .> UC007 : <<extends>>
   UC007 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene sesion activa
2. Administrador tiene funcion USR-002 (Modificar Usuario)
3. Usuario a modificar existe en el sistema

4.2 Trigger
^^^^^^^^^^^

Administrador selecciona "Editar" en un usuario desde la lista de usuarios.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Datos del usuario actualizados en BD
2. Evento USER_MODIFIED registrado con valores old/new (BR_008)
3. Si se cambio email, se mantiene unicidad

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Username no se puede modificar (es inmutable)
2. Cambios son atomicos
3. Auditoria siempre registra cambios intentados

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
     - Hace clic en "Editar"
     -
   * - 3
     -
     - Verifica permiso USR-002
   * - 4
     -
     - Obtiene datos actuales del usuario
   * - 5
     -
     - Muestra formulario con datos precargados
   * - 6
     - Modifica campos deseados
     -
   * - 7
     - Presiona "Guardar Cambios"
     -
   * - 8
     -
     - Valida formato de campos modificados
   * - 9
     -
     - Si email cambio, valida unicidad
   * - 10
     -
     - Compara valores old vs new
   * - 11
     -
     - Actualiza registro en BD
   * - 12
     -
     - Registra USER_MODIFIED en auditoria (BR_008)
   * - 13
     -
     - Muestra mensaje "Usuario actualizado"

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-007 Modificar Usuario
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
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Selecciona usuario, clic "Editar"
   activate FE

   FE -> UC: 2. GET /api/users/{userId}
   activate UC
   UC -> DB: SELECT * FROM users WHERE id=?
   DB --> UC: {userData}
   UC --> FE: 3. 200 OK {user}
   deactivate UC

   FE --> ADM: 4. Formulario con datos actuales
   note right: Username deshabilitado\n(no editable)

   ADM -> FE: 5. Modifica campos
   ADM -> FE: 6. Clic "Guardar"

   FE -> UC: 7. PUT /api/users/{userId}\n{nombre, apellido, email, telefono, status}
   activate UC

   UC -> RBAC: 8. checkPermission(adminId, 'USR-002')
   activate RBAC
   RBAC --> UC: authorized
   deactivate RBAC

   UC -> US: 9. updateUser(userId, newData)
   activate US

   US -> DB: 10. SELECT * FROM users WHERE id=?
   DB --> US: {oldData}

   US -> US: 11. validateFields(newData)

   alt Email cambio
       US -> DB: 12. SELECT id FROM users\nWHERE email=? AND id!=?
       DB --> US: null (disponible)
   end

   US -> US: 13. buildChangeset(oldData, newData)
   note right: Detecta que campos\ncambiaron realmente

   US -> DB: 14. UPDATE users SET\nnombre=?, apellido=?, email=?,\ntelefono=?, status=?,\nupdated_at=NOW(), updated_by=?
   DB --> US: OK

   US -> AUD: 15. logEvent(USER_MODIFIED,\nadminId, userId, {old, new})
   activate AUD
   AUD -> DB: INSERT INTO audit_log\n(action, performed_by, target_user,\nold_values, new_values)
   note right: BR_008:\nGuarda valores\nanteriores y nuevos
   AUD --> US: OK
   deactivate AUD

   US --> UC: 16. {user: updatedUser}
   deactivate US

   UC --> FE: 17. 200 OK {user}
   deactivate UC

   FE --> ADM: 18. "Usuario actualizado exitosamente"
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Email Duplicado
^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 9 del flujo normal

**Condicion:** Nuevo email ya pertenece a otro usuario

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 9.1
     - Sistema detecta email duplicado
   * - 9.2
     - Sistema muestra "El email ya esta registrado"
   * - 9.3
     - Admin corrige email

**Retorno:** Paso 6 del flujo normal

7.2 FA-2: Sin Cambios Detectados
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 10 del flujo normal

**Condicion:** Valores nuevos son identicos a los actuales

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 10.1
     - Sistema detecta que no hay cambios
   * - 10.2
     - Sistema muestra "No se detectaron cambios"
   * - 10.3
     - No se actualiza BD ni auditoria

**Retorno:** Fin del caso de uso

7.3 FA-3: Cambiar Estado a INACTIVO
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 6 del flujo normal

**Condicion:** Admin cambia status de ACTIVO a INACTIVO

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 6.1
     - Sistema muestra advertencia de confirmacion
   * - 6.2
     - Admin confirma desactivacion
   * - 6.3
     - Sistema invalida sesiones activas del usuario
   * - 6.4
     - Continua con paso 7

**Retorno:** Paso 7 del flujo normal

----

8. Excepciones
--------------

8.1 EX-1: Usuario No Encontrado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** userId no existe en BD (fue eliminado)

**Accion del Sistema:** Retorna 404 Not Found

**Mensaje al Usuario:** "Usuario no encontrado"

8.2 EX-2: Sin Permiso de Modificacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Administrador no tiene funcion USR-002

**Accion del Sistema:** Retorna 403 Forbidden

**Mensaje al Usuario:** "No tiene permisos para modificar usuarios"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-007 Modificar Usuario
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

   :Admin selecciona usuario\ny hace clic en "Editar";

   :Verificar permiso USR-002;

   if (Tiene permiso?) then (si)

       :Obtener datos actuales;
       :Mostrar formulario precargado;

       :Admin modifica campos;

       :Validar formato de campos;

       if (Formato valido?) then (si)

           if (Email cambio?) then (si)
               :Verificar unicidad email;

               if (Email disponible?) then (no)
                   #FFE0B2:Error: "Email ya registrado";
                   stop
               else (si)
               endif
           else (no)
           endif

           :Comparar old vs new;

           if (Hay cambios?) then (si)

               if (Cambio a INACTIVO?) then (si)
                   :Confirmar desactivacion;
                   :Invalidar sesiones activas;
               else (no)
               endif

               :Actualizar en BD;
               #C8E6C9:Registrar en auditoria\n(BR_008)\ncon old/new values;
               #C8E6C9:Mostrar "Usuario actualizado";

           else (no)
               #FFE0B2:Mostrar "Sin cambios";
           endif

           stop

       else (no)
           #FFE0B2:Mostrar errores validacion;
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
     - Paso 12: USER_MODIFIED registra admin, usuario, valores old y new

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-007.01
     - Sistema DEBE verificar permiso USR-002 antes de permitir edicion
   * - FR-007.02
     - Sistema DEBE mostrar formulario con datos actuales precargados
   * - FR-007.03
     - Sistema DEBE deshabilitar campo username (inmutable)
   * - FR-007.04
     - Sistema DEBE validar formato de campos modificados
   * - FR-007.05
     - Sistema DEBE validar unicidad de email si cambio
   * - FR-007.06
     - Sistema DEBE detectar si hubo cambios reales
   * - FR-007.07
     - Sistema DEBE invalidar sesiones si usuario pasa a INACTIVO
   * - FR-007.08
     - Sistema DEBE registrar old/new values en auditoria (BR_008)
   * - FR-007.09
     - Sistema DEBE mostrar mensaje de confirmacion

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
     - FR-007.01 a FR-007.09 (9 requerimientos)
   * - **UC Relacionados**
     - UC-006 (Crear), UC-008 (Baja), UC-009 (Listar)
   * - **Actores RBAC**
     - AGR-007: admin_usuarios
   * - **Funciones RBAC**
     - USR-002: Modificar Usuario

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
