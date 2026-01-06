.. meta::
   :artefacto: UC_044
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-044:

==============================================================================
UC-044: Consultar Permisos Efectivos
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
     - UC-044
   * - **Nombre**
     - Consultar Permisos Efectivos
   * - **Actor Primario**
     - Administrador de Seguridad / Usuario
   * - **Actores Secundarios**
     - Ninguno
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

Permite consultar los permisos efectivos de un usuario: funciones asignadas,
segmentos de datos accesibles, y agrupadores a los que pertenece. Util para
auditorias y verificacion de accesos.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-044 Consultar Permisos
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
   actor "Usuario" as USR

   rectangle "MOD_Access" {
       usecase "UC-044:\nConsultar\nPermisos" as UC044
       usecase "Ver\nFunciones" as VF
       usecase "Ver\nSegmentos" as VS
       usecase "Ver\nAgrupadores" as VA
       usecase "Exportar\nReporte" as ER
   }

   ADM --> UC044
   USR --> UC044 : propios
   UC044 ..> VF : <<include>>
   UC044 ..> VS : <<include>>
   UC044 ..> VA : <<include>>
   UC044 ..> ER : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario autenticado
2. Si consulta otro usuario: requiere ACC-006 (Consultar Permisos)
3. Puede consultar sus propios permisos sin permiso especial

4.2 Trigger
^^^^^^^^^^^

- Admin: Selecciona "Ver Permisos" en perfil de usuario
- Usuario: Accede a "Mis Permisos" en menu

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Permisos efectivos mostrados en pantalla

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
     - Solicita ver permisos
     -
   * - 2
     -
     - Obtiene funciones del usuario
   * - 3
     -
     - Obtiene segmentos del usuario
   * - 4
     -
     - Obtiene agrupadores del usuario
   * - 5
     -
     - Muestra vista consolidada

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-044 Consultar Permisos
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin/Usuario" as U
   participant "Frontend" as FE #E3F2FD
   participant "AccessController" as AC #E8F5E9
   participant "RBACService" as RBAC #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Ver permisos de {userId}
   FE -> AC: 2. GET /api/users/{userId}/permissions
   activate AC

   AC -> RBAC: 3. getEffectivePermissions(userId)
   activate RBAC

   RBAC -> DB: 4. SELECT funciones
   DB --> RBAC: [functions]

   RBAC -> DB: 5. SELECT segmentos
   DB --> RBAC: [segments]

   RBAC -> DB: 6. SELECT agrupadores
   DB --> RBAC: [groups]

   RBAC --> AC: 7. {functions, segments, groups}
   deactivate RBAC

   AC --> FE: 8. 200 OK {permissions}
   deactivate AC

   FE --> U: 9. Vista consolidada de permisos
   note right: Tabs: Funciones,\nSegmentos, Agrupadores
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Exportar a PDF
^^^^^^^^^^^^^^^^^^^^^^^^

Admin puede exportar reporte de permisos para auditoria externa.

----

8. Excepciones
--------------

8.1 EX-1: Sin Permiso para Ver Otros
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "Solo puede consultar sus propios permisos"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-044 Consultar Permisos
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Solicita ver permisos;

   if (Es propio usuario?) then (si)
       :Permitir consulta;
   else (no)
       if (Tiene ACC-006?) then (si)
           :Permitir consulta;
       else (no)
           #FFCDD2:403 Forbidden;
           stop
       endif
   endif

   :Obtener funciones;
   :Obtener segmentos;
   :Obtener agrupadores;
   :Mostrar vista consolidada;

   if (Exportar?) then (si)
       :Generar PDF;
   else (no)
   endif

   stop
   @enduml

----

10. Reglas de Negocio
---------------------

No aplica BR especificas (solo consulta).

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-044.01
     - Permitir consulta propia sin permiso especial
   * - FR-044.02
     - Requerir ACC-006 para consultar otros
   * - FR-044.03
     - Mostrar funciones asignadas
   * - FR-044.04
     - Mostrar segmentos asignados
   * - FR-044.05
     - Mostrar agrupadores del usuario
   * - FR-044.06
     - Permitir exportar a PDF

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-004
   * - **FR Derivados**
     - FR-044.01 a FR-044.06
   * - **Funcion RBAC**
     - ACC-006: Consultar Permisos

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
     - Version con PlantUML (Sphinx)