.. meta::
   :artefacto: UC_013
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-013:

==============================================================================
UC-013: Asignar Funcion a Rol
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
     - UC-013
   * - **Nombre**
     - Asignar Funcion a Rol
   * - **Actor Primario**
     - Administrador de Seguridad
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Critica
   * - **BReq Origen**
     - BReq-004: Control de Acceso Basado en Roles

----

2. Descripcion
--------------

Permite asignar funciones (permisos) a roles, definiendo que acciones
puede realizar cada rol. Las funciones se muestran agrupadas por modulo
para facilitar la seleccion. Los cambios aplican inmediatamente a todos
los usuarios con el rol. Soporta matriz de permisos para visualizacion
y edicion rapida.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-013 Asignar Funcion a Rol
   :align: center
   :scale: 90%

   @startuml
   left to right direction
   skinparam actorStyle awesome
   skinparam backgroundColor #FAFAFA
   skinparam usecase {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
   }

   actor "Administrador\nSeguridad" as ADM
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Access" {
       usecase "UC-013:\nAsignar Funcion\na Rol" as UC013
       usecase "Asignar\nIndividual" as AI
       usecase "Asignar por\nModulo" as AM
       usecase "Quitar\nFuncion" as QF
       usecase "Ver Matriz\nPermisos" as VMP
       usecase "Copiar de\nOtro Rol" as COR
   }

   ADM --> UC013
   UC013 ..> AI : <<extends>>
   UC013 ..> AM : <<extends>>
   UC013 ..> QF : <<extends>>
   UC013 ..> VMP : <<include>>
   UC013 ..> COR : <<extends>>
   UC013 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion FUN-002 (Asignar Funciones)
2. Rol destino existe y esta activo
3. Funcion(es) a asignar existen y estan activas

4.2 Trigger
^^^^^^^^^^^

Usuario accede desde gestion de roles: "Asignar Funciones".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Relacion rol-funcion creada en role_functions
2. Cache de permisos invalidado para usuarios del rol
3. Usuarios con el rol tienen nuevos permisos inmediatamente
4. Evento FUNCTION_ASSIGNED registrado (BR_008)

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
     - Selecciona rol para asignar funciones
     -
   * - 2
     -
     - Verifica permiso FUN-002
   * - 3
     -
     - Carga funciones actuales del rol
   * - 4
     -
     - Carga todas las funciones por modulo
   * - 5
     -
     - Muestra matriz con checkboxes
   * - 6
     - Marca/desmarca funciones
     -
   * - 7
     - Presiona "Guardar Cambios"
     -
   * - 8
     -
     - Calcula diferencias (add/remove)
   * - 9
     -
     - Aplica cambios en role_functions
   * - 10
     -
     - Invalida cache de todos los usuarios del rol
   * - 11
     -
     - Registra cambios en auditoria
   * - 12
     -
     - Muestra confirmacion

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-013 Asignar Funcion a Rol
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "RoleFunctionController" as RFC #E8F5E9
   participant "FunctionService" as FS #E8F5E9
   participant "CacheService" as CS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a funciones del rol
   FE -> RFC: 2. GET /api/roles/{id}/functions/matrix
   activate RFC

   RFC -> DB: 3. SELECT f.*, rf.role_id IS NOT NULL as assigned\nFROM functions f\nLEFT JOIN role_functions rf\n  ON f.id = rf.function_id AND rf.role_id = ?\nORDER BY f.module_id, f.code
   DB --> RFC: [functionsWithStatus]

   RFC --> FE: 4. {functionsByModule, assigned}
   deactivate RFC

   FE --> ADM: 5. Matriz de permisos

   ADM -> FE: 6. Modifica checkboxes
   ADM -> FE: 7. Guardar Cambios

   FE -> RFC: 8. PUT /api/roles/{id}/functions\n{functionIds: [1,2,5,8]}
   activate RFC

   RFC -> FS: 9. updateRoleFunctions(roleId, newIds)
   activate FS

   FS -> DB: 10. SELECT function_id FROM role_functions\nWHERE role_id = ?
   DB --> FS: [currentIds]

   FS -> FS: 11. calculateDiff(current, new)
   note right
       toAdd: [5, 8]
       toRemove: [3, 4]
   end note

   FS -> DB: 12. DELETE FROM role_functions\nWHERE role_id = ? AND function_id IN (3,4)
   FS -> DB: 13. INSERT INTO role_functions\n(role_id, function_id) VALUES (?, 5), (?, 8)

   FS -> DB: 14. SELECT user_id FROM user_roles\nWHERE role_id = ?
   DB --> FS: [userIds]

   FS -> CS: 15. invalidateUsersPermissions(userIds)
   CS --> FS: OK

   FS -> AUD: 16. logEvent('FUNCTION_ASSIGNED',\n{roleId, added: [5,8], removed: [3,4]})
   AUD -> DB: INSERT audit_log

   FS --> RFC: 17. {added: 2, removed: 2}
   deactivate FS

   RFC --> FE: 18. 200 OK
   deactivate RFC

   FE --> ADM: 19. "Permisos actualizados.\n2 funciones agregadas, 2 removidas."
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Asignar Modulo Completo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Admin marca checkbox de modulo

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Admin marca checkbox del modulo "MOD_Users"
   * - 2
     - Sistema marca todas las funciones del modulo
   * - 3
     - Admin puede desmarcar funciones individuales
   * - 4
     - Guardar aplica seleccion final

7.2 FA-2: Copiar de Otro Rol
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Admin hace clic en "Copiar de..."

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Sistema muestra lista de roles
   * - 2
     - Admin selecciona rol origen
   * - 3
     - Sistema copia seleccion de funciones
   * - 4
     - Admin puede ajustar antes de guardar

7.3 FA-3: Ver Impacto
^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Admin hace clic en "Ver Usuarios Afectados"

Sistema muestra lista de usuarios que tienen este rol.

----

8. Excepciones
--------------

8.1 EX-1: Rol Protegido
^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Intento de modificar funciones de rol ADMIN

**Mensaje:** "Las funciones del rol ADMIN no pueden modificarse."

8.2 EX-2: Funcion Inactiva
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Funcion seleccionada esta inactiva

**Mensaje:** "La funcion '[CODE]' esta inactiva y no puede asignarse."

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-013 Asignar Funcion a Rol
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Verificar permiso FUN-002;

   if (Tiene permiso?) then (si)
       :Cargar rol;

       if (Rol protegido?) then (si)
           #FFE0B2:Solo lectura;
       else (no)
           :Cargar matriz de funciones;
           :Marcar funciones actuales;

           if (Copiar de otro rol?) then (si)
               :Seleccionar rol origen;
               :Copiar seleccion;
           else (no)
           endif

           :Usuario modifica checkboxes;

           if (Marcar modulo completo?) then (si)
               :Seleccionar todas del modulo;
           else (no)
           endif

           :Guardar cambios;
           :Calcular diferencias;

           fork
               :Agregar nuevas funciones;
           fork again
               :Remover funciones quitadas;
           end fork

           :Obtener usuarios del rol;
           :Invalidar cache de permisos;
           #C8E6C9:FUNCTION_ASSIGNED;
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
     - Aplicacion
   * - BR_008
     - Auditoria
     - Registra funciones agregadas y removidas
   * - BR_024
     - Roles Protegidos
     - ADMIN no puede modificarse
   * - BR_030
     - Propagacion Inmediata
     - Cambios aplican sin relogin

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-013.01
     - Verificar permiso FUN-002
   * - FR-013.02
     - Mostrar matriz de funciones por modulo
   * - FR-013.03
     - Mostrar funciones actuales del rol marcadas
   * - FR-013.04
     - Permitir marcar/desmarcar funciones individuales
   * - FR-013.05
     - Permitir seleccionar modulo completo
   * - FR-013.06
     - Permitir copiar funciones de otro rol
   * - FR-013.07
     - Calcular diferencias antes de guardar
   * - FR-013.08
     - Invalidar cache de todos los usuarios del rol
   * - FR-013.09
     - Mostrar resumen de cambios aplicados
   * - FR-013.10
     - Proteger roles del sistema

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-004
   * - **BR Aplicables**
     - BR_008, BR_024, BR_030
   * - **FR Derivados**
     - FR-013.01 a FR-013.10
   * - **UC Relacionados**
     - UC-010 (Roles), UC-011 (Funciones)
   * - **Funcion RBAC**
     - FUN-002

----

13. Historial de Cambios
------------------------

.. list-table::
   :widths: 12 12 76
   :header-rows: 1

   * - Version
     - Fecha
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Version completa. Matriz permisos. Copiar de rol. Diff de cambios.