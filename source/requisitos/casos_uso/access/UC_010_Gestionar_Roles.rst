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
UC-010: Gestionar Roles del Sistema
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
     - Gestionar Roles del Sistema
   * - **Actor Primario**
     - Administrador de Seguridad
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Alta
   * - **Prioridad**
     - Critica
   * - **BReq Origen**
     - BReq-004: Control de Acceso Basado en Roles

----

2. Descripcion
--------------

Permite gestionar el ciclo de vida completo de roles del sistema: crear
nuevos roles con descripcion y nivel jerarquico, modificar propiedades,
activar/desactivar roles y eliminar roles sin usuarios asignados.
Los roles son la base del modelo RBAC y agrupan funciones que se asignan
a usuarios. Implementa validaciones de integridad referencial y registra
todos los cambios en auditoria (BR_008).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-010 Gestionar Roles
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

   actor "Administrador\nSeguridad" as ADM
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Access" {
       usecase "UC-010:\nGestionar\nRoles" as UC010
       usecase "Crear\nRol" as CR
       usecase "Modificar\nRol" as MR
       usecase "Activar/\nDesactivar" as AD
       usecase "Eliminar\nRol" as ER
       usecase "Listar\nRoles" as LR
       usecase "Ver Usuarios\nAsignados" as VUA
       usecase "Clonar\nRol" as CLR
   }

   ADM --> UC010
   UC010 ..> CR : <<extends>>
   UC010 ..> MR : <<extends>>
   UC010 ..> AD : <<extends>>
   UC010 ..> ER : <<extends>>
   UC010 ..> LR : <<include>>
   UC010 ..> VUA : <<extends>>
   UC010 ..> CLR : <<extends>>
   UC010 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion ROL-001 (Gestionar Roles)
2. Sistema de roles inicializado con roles base

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Administracion > Roles" desde menu principal.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Operacion CRUD ejecutada exitosamente
2. Evento correspondiente registrado en auditoria (BR_008)
3. Cache de permisos invalidado si aplica

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Roles protegidos (ADMIN, SYSTEM) no pueden eliminarse
2. Roles con usuarios asignados no pueden eliminarse
3. Integridad referencial mantenida

----

5. Flujo Normal: Crear Rol
--------------------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a Gestion de Roles
     -
   * - 2
     -
     - Verifica permiso ROL-001
   * - 3
     -
     - Muestra lista de roles existentes
   * - 4
     - Hace clic en "Nuevo Rol"
     -
   * - 5
     -
     - Muestra formulario de creacion
   * - 6
     - Ingresa codigo unico del rol
     -
   * - 7
     - Ingresa nombre descriptivo
     -
   * - 8
     - Ingresa descripcion detallada
     -
   * - 9
     - Selecciona nivel jerarquico (1-10)
     -
   * - 10
     - Presiona "Guardar"
     -
   * - 11
     -
     - Valida unicidad de codigo
   * - 12
     -
     - Crea rol con status=ACTIVE
   * - 13
     -
     - Registra ROLE_CREATED (BR_008)
   * - 14
     -
     - Muestra confirmacion

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-010 Crear Rol
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin Seguridad" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "RoleController" as RC #E8F5E9
   participant "RoleService" as RS #E8F5E9
   participant "ValidationService" as VS #E8F5E9
   participant "CacheService" as CS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a Gestion Roles
   FE -> RC: 2. GET /api/roles
   activate RC

   RC -> DB: 3. SELECT * FROM roles\nORDER BY level, name
   DB --> RC: [roles]

   RC --> FE: 4. {roles, total}
   deactivate RC

   FE --> ADM: 5. Lista de roles

   ADM -> FE: 6. Clic "Nuevo Rol"
   FE --> ADM: 7. Formulario de creacion

   ADM -> FE: 8. Completa datos y guarda
   FE -> RC: 9. POST /api/roles\n{code, name, description, level}
   activate RC

   RC -> VS: 10. validateRole(data)
   activate VS
   VS -> DB: SELECT id FROM roles WHERE code = ?
   DB --> VS: [] (no existe)
   VS --> RC: {valid: true}
   deactivate VS

   RC -> RS: 11. createRole(data)
   activate RS

   RS -> DB: 12. INSERT INTO roles\n(code, name, description, level, status)\nVALUES (?, ?, ?, ?, 'ACTIVE')
   DB --> RS: {id: 15}

   RS -> CS: 13. invalidateRoleCache()
   CS --> RS: OK

   RS -> AUD: 14. logEvent('ROLE_CREATED',\n{roleId: 15, code, name})
   AUD -> DB: INSERT INTO audit_log
   AUD --> RS: OK

   RS --> RC: 15. {role: {...}}
   deactivate RS

   RC --> FE: 16. 201 Created {role}
   deactivate RC

   FE --> ADM: 17. "Rol creado exitosamente"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Modificar Rol Existente
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 4 del flujo normal

**Condicion:** Usuario selecciona rol y hace clic en "Editar"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 4.1
     - Sistema carga datos del rol en formulario
   * - 4.2
     - Usuario modifica campos permitidos (no codigo)
   * - 4.3
     - Sistema valida cambios
   * - 4.4
     - Sistema actualiza rol
   * - 4.5
     - Sistema registra ROLE_UPDATED
   * - 4.6
     - Si cambio nivel: invalida cache de permisos

**Retorno:** Paso 14

7.2 FA-2: Desactivar Rol
^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario hace clic en "Desactivar" en rol activo

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Sistema muestra advertencia de impacto
   * - 2
     - Sistema lista usuarios afectados
   * - 3
     - Usuario confirma desactivacion
   * - 4
     - Sistema cambia status a INACTIVE
   * - 5
     - Sistema registra ROLE_DEACTIVATED
   * - 6
     - Usuarios con rol pierden acceso inmediato

7.3 FA-3: Eliminar Rol
^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario hace clic en "Eliminar"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Sistema verifica rol no es protegido
   * - 2
     - Sistema verifica no hay usuarios asignados
   * - 3
     - Sistema verifica no hay funciones asignadas
   * - 4
     - Sistema solicita confirmacion con codigo
   * - 5
     - Usuario ingresa codigo de confirmacion
   * - 6
     - Sistema elimina rol
   * - 7
     - Sistema registra ROLE_DELETED

7.4 FA-4: Clonar Rol
^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario hace clic en "Clonar" en rol existente

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Sistema crea copia con codigo nuevo
   * - 2
     - Sistema copia todas las funciones asignadas
   * - 3
     - Usuario modifica propiedades del clon
   * - 4
     - Sistema guarda nuevo rol
   * - 5
     - Sistema registra ROLE_CLONED

7.5 FA-5: Ver Usuarios Asignados
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario hace clic en icono de usuarios

Sistema muestra lista paginada de usuarios con el rol.

----

8. Excepciones
--------------

8.1 EX-1: Codigo de Rol Duplicado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Codigo ya existe en la base de datos

**Mensaje:** "El codigo de rol '[CODE]' ya existe. Use un codigo unico."

**Codigo HTTP:** 409 Conflict

8.2 EX-2: Rol Protegido
^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Intento de eliminar/modificar rol ADMIN o SYSTEM

**Mensaje:** "El rol '[NAME]' es un rol protegido del sistema y no puede modificarse."

**Codigo HTTP:** 403 Forbidden

8.3 EX-3: Rol con Usuarios Asignados
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Intento de eliminar rol con usuarios

**Mensaje:** "No se puede eliminar el rol '[NAME]'. Tiene [N] usuarios asignados. Reasigne los usuarios primero."

**Codigo HTTP:** 409 Conflict

8.4 EX-4: Rol con Funciones Asignadas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Intento de eliminar rol con funciones

**Mensaje:** "No se puede eliminar el rol '[NAME]'. Tiene [N] funciones asignadas. Quite las funciones primero."

**Codigo HTTP:** 409 Conflict

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-010 Gestionar Roles
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

   :Accede a Gestion de Roles;
   :Verificar permiso ROL-001;

   if (Tiene permiso?) then (si)
       :Cargar lista de roles;
       :Mostrar tabla con acciones;

       switch (Accion seleccionada?)
       case (Crear)
           :Mostrar formulario vacio;
           :Usuario ingresa datos;
           :Validar unicidad codigo;

           if (Codigo unico?) then (si)
               :Crear rol (ACTIVE);
               #C8E6C9:ROLE_CREATED;
           else (no)
               #FFCDD2:Error: duplicado;
           endif

       case (Modificar)
           :Cargar datos del rol;

           if (Rol protegido?) then (si)
               #FFCDD2:Error: protegido;
           else (no)
               :Usuario modifica campos;
               :Validar cambios;
               :Actualizar rol;
               :Invalidar cache;
               #C8E6C9:ROLE_UPDATED;
           endif

       case (Desactivar)
           :Mostrar usuarios afectados;
           :Solicitar confirmacion;

           if (Confirma?) then (si)
               :Cambiar status = INACTIVE;
               #C8E6C9:ROLE_DEACTIVATED;
           else (no)
               :Cancelar;
           endif

       case (Eliminar)
           if (Rol protegido?) then (si)
               #FFCDD2:Error: protegido;
           elseif (Tiene usuarios?) then (si)
               #FFCDD2:Error: usuarios asignados;
           elseif (Tiene funciones?) then (si)
               #FFCDD2:Error: funciones asignadas;
           else (no)
               :Solicitar confirmacion;

               if (Confirma con codigo?) then (si)
                   :Eliminar rol;
                   #C8E6C9:ROLE_DELETED;
               else (no)
                   :Cancelar;
               endif
           endif

       case (Clonar)
           :Copiar rol y funciones;
           :Usuario modifica nuevo codigo;
           :Guardar clon;
           #C8E6C9:ROLE_CLONED;

       endswitch

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
     - Auditoria Completa
     - Eventos: ROLE_CREATED, ROLE_UPDATED, ROLE_DEACTIVATED, ROLE_DELETED, ROLE_CLONED
   * - BR_024
     - Roles Protegidos
     - ADMIN y SYSTEM no pueden eliminarse ni desactivarse
   * - BR_025
     - Integridad Rol
     - No eliminar roles con usuarios o funciones asignadas

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-010.01
     - Sistema DEBE verificar permiso ROL-001
   * - FR-010.02
     - Sistema DEBE listar roles con paginacion y busqueda
   * - FR-010.03
     - Sistema DEBE validar unicidad de codigo de rol
   * - FR-010.04
     - Sistema DEBE permitir crear rol con codigo, nombre, descripcion, nivel
   * - FR-010.05
     - Sistema DEBE permitir modificar propiedades (excepto codigo)
   * - FR-010.06
     - Sistema DEBE impedir modificar roles protegidos (ADMIN, SYSTEM)
   * - FR-010.07
     - Sistema DEBE permitir activar/desactivar roles
   * - FR-010.08
     - Sistema DEBE impedir eliminar roles con usuarios asignados
   * - FR-010.09
     - Sistema DEBE impedir eliminar roles con funciones asignadas
   * - FR-010.10
     - Sistema DEBE permitir clonar rol con sus funciones
   * - FR-010.11
     - Sistema DEBE mostrar usuarios asignados a cada rol
   * - FR-010.12
     - Sistema DEBE invalidar cache de permisos al modificar roles
   * - FR-010.13
     - Sistema DEBE registrar todas las operaciones en auditoria

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-004: Control de Acceso Basado en Roles
   * - **BR Aplicables**
     - BR_008, BR_024, BR_025
   * - **FR Derivados**
     - FR-010.01 a FR-010.13 (13 requerimientos)
   * - **UC Relacionados**
     - UC-011 (Funciones), UC-012 (Asignar Rol)
   * - **Actores RBAC**
     - AGR-001: admin_seguridad
   * - **Funciones RBAC**
     - ROL-001: Gestionar Roles

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
     - Version completa con PlantUML. Clonacion. Roles protegidos. Cache.
