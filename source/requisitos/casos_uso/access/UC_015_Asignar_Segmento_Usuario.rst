.. meta::
   :artefacto: UC_015
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-015:

==============================================================================
UC-015: Asignar Segmento a Usuario
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
     - UC-015
   * - **Nombre**
     - Asignar Segmento a Usuario
   * - **Actor Primario**
     - Administrador de Datos
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Critica
   * - **BReq Origen**
     - BReq-005: Segmentacion de Datos

----

2. Descripcion
--------------

Permite asignar segmentos de datos a usuarios, controlando que informacion
contable puede ver cada usuario segun BR_009. Un usuario puede tener
multiples segmentos asignados. Soporta herencia jerarquica: asignar
un segmento padre incluye automaticamente acceso a sus hijos.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-015 Asignar Segmento
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

   actor "Administrador\nDatos" as ADM
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Access" {
       usecase "UC-015:\nAsignar Segmento\na Usuario" as UC015
       usecase "Asignar\nIndividual" as AI
       usecase "Asignar\nMasivo" as AM
       usecase "Herencia\nJerarquica" as HJ
       usecase "Quitar\nSegmento" as QS
       usecase "Ver Segmentos\nEfectivos" as VSE
   }

   ADM --> UC015
   UC015 ..> AI : <<extends>>
   UC015 ..> AM : <<extends>>
   UC015 ..> HJ : <<include>>
   UC015 ..> QS : <<extends>>
   UC015 ..> VSE : <<include>>
   UC015 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion SEG-002 (Asignar Segmentos)
2. Usuario destino existe y esta activo
3. Segmento(s) a asignar existen y estan activos

4.2 Trigger
^^^^^^^^^^^

- Desde gestion de usuarios: "Asignar Segmentos"
- Desde gestion de segmentos: "Asignar a Usuarios"

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Relacion usuario-segmento creada en user_segments
2. Usuario puede ver datos de segmentos asignados
3. Herencia aplicada para segmentos hijos
4. Evento SEGMENT_ASSIGNED registrado (BR_008)

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
     - Selecciona usuario
     -
   * - 2
     -
     - Verifica permiso SEG-002
   * - 3
     -
     - Muestra segmentos actuales del usuario
   * - 4
     -
     - Muestra arbol de segmentos disponibles
   * - 5
     - Marca segmentos a asignar
     -
   * - 6
     -
     - Muestra preview de acceso efectivo (con herencia)
   * - 7
     - Presiona "Asignar"
     -
   * - 8
     -
     - Crea registros en user_segments
   * - 9
     -
     - Invalida cache de segmentos usuario
   * - 10
     -
     - Registra SEGMENT_ASSIGNED
   * - 11
     -
     - Muestra confirmacion

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-015 Asignar Segmento a Usuario
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "UserSegmentController" as USC #E8F5E9
   participant "SegmentService" as SS #E8F5E9
   participant "CacheService" as CS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Selecciona usuario
   FE -> USC: 2. GET /api/users/{id}/segments
   activate USC

   USC -> DB: 3. SELECT s.* FROM segments s\nJOIN user_segments us ON s.id = us.segment_id\nWHERE us.user_id = ?
   DB --> USC: [assignedSegments]

   USC -> DB: 4. SELECT * FROM segments\nWHERE status = 'ACTIVE'
   DB --> USC: [allSegments]

   USC --> FE: 5. {assigned, tree}
   deactivate USC

   FE --> ADM: 6. Arbol con checkboxes

   ADM -> FE: 7. Marca segmentos
   FE -> FE: 8. Calcular acceso efectivo
   note right
       Si marca "Region Norte":
       - CC-001 (heredado)
       - CC-002 (heredado)
       - CC-003 (heredado)
   end note
   FE --> ADM: 9. Preview de acceso

   ADM -> FE: 10. Confirmar asignacion
   FE -> USC: 11. POST /api/users/{id}/segments\n{segmentIds: [1, 5, 8]}
   activate USC

   USC -> SS: 12. assignSegments(userId, segmentIds)
   activate SS

   SS -> DB: 13. DELETE FROM user_segments\nWHERE user_id = ?
   note right: Reemplaza asignacion completa

   loop Para cada segmento
       SS -> DB: 14. INSERT INTO user_segments\n(user_id, segment_id, inherited)
   end

   SS -> SS: 15. calculateEffectiveSegments()
   note right
       Expande herencia:
       segment + todos sus hijos
   end note

   SS -> CS: 16. invalidateUserSegments(userId)
   CS --> SS: OK

   SS -> AUD: 17. logEvent('SEGMENT_ASSIGNED',\n{userId, segments, effective})
   AUD -> DB: INSERT audit_log

   SS --> USC: 18. {assigned, effective}
   deactivate SS

   USC --> FE: 19. 200 OK
   deactivate USC

   FE --> ADM: 20. "Segmentos asignados.\nAcceso efectivo a [N] segmentos."
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
     - Admin selecciona multiples usuarios
   * - 2
     - Clic en "Asignar Segmentos"
   * - 3
     - Selecciona segmentos a asignar
   * - 4
     - Selecciona modo: agregar o reemplazar
   * - 5
     - Sistema aplica a todos los seleccionados

7.2 FA-2: Quitar Segmento
^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario tiene segmento asignado

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Admin desmarca segmento
   * - 2
     - Sistema muestra datos que dejara de ver
   * - 3
     - Admin confirma
   * - 4
     - Sistema elimina asignacion
   * - 5
     - Registra SEGMENT_UNASSIGNED

7.3 FA-3: Sin Segmentos
^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario sin ningun segmento asignado

Sistema muestra advertencia: usuario no vera datos en reportes.

----

8. Excepciones
--------------

8.1 EX-1: Usuario Inactivo
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No se pueden asignar segmentos a usuarios inactivos."

8.2 EX-2: Segmento Inactivo
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "El segmento '[NAME]' esta inactivo y no puede asignarse."

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-015 Asignar Segmento
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Verificar permiso SEG-002;

   if (Tiene permiso?) then (si)
       :Cargar segmentos usuario;
       :Mostrar arbol con checkboxes;

       if (Asignacion masiva?) then (si)
           :Seleccionar usuarios;
           :Seleccionar modo (agregar/reemplazar);
       else (individual)
       endif

       :Usuario marca segmentos;
       :Calcular acceso efectivo (herencia);
       :Mostrar preview;

       if (Confirma?) then (si)
           if (Modo reemplazar?) then (si)
               :Eliminar asignaciones previas;
           else (agregar)
           endif

           :Crear nuevas asignaciones;
           :Expandir herencia;
           :Invalidar cache;
           #C8E6C9:SEGMENT_ASSIGNED;

           if (Sin segmentos?) then (si)
               #FFE0B2:Advertencia: sin acceso a datos;
           else (no)
           endif
       else (no)
           :Cancelar;
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
     - SEGMENT_ASSIGNED, SEGMENT
cat >> /mnt/user-data/outputs/casos_uso_v2/access/UC_015_Asignar_Segmento_Usuario.rst << 'EOF'
_UNASSIGNED registrados
   * - BR_009
     - Segmentacion
     - Usuario ve solo datos de segmentos asignados
   * - BR_032
     - Herencia Segmentos
     - Asignar padre incluye acceso a hijos

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-015.01
     - Verificar permiso SEG-002
   * - FR-015.02
     - Mostrar segmentos actuales del usuario
   * - FR-015.03
     - Mostrar arbol de segmentos disponibles
   * - FR-015.04
     - Permitir seleccion multiple de segmentos
   * - FR-015.05
     - Calcular y mostrar acceso efectivo (herencia)
   * - FR-015.06
     - Soportar asignacion masiva a multiples usuarios
   * - FR-015.07
     - Permitir modo agregar o reemplazar
   * - FR-015.08
     - Permitir quitar segmentos asignados
   * - FR-015.09
     - Advertir si usuario queda sin segmentos
   * - FR-015.10
     - Invalidar cache de segmentos inmediatamente
   * - FR-015.11
     - Registrar asignacion/remocion en auditoria

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-005
   * - **BR Aplicables**
     - BR_008, BR_009, BR_032
   * - **FR Derivados**
     - FR-015.01 a FR-015.11
   * - **UC Relacionados**
     - UC-014 (Segmentos), UC-006 (Usuarios)
   * - **Funcion RBAC**
     - SEG-002

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
     - Version completa. Herencia. Acceso efectivo. Masivo.
