.. meta::
   :artefacto: UC_012
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-012:

==============================================================================
UC-012: Asignar Rol a Usuario
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
     - UC-012
   * - **Nombre**
     - Asignar Rol a Usuario
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

Permite asignar uno o mas roles a un usuario, estableciendo asi sus
permisos en el sistema. Soporta asignacion individual, masiva y con
vigencia temporal (fecha desde/hasta). La asignacion hereda todas las
funciones de los roles asignados. Un usuario puede tener multiples
roles simultaneos (BR_028).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-012 Asignar Rol
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
       usecase "UC-012:\nAsignar Rol\na Usuario" as UC012
       usecase "Asignacion\nIndividual" as AI
       usecase "Asignacion\nMasiva" as AM
       usecase "Con Vigencia\nTemporal" as VT
       usecase "Quitar\nRol" as QR
       usecase "Ver Roles\nUsuario" as VRU
   }

   ADM --> UC012
   UC012 ..> AI : <<extends>>
   UC012 ..> AM : <<extends>>
   UC012 ..> VT : <<extends>>
   UC012 ..> QR : <<extends>>
   UC012 ..> VRU : <<include>>
   UC012 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion ROL-002 (Asignar Roles)
2. Usuario destino existe y esta activo
3. Rol a asignar existe y esta activo

4.2 Trigger
^^^^^^^^^^^

- Desde gestion de usuarios: clic en "Asignar Roles"
- Desde gestion de roles: clic en "Asignar a Usuarios"

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Relacion usuario-rol creada en user_roles
2. Cache de permisos del usuario invalidado
3. Usuario tiene acceso inmediato a nuevas funciones
4. Evento ROLE_ASSIGNED registrado (BR_008)

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
     - Selecciona usuario para asignar rol
     -
   * - 2
     -
     - Verifica permiso ROL-002
   * - 3
     -
     - Muestra roles actuales del usuario
   * - 4
     -
     - Muestra roles disponibles para asignar
   * - 5
     - Selecciona rol(es) a asignar
     -
   * - 6
     - (Opcional) Define fecha desde/hasta
     -
   * - 7
     - Presiona "Asignar"
     -
   * - 8
     -
     - Valida que rol no este ya asignado
   * - 9
     -
     - Crea registro en user_roles
   * - 10
     -
     - Invalida cache de permisos usuario
   * - 11
     -
     - Registra ROLE_ASSIGNED (BR_008)
   * - 12
     -
     - Muestra confirmacion

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-012 Asignar Rol a Usuario
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "UserRoleController" as URC #E8F5E9
   participant "RoleService" as RS #E8F5E9
   participant "CacheService" as CS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Selecciona usuario
   FE -> URC: 2. GET /api/users/{id}/roles
   activate URC

   URC -> DB: 3. SELECT r.* FROM roles r\nJOIN user_roles ur ON r.id = ur.role_id\nWHERE ur.user_id = ?
   DB --> URC: [assignedRoles]

   URC -> DB: 4. SELECT * FROM roles\nWHERE status = 'ACTIVE'\nAND id NOT IN (assigned)
   DB --> URC: [availableRoles]

   URC --> FE: 5. {assigned, available}
   deactivate URC

   FE --> ADM: 6. Panel de asignacion

   ADM -> FE: 7. Selecciona roles y asigna
   FE -> URC: 8. POST /api/users/{id}/roles\n{roleIds: [1,2], validFrom, validUntil}
   activate URC

   URC -> RS: 9. assignRoles(userId, roleIds, dates)
   activate RS

   loop Para cada rol
       RS -> DB: 10. SELECT id FROM user_roles\nWHERE user_id = ? AND role_id = ?
       DB --> RS: [] (no existe)

       RS -> DB: 11. INSERT INTO user_roles\n(user_id, role_id, valid_from, valid_until)
       DB --> RS: OK
   end

   RS -> CS: 12. invalidateUserPermissions(userId)
   CS --> RS: OK
   note right: Usuario obtiene\nnuevos permisos\ninmediatamente

   RS -> AUD: 13. logEvent('ROLE_ASSIGNED',\n{userId, roleIds, assignedBy})
   AUD -> DB: INSERT audit_log

   RS --> URC: 14. {success: true}
   deactivate RS

   URC --> FE: 15. 200 OK
   deactivate URC

   FE --> ADM: 16. "Roles asignados exitosamente"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Asignacion Masiva
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Admin selecciona multiples usuarios

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Admin selecciona checkbox de multiples usuarios
   * - 2
     - Clic en "Asignar Rol Masivo"
   * - 3
     - Selecciona rol(es) a asignar
   * - 4
     - Sistema asigna rol a todos los seleccionados
   * - 5
     - Muestra resumen: [N] asignados, [M] ya tenian rol

7.2 FA-2: Quitar Rol
^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario ya tiene rol asignado

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Admin hace clic en "X" junto al rol asignado
   * - 2
     - Sistema solicita confirmacion
   * - 3
     - Admin confirma
   * - 4
     - Sistema elimina registro de user_roles
   * - 5
     - Sistema invalida cache de permisos
   * - 6
     - Registra ROLE_UNASSIGNED

7.3 FA-3: Vigencia Temporal
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Admin define fechas de vigencia

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Admin activa "Vigencia temporal"
   * - 2
     - Define fecha desde y/o fecha hasta
   * - 3
     - Sistema guarda con valid_from y valid_until
   * - 4
     - Rol solo efectivo dentro del rango
   * - 5
     - Job nocturno desactiva roles vencidos

7.4 FA-4: Rol Ya Asignado
^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario ya tiene el rol

Sistema muestra mensaje informativo y omite rol duplicado.

----

8. Excepciones
--------------

8.1 EX-1: Usuario Inactivo
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No se pueden asignar roles a usuarios inactivos."

8.2 EX-2: Rol Inactivo
^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "El rol '[NAME]' esta inactivo y no puede asignarse."

8.3 EX-3: Sin Roles Disponibles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "El usuario ya tiene todos los roles disponibles asignados."

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-012 Asignar Rol
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Verificar permiso ROL-002;

   if (Tiene permiso?) then (si)
       :Cargar roles del usuario;
       :Cargar roles disponibles;

       if (Asignacion masiva?) then (si)
           :Seleccionar usuarios;
           :Seleccionar rol;
       else (individual)
           :Seleccionar rol(es);
       endif

       if (Vigencia temporal?) then (si)
           :Definir fechas;
       else (no)
       endif

       while (Hay roles por asignar?) is (si)
           if (Ya tiene rol?) then (si)
               :Omitir;
           else (no)
               :Crear user_roles;
           endif
       endwhile (no)

       :Invalidar cache permisos;
       #C8E6C9:ROLE_ASSIGNED;
       :Mostrar confirmacion;

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
     - ROLE_ASSIGNED, ROLE_UNASSIGNED registrados
   * - BR_028
     - Multi-Rol
     - Usuario puede tener multiples roles simultaneos
   * - BR_029
     - Vigencia Rol
     - Roles pueden tener fecha de expiracion

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-012.01
     - Verificar permiso ROL-002
   * - FR-012.02
     - Mostrar roles actuales del usuario
   * - FR-012.03
     - Mostrar roles disponibles para asignar
   * - FR-012.04
     - Permitir asignar multiples roles simultaneamente
   * - FR-012.05
     - Soportar asignacion masiva a multiples usuarios
   * - FR-012.06
     - Permitir definir vigencia temporal (desde/hasta)
   * - FR-012.07
     - Permitir quitar rol asignado
   * - FR-012.08
     - Invalidar cache de permisos inmediatamente
   * - FR-012.09
     - Registrar asignacion/remocion en auditoria

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-004
   * - **BR Aplicables**
     - BR_008, BR_028, BR_029
   * - **FR Derivados**
     - FR-012.01 a FR-012.09
   * - **UC Relacionados**
     - UC-010, UC-006 (Usuarios)
   * - **Funcion RBAC**
     - ROL-002

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
     - Version completa. Asignacion masiva. Vigencia temporal.
