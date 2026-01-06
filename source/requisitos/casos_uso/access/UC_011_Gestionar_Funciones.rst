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
UC-011: Gestionar Funciones del Sistema
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
     - Gestionar Funciones del Sistema
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

Permite gestionar las funciones (permisos granulares) del sistema: crear
nuevas funciones asociadas a modulos, modificar propiedades, activar/
desactivar y eliminar funciones no asignadas. Las funciones representan
acciones atomicas que se agrupan en roles para control de acceso.
Cada funcion tiene un codigo unico con prefijo de modulo (ej: USR-001).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-011 Gestionar Funciones
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
       usecase "UC-011:\nGestionar\nFunciones" as UC011
       usecase "Crear\nFuncion" as CF
       usecase "Modificar\nFuncion" as MF
       usecase "Activar/\nDesactivar" as AD
       usecase "Eliminar\nFuncion" as EF
       usecase "Listar por\nModulo" as LM
       usecase "Ver Roles\nAsignados" as VRA
   }

   ADM --> UC011
   UC011 ..> CF : <<extends>>
   UC011 ..> MF : <<extends>>
   UC011 ..> AD : <<extends>>
   UC011 ..> EF : <<extends>>
   UC011 ..> LM : <<include>>
   UC011 ..> VRA : <<extends>>
   UC011 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion FUN-001 (Gestionar Funciones)
2. Existen modulos registrados en el sistema

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Administracion > Funciones" desde menu.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Operacion CRUD ejecutada exitosamente
2. Evento registrado en auditoria (BR_008)
3. Cache de permisos invalidado si aplica

----

5. Flujo Normal: Crear Funcion
------------------------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a Gestion de Funciones
     -
   * - 2
     -
     - Verifica permiso FUN-001
   * - 3
     -
     - Muestra lista agrupada por modulo
   * - 4
     - Hace clic en "Nueva Funcion"
     -
   * - 5
     -
     - Muestra formulario
   * - 6
     - Selecciona modulo destino
     -
   * - 7
     -
     - Genera codigo sugerido (MOD-XXX)
   * - 8
     - Ingresa nombre descriptivo
     -
   * - 9
     - Ingresa descripcion de la accion
     -
   * - 10
     - Selecciona tipo (READ/WRITE/DELETE/ADMIN)
     -
   * - 11
     - Presiona "Guardar"
     -
   * - 12
     -
     - Valida unicidad de codigo
   * - 13
     -
     - Crea funcion con status=ACTIVE
   * - 14
     -
     - Registra FUNCTION_CREATED (BR_008)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-011 Crear Funcion
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "FunctionController" as FC #E8F5E9
   participant "FunctionService" as FS #E8F5E9
   participant "CacheService" as CS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a Funciones
   FE -> FC: 2. GET /api/functions?groupBy=module
   activate FC

   FC -> DB: 3. SELECT f.*, m.name as module_name\nFROM functions f\nJOIN modules m ON f.module_id = m.id\nORDER BY m.name, f.code
   DB --> FC: [functions]

   FC --> FE: 4. {functionsByModule}
   deactivate FC

   FE --> ADM: 5. Lista agrupada por modulo

   ADM -> FE: 6. Clic "Nueva Funcion"
   FE -> FC: 7. GET /api/modules
   FC --> FE: [modules]
   FE --> ADM: 8. Formulario con selector modulo

   ADM -> FE: 9. Selecciona modulo "USR"
   FE -> FC: 10. GET /api/functions/next-code/USR
   FC -> DB: SELECT MAX(CAST(SUBSTRING(code, 5) AS INT))\nFROM functions WHERE code LIKE 'USR-%'
   FC --> FE: 11. {nextCode: 'USR-005'}

   ADM -> FE: 12. Completa datos y guarda
   FE -> FC: 13. POST /api/functions\n{code, name, description, type, moduleId}
   activate FC

   FC -> FS: 14. createFunction(data)
   activate FS

   FS -> DB: 15. SELECT id FROM functions WHERE code = ?
   DB --> FS: [] (no existe)

   FS -> DB: 16. INSERT INTO functions\n(code, name, description, type, module_id, status)
   DB --> FS: {id: 25}

   FS -> CS: 17. invalidateFunctionCache()

   FS -> AUD: 18. logEvent('FUNCTION_CREATED',\n{functionId, code, module})
   AUD -> DB: INSERT audit_log

   FS --> FC: 19. {function}
   deactivate FS

   FC --> FE: 20. 201 Created
   deactivate FC

   FE --> ADM: 21. "Funcion creada exitosamente"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Modificar Funcion
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario hace clic en "Editar"

Sistema permite modificar nombre, descripcion y tipo. Codigo no editable.

7.2 FA-2: Desactivar Funcion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Funcion activa

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Sistema muestra roles afectados
   * - 2
     - Usuario confirma desactivacion
   * - 3
     - Sistema cambia status = INACTIVE
   * - 4
     - Usuarios con roles que tenian esta funcion pierden permiso

7.3 FA-3: Eliminar Funcion
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Funcion sin roles asignados

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Sistema verifica no hay roles asignados
   * - 2
     - Sistema solicita confirmacion
   * - 3
     - Sistema elimina funcion
   * - 4
     - Registra FUNCTION_DELETED

7.4 FA-4: Ver Roles que Usan Funcion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario hace clic en icono de roles

Sistema muestra lista de roles que tienen asignada la funcion.

7.5 FA-5: Buscar Funciones
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario usa buscador

Sistema filtra por codigo, nombre o modulo en tiempo real.

----

8. Excepciones
--------------

8.1 EX-1: Codigo Duplicado
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "El codigo '[CODE]' ya existe. Use un codigo diferente."

8.2 EX-2: Funcion con Roles Asignados
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Intento de eliminar funcion asignada a roles

**Mensaje:** "No se puede eliminar. La funcion esta asignada a [N] roles."

8.3 EX-3: Funcion del Sistema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Intento de eliminar funcion critica del sistema

**Mensaje:** "Esta funcion es critica del sistema y no puede eliminarse."

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-011 Gestionar Funciones
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Verificar permiso FUN-001;

   if (Tiene permiso?) then (si)
       :Cargar funciones por modulo;

       switch (Accion?)
       case (Crear)
           :Seleccionar modulo;
           :Generar codigo sugerido;
           :Ingresar datos;
           :Validar unicidad;

           if (Codigo unico?) then (si)
               :Crear funcion;
               #C8E6C9:FUNCTION_CREATED;
           else (no)
               #FFCDD2:Error duplicado;
           endif

       case (Modificar)
           :Cargar funcion;
           :Modificar campos;
           :Actualizar;
           #C8E6C9:FUNCTION_UPDATED;

       case (Desactivar)
           :Mostrar roles afectados;
           if (Confirma?) then (si)
               :status = INACTIVE;
               :Invalidar cache;
               #C8E6C9:FUNCTION_DEACTIVATED;
           else (no)
           endif

       case (Eliminar)
           if (Tiene roles?) then (si)
               #FFCDD2:Error: roles asignados;
           elseif (Es critica?) then (si)
               #FFCDD2:Error: funcion critica;
           else (no)
               :Eliminar funcion;
               #C8E6C9:FUNCTION_DELETED;
           endif
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
     - Aplicacion
   * - BR_008
     - Auditoria
     - Todas las operaciones registradas
   * - BR_026
     - Codigo Funcion
     - Formato: MODULO-NNN (ej: USR-001)
   * - BR_027
     - Funciones Criticas
     - Funciones del sistema no eliminables

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-011.01
     - Verificar permiso FUN-001
   * - FR-011.02
     - Listar funciones agrupadas por modulo
   * - FR-011.03
     - Generar codigo secuencial por modulo
   * - FR-011.04
     - Validar unicidad de codigo
   * - FR-011.05
     - Crear funcion con codigo, nombre, descripcion, tipo
   * - FR-011.06
     - Clasificar por tipo: READ, WRITE, DELETE, ADMIN
   * - FR-011.07
     - Permitir activar/desactivar funciones
   * - FR-011.08
     - Impedir eliminar funciones con roles
   * - FR-011.09
     - Impedir eliminar funciones criticas
   * - FR-011.10
     - Mostrar roles que usan cada funcion
   * - FR-011.11
     - Invalidar cache al modificar

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-004
   * - **BR Aplicables**
     - BR_008, BR_026, BR_027
   * - **FR Derivados**
     - FR-011.01 a FR-011.11
   * - **UC Relacionados**
     - UC-010 (Roles), UC-013 (Asignar Funciones)
   * - **Funcion RBAC**
     - FUN-001

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
     - Version completa con PlantUML. Tipos de funcion. Funciones criticas.
