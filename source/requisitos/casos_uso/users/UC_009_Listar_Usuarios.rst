.. meta::
   :artefacto: UC_009
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/users
   :modulo: MOD_Users
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-009:

==============================================================================
UC-009: Listar Usuarios
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
     - UC-009
   * - **Nombre**
     - Listar Usuarios
   * - **Actor Primario**
     - Administrador de Usuarios
   * - **Actores Secundarios**
     - Ninguno
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

Permite a un administrador visualizar la lista completa de usuarios del
sistema con paginacion, busqueda y filtros. Sirve como punto de entrada
para las operaciones de gestion de usuarios (crear, modificar, dar de baja).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-009 Listar Usuarios
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

   rectangle "MOD_Users" {
       usecase "UC-009:\nListar\nUsuarios" as UC009
       usecase "Buscar\nUsuario" as BU
       usecase "Filtrar por\nEstado" as FE
       usecase "Exportar\nLista" as EL
       usecase "UC-006:\nCrear" as UC006
       usecase "UC-007:\nModificar" as UC007
       usecase "UC-008:\nBaja" as UC008
   }

   ADM --> UC009
   UC009 ..> BU : <<include>>
   UC009 ..> FE : <<include>>
   UC009 ..> EL : <<extends>>
   UC009 .> UC006 : <<extends>>
   UC009 .> UC007 : <<extends>>
   UC009 .> UC008 : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene sesion activa
2. Administrador tiene funcion USR-004 (Consultar Usuarios)

4.2 Trigger
^^^^^^^^^^^

Administrador accede a "Gestion de Usuarios" en menu de administracion.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Lista de usuarios mostrada con paginacion
2. Filtros y busqueda aplicados si se especificaron

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Solo usuarios con permiso pueden ver la lista
2. Datos sensibles (password hash) nunca se exponen

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
     - Accede a "Gestion de Usuarios"
     -
   * - 2
     -
     - Verifica permiso USR-004
   * - 3
     -
     - Obtiene primera pagina de usuarios
   * - 4
     -
     - Muestra tabla paginada (20 por pagina)
   * - 5
     - Visualiza lista de usuarios
     -
   * - 6
     - (Opcional) Ingresa texto en busqueda
     -
   * - 7
     -
     - Filtra por username, nombre o email
   * - 8
     - (Opcional) Selecciona filtro de estado
     -
   * - 9
     -
     - Filtra por ACTIVO, INACTIVO o TODOS
   * - 10
     - (Opcional) Cambia de pagina
     -
   * - 11
     -
     - Carga pagina solicitada
   * - 12
     - (Opcional) Selecciona accion sobre usuario
     -
   * - 13
     -
     - Navega a UC correspondiente (006, 007 o 008)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-009 Listar Usuarios
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
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a "Gestion Usuarios"
   activate FE

   FE -> UC: 2. GET /api/users?page=1&limit=20
   activate UC

   UC -> RBAC: 3. checkPermission(adminId, 'USR-004')
   activate RBAC
   RBAC --> UC: authorized
   deactivate RBAC

   UC -> US: 4. getUsers(page=1, limit=20)
   activate US

   US -> DB: 5. SELECT id, username, email,\nnombre, apellido, status, created_at\nFROM users\nORDER BY created_at DESC\nLIMIT 20 OFFSET 0
   DB --> US: [users]

   US -> DB: 6. SELECT COUNT(*) FROM users
   DB --> US: {total: 150}

   US --> UC: 7. {users, total, page, pages}
   deactivate US

   UC --> FE: 8. 200 OK {users, pagination}
   deactivate UC

   FE --> ADM: 9. Muestra tabla con usuarios
   note right: Columnas: Username, Nombre,\nEmail, Estado, Fecha, Acciones

   == Busqueda ==

   ADM -> FE: 10. Ingresa "juan" en busqueda
   FE -> FE: 11. Debounce 300ms

   FE -> UC: 12. GET /api/users?search=juan&page=1
   activate UC

   UC -> US: 13. searchUsers("juan")
   activate US

   US -> DB: 14. SELECT * FROM users\nWHERE username ILIKE '%juan%'\nOR nombre ILIKE '%juan%'\nOR email ILIKE '%juan%'
   DB --> US: [filteredUsers]

   US --> UC: 15. {users, total}
   deactivate US

   UC --> FE: 16. 200 OK {users}
   deactivate UC

   FE --> ADM: 17. Actualiza tabla con resultados

   == Filtro Estado ==

   ADM -> FE: 18. Selecciona filtro "INACTIVO"

   FE -> UC: 19. GET /api/users?status=INACTIVO
   activate UC

   UC -> US: 20. getUsers(status='INACTIVO')
   US -> DB: SELECT * FROM users\nWHERE status = 'INACTIVO'
   DB --> US: [inactiveUsers]

   UC --> FE: 21. 200 OK {users}
   deactivate UC

   FE --> ADM: 22. Muestra solo usuarios inactivos
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Sin Resultados de Busqueda
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 7 del flujo normal

**Condicion:** Busqueda no encuentra coincidencias

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 7.1
     - Sistema retorna lista vacia
   * - 7.2
     - Sistema muestra "No se encontraron usuarios"
   * - 7.3
     - Muestra boton "Limpiar filtros"

**Retorno:** Paso 5 (al limpiar filtros)

7.2 FA-2: Exportar Lista
^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 5 del flujo normal

**Condicion:** Admin hace clic en "Exportar"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 5.1
     - Sistema muestra opciones: CSV, Excel
   * - 5.2
     - Admin selecciona formato
   * - 5.3
     - Sistema genera archivo con usuarios filtrados
   * - 5.4
     - Sistema descarga archivo

**Retorno:** Paso 5 del flujo normal

7.3 FA-3: Ordenar por Columna
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 5 del flujo normal

**Condicion:** Admin hace clic en header de columna

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 5.1
     - Sistema ordena por columna seleccionada
   * - 5.2
     - Clic adicional invierte orden (ASC/DESC)
   * - 5.3
     - Sistema actualiza tabla

**Retorno:** Paso 5 del flujo normal

----

8. Excepciones
--------------

8.1 EX-1: Sin Permiso de Consulta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario no tiene funcion USR-004

**Accion del Sistema:** Retorna 403 Forbidden

**Mensaje al Usuario:** "No tiene permisos para consultar usuarios"

8.2 EX-2: Error de Conexion
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** No se puede conectar a BD

**Accion del Sistema:** Muestra error y opcion de reintentar

**Mensaje al Usuario:** "Error al cargar usuarios. Reintentar"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-009 Listar Usuarios
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

   :Admin accede a\n"Gestion de Usuarios";

   :Verificar permiso USR-004;

   if (Tiene permiso?) then (si)

       :Obtener usuarios (pagina 1);
       :Mostrar tabla paginada;

       while (Admin interactua?) is (si)

           split
               :Buscar por texto;
               :Filtrar resultados;
           split again
               :Filtrar por estado;
               :Aplicar filtro;
           split again
               :Cambiar pagina;
               :Cargar nueva pagina;
           split again
               :Ordenar por columna;
               :Reordenar resultados;
           split again
               :Exportar lista;
               :Generar archivo;
               :Descargar;
           split again
               :Seleccionar usuario;

               if (Accion?) then (Crear)
                   :Ir a UC-006;
                   stop
               elseif (Editar) then
                   :Ir a UC-007;
                   stop
               elseif (Baja) then
                   :Ir a UC-008;
                   stop
               else (Ver detalle)
                   :Mostrar modal detalle;
               endif
           end split

           :Actualizar vista;

       endwhile (no)

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
   * - --
     - --
     - Este UC no aplica BR especificas (solo consulta)

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-009.01
     - Sistema DEBE verificar permiso USR-004 antes de mostrar lista
   * - FR-009.02
     - Sistema DEBE mostrar tabla con: username, nombre, email, estado, fecha
   * - FR-009.03
     - Sistema DEBE paginar resultados (20 por pagina)
   * - FR-009.04
     - Sistema DEBE permitir busqueda por username, nombre, email
   * - FR-009.05
     - Sistema DEBE permitir filtro por estado (ACTIVO/INACTIVO/TODOS)
   * - FR-009.06
     - Sistema DEBE permitir ordenar por cualquier columna
   * - FR-009.07
     - Sistema DEBE mostrar botones de accion: Editar, Dar de Baja
   * - FR-009.08
     - Sistema DEBE permitir exportar a CSV y Excel
   * - FR-009.09
     - Sistema DEBE mostrar total de usuarios y paginas

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - Ninguna especifica
   * - **FR Derivados**
     - FR-009.01 a FR-009.09 (9 requerimientos)
   * - **UC Relacionados**
     - UC-006 (Crear), UC-007 (Modificar), UC-008 (Baja)
   * - **Actores RBAC**
     - AGR-007: admin_usuarios
   * - **Funciones RBAC**
     - USR-004: Consultar Usuarios

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
