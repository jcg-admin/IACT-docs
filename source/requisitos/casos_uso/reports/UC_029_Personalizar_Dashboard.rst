.. meta::
   :artefacto: UC_029
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-029:

==============================================================================
UC-029: Personalizar Dashboard
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
     - UC-029
   * - **Nombre**
     - Personalizar Dashboard
   * - **Actor Primario**
     - Usuario autenticado
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Reports
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Baja
   * - **BReq Origen**
     - BReq-003: Visualizacion de Indicadores

----

2. Descripcion
--------------

Permite a los usuarios personalizar su dashboard seleccionando widgets,
ordenando su disposicion, configurando preferencias de visualizacion
y guardando la configuracion para futuras sesiones.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-029 Personalizar Dashboard
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

   actor "Usuario" as USR

   rectangle "MOD_Reports" {
       usecase "UC-029:\nPersonalizar\nDashboard" as UC029
       usecase "Agregar\nWidgets" as AW
       usecase "Reordenar\nWidgets" as RW
       usecase "Configurar\nWidget" as CW
       usecase "Guardar\nLayout" as GL
       usecase "Restaurar\nDefault" as RD
   }

   USR --> UC029
   UC029 ..> AW : <<include>>
   UC029 ..> RW : <<include>>
   UC029 ..> CW : <<extends>>
   UC029 ..> GL : <<include>>
   UC029 ..> RD : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion DSH-004 (Personalizar Dashboard)
2. Usuario autenticado con sesion activa

4.2 Trigger
^^^^^^^^^^^

Usuario hace clic en "Personalizar" en cualquier dashboard.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Layout personalizado guardado
2. Dashboard muestra configuracion del usuario
3. Evento DASHBOARD_CUSTOMIZED registrado

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
     - Hace clic en "Personalizar"
     -
   * - 2
     -
     - Verifica permiso DSH-004
   * - 3
     -
     - Carga layout actual del usuario
   * - 4
     -
     - Activa modo edicion
   * - 5
     -
     - Muestra catalogo de widgets disponibles
   * - 6
     - Arrastra widget al dashboard
     -
   * - 7
     -
     - Agrega widget en posicion
   * - 8
     - Reordena widgets (drag & drop)
     -
   * - 9
     -
     - Actualiza posiciones
   * - 10
     - (Opcional) Configura widget
     -
   * - 11
     - Hace clic en "Guardar"
     -
   * - 12
     -
     - Guarda configuracion en BD
   * - 13
     -
     - Registra en auditoria
   * - 14
     -
     - Desactiva modo edicion

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-029 Personalizar Dashboard
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   actor "Usuario" as U
   participant "Frontend" as FE #E3F2FD
   participant "DashboardController" as DC #E8F5E9
   participant "LayoutService" as LS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Clic "Personalizar"
   FE -> DC: 2. GET /api/dashboard/customize
   activate DC

   DC -> LS: 3. getUserLayout(userId)
   LS -> DB: SELECT * FROM user_layouts
   LS --> DC: {currentLayout}

   DC -> LS: 4. getAvailableWidgets()
   LS --> DC: [widgets]

   DC --> FE: 5. {layout, widgets}
   deactivate DC

   FE --> U: 6. Modo edicion activo

   U -> FE: 7. Arrastra widgets
   U -> FE: 8. Reordena posiciones
   U -> FE: 9. Configura opciones

   U -> FE: 10. Clic "Guardar"
   FE -> DC: 11. PUT /api/dashboard/layout\n{widgets, positions, config}
   activate DC

   DC -> LS: 12. saveLayout(userId, layout)
   activate LS
   LS -> DB: 13. UPSERT user_layouts
   LS --> DC: OK
   deactivate LS

   DC -> AUD: 14. logEvent(DASHBOARD_CUSTOMIZED)
   AUD -> DB: INSERT audit_log

   DC --> FE: 15. 200 OK
   deactivate DC

   FE --> U: 16. "Configuracion guardada"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Restaurar Default
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario hace clic en "Restaurar Default"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 7.1.1
     - Sistema solicita confirmacion
   * - 7.1.2
     - Usuario confirma
   * - 7.1.3
     - Sistema elimina layout personalizado
   * - 7.1.4
     - Sistema carga layout por defecto

7.2 FA-2: Quitar Widget
^^^^^^^^^^^^^^^^^^^^^^^

Usuario arrastra widget fuera del area o hace clic en "X".

----

8. Excepciones
--------------

8.1 EX-1: Widget No Disponible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario no tiene permiso para widget especifico

**Accion:** Widget aparece deshabilitado con tooltip explicativo

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-029 Personalizar Dashboard
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Clic "Personalizar";
   :Verificar permiso DSH-004;
   :Cargar layout actual;
   :Activar modo edicion;
   :Mostrar catalogo widgets;

   while (Editando?) is (si)
       split
           :Agregar widget;
       split again
           :Quitar widget;
       split again
           :Reordenar (drag & drop);
       split again
           :Configurar widget;
       end split
   endwhile (Guardar)

   if (Restaurar default?) then (si)
       :Eliminar layout usuario;
       :Cargar layout default;
   else (no)
       :Guardar layout personalizado;
   endif

   #C8E6C9:Registrar auditoria;
   :Desactivar modo edicion;
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
     - Aplicacion
   * - BR_008
     - Auditoria
     - Cambios de personalizacion registrados
   * - BR_019
     - Widgets Permitidos
     - Solo widgets para los que tiene permiso

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-029.01
     - Verificar permiso DSH-004
   * - FR-029.02
     - Cargar layout guardado del usuario
   * - FR-029.03
     - Mostrar catalogo de widgets disponibles
   * - FR-029.04
     - Permitir agregar widgets (drag & drop)
   * - FR-029.05
     - Permitir quitar widgets
   * - FR-029.06
     - Permitir reordenar widgets
   * - FR-029.07
     - Permitir configurar opciones de widget
   * - FR-029.08
     - Guardar layout en BD
   * - FR-029.09
     - Permitir restaurar layout default

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-003
   * - **BR Aplicables**
     - BR_008, BR_019
   * - **FR Derivados**
     - FR-029.01 a FR-029.09
   * - **Funcion RBAC**
     - DSH-004

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
     - Version con PlantUML embebido. 3 diagramas.
