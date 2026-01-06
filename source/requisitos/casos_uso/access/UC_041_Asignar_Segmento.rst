.. meta::
   :artefacto: UC_041
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-041:

==============================================================================
UC-041: Asignar Segmento de Datos
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
     - UC-041
   * - **Nombre**
     - Asignar Segmento de Datos
   * - **Actor Primario**
     - Administrador de Seguridad
   * - **Actores Secundarios**
     - Sistema de Auditoria
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

Permite asignar segmentos de datos (centros de costo) a un usuario, definiendo
que datos puede visualizar en reportes y dashboards. Un usuario solo ve datos
de los centros asignados. Implementa control de acceso a nivel de datos (BR_009).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-041 Asignar Segmento
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

   actor "Administrador\nSeguridad" as ADM
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Access" {
       usecase "UC-041:\nAsignar\nSegmento" as UC041
       usecase "Buscar\nUsuario" as BU
       usecase "Seleccionar\nCentros" as SC
       usecase "Registrar\nEvento" as REG
   }

   ADM --> UC041
   UC041 ..> BU : <<include>>
   UC041 ..> SC : <<include>>
   UC041 ..> REG : <<include>>
   UC041 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene sesion activa
2. Administrador tiene funcion ACC-003 (Asignar Segmentos)
3. Usuario destino existe y esta ACTIVO
4. Catalogo de centros de costo disponible

4.2 Trigger
^^^^^^^^^^^

Administrador selecciona "Asignar Segmentos" desde perfil de usuario.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Centros asignados en tabla user_segments
2. Evento SEGMENTS_ASSIGNED registrado (BR_008)
3. Usuario puede ver datos de centros asignados

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Sin segmentos = sin acceso a datos (por defecto)
2. Asignacion "TODOS" permite ver todos los centros

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
     - Accede a segmentos del usuario
     -
   * - 2
     -
     - Verifica permiso ACC-003
   * - 3
     -
     - Muestra segmentos actuales del usuario
   * - 4
     -
     - Muestra catalogo de centros disponibles
   * - 5
     - Selecciona centros a asignar
     -
   * - 6
     - Presiona "Asignar Segmentos"
     -
   * - 7
     -
     - Inserta en user_segments
   * - 8
     -
     - Registra SEGMENTS_ASSIGNED en auditoria
   * - 9
     -
     - Muestra mensaje de exito

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-041 Asignar Segmento
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

   actor "Admin\nSeguridad" as ADM
   participant "Frontend\n(React)" as FE #E3F2FD
   participant "AccessController\n(DRF)" as AC #E8F5E9
   participant "RBACService" as RBAC #E8F5E9
   participant "SegmentService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a Segmentos
   activate FE

   FE -> AC: 2. GET /api/users/{userId}/segments
   activate AC
   AC -> DB: SELECT * FROM user_segments\nWHERE user_id = ?
   DB --> AC: [currentSegments]
   AC --> FE: 3. {segments}
   deactivate AC

   FE -> AC: 4. GET /api/segments/catalog
   activate AC
   AC -> DB: SELECT * FROM cost_centers\nWHERE active = true
   DB --> AC: [allCenters]
   AC --> FE: 5. {catalog}
   deactivate AC

   FE --> ADM: 6. Muestra segmentos actuales\ny catalogo

   ADM -> FE: 7. Selecciona centros [C1, C2, C3]
   ADM -> FE: 8. Clic "Asignar"

   FE -> AC: 9. POST /api/users/{userId}/segments\n{segments: [C1, C2, C3]}
   activate AC

   AC -> RBAC: 10. checkPermission(adminId, 'ACC-003')
   RBAC --> AC: authorized

   AC -> SS: 11. assignSegments(userId, segments)
   activate SS

   SS -> DB: 12. INSERT INTO user_segments\n(user_id, segment_id, assigned_by)\nON CONFLICT DO NOTHING
   DB --> SS: OK

   SS -> AUD: 13. logEvent(SEGMENTS_ASSIGNED,\nadminId, userId, {segments})
   activate AUD
   AUD -> DB: INSERT INTO audit_log
   note right: BR_008
   AUD --> SS: OK
   deactivate AUD

   SS --> AC: 14. {assigned: [C1, C2, C3]}
   deactivate SS

   AC --> FE: 15. 200 OK
   deactivate AC

   FE --> ADM: 16. "Segmentos asignados"
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Asignar Acceso Total
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 5 del flujo normal

**Condicion:** Admin selecciona "Acceso a TODOS los centros"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 5.1
     - Admin marca checkbox "Acceso Total"
   * - 5.2
     - Sistema deshabilita seleccion individual
   * - 5.3
     - Sistema asigna flag all_segments = true
   * - 5.4
     - Usuario podra ver todos los centros, incluidos futuros

**Retorno:** Paso 6 del flujo normal

----

8. Excepciones
--------------

8.1 EX-1: Centro No Existe
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Centro de costo fue eliminado

**Accion del Sistema:** Omite centro invalido, continua con validos

**Mensaje al Usuario:** "Algunos centros no existen y fueron omitidos"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-041 Asignar Segmento
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

   :Admin accede a Segmentos;

   :Verificar permiso ACC-003;

   if (Tiene permiso?) then (si)

       :Mostrar segmentos actuales;
       :Mostrar catalogo de centros;

       if (Selecciona "Acceso Total"?) then (si)
           :Marcar all_segments = true;
       else (no)
           :Seleccionar centros individuales;
       endif

       :Insertar en user_segments;
       #C8E6C9:Registrar en auditoria\n(BR_008);
       #C8E6C9:Mostrar confirmacion;
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
     - Auditoria de Accesos
     - Paso 8: SEGMENTS_ASSIGNED registrado
   * - BR_009
     - Segmentacion de Datos
     - Control de acceso a nivel de datos por centro de costo

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-041.01
     - Sistema DEBE verificar permiso ACC-003
   * - FR-041.02
     - Sistema DEBE mostrar segmentos actuales del usuario
   * - FR-041.03
     - Sistema DEBE mostrar catalogo de centros de costo
   * - FR-041.04
     - Sistema DEBE permitir seleccion multiple de centros
   * - FR-041.05
     - Sistema DEBE permitir opcion "Acceso Total"
   * - FR-041.06
     - Sistema DEBE registrar en auditoria (BR_008)
   * - FR-041.07
     - Sistema DEBE aplicar segmentos en queries de datos

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_008 (Auditoria), BR_009 (Segmentacion)
   * - **FR Derivados**
     - FR-041.01 a FR-041.07 (7 requerimientos)
   * - **UC Relacionados**
     - UC-042 (Revocar Segmento)
   * - **Actores RBAC**
     - AGR-008: admin_seguridad
   * - **Funciones RBAC**
     - ACC-003: Asignar Segmentos

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
