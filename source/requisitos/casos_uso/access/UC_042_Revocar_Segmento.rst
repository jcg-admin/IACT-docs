.. meta::
   :artefacto: UC_042
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-042:

==============================================================================
UC-042: Revocar Segmento de Datos
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
     - UC-042
   * - **Nombre**
     - Revocar Segmento de Datos
   * - **Actor Primario**
     - Administrador de Seguridad
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Baja
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

2. Descripcion
--------------

Permite revocar segmentos de datos previamente asignados a un usuario,
restringiendo su acceso a los centros de costo revocados. Los datos de
esos centros dejan de ser visibles inmediatamente.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-042 Revocar Segmento
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
       usecase "UC-042:\nRevocar\nSegmento" as UC042
       usecase "Registrar\nEvento" as REG
   }

   ADM --> UC042
   UC042 ..> REG : <<include>>
   UC042 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene funcion ACC-004 (Revocar Segmentos)
2. Usuario tiene al menos un segmento asignado

4.2 Trigger
^^^^^^^^^^^

Administrador selecciona "Revocar Segmentos" desde perfil de usuario.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Segmentos eliminados de user_segments
2. Evento SEGMENTS_REVOKED registrado (BR_008)

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
     - Verifica permiso ACC-004
   * - 3
     -
     - Muestra segmentos asignados
   * - 4
     - Selecciona segmentos a revocar
     -
   * - 5
     - Confirma con motivo
     -
   * - 6
     -
     - Elimina de user_segments
   * - 7
     -
     - Registra SEGMENTS_REVOKED (BR_008)
   * - 8
     -
     - Muestra confirmacion

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-042 Revocar Segmento
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "AccessController" as AC #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Selecciona segmentos a revocar
   FE -> AC: 2. DELETE /api/users/{id}/segments\n{segments, reason}
   activate AC
   AC -> DB: 3. DELETE FROM user_segments
   AC -> AUD: 4. logEvent(SEGMENTS_REVOKED)
   AUD -> DB: INSERT audit_log
   AC --> FE: 5. 200 OK
   deactivate AC
   FE --> ADM: 6. "Segmentos revocados"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Revocar Acceso Total
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si usuario tenia all_segments=true, se desactiva el flag.

----

8. Excepciones
--------------

8.1 EX-1: Sin Segmentos Asignados
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "El usuario no tiene segmentos asignados"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-042 Revocar Segmento
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Admin accede a segmentos;
   :Verificar permiso ACC-004;
   if (Tiene permiso?) then (si)
       :Mostrar segmentos asignados;
       :Admin selecciona y confirma;
       :Eliminar de user_segments;
       #C8E6C9:Registrar auditoria;
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
     - SEGMENTS_REVOKED con motivo
   * - BR_009
     - Segmentacion
     - Restriccion de acceso a datos

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-042.01
     - Verificar permiso ACC-004
   * - FR-042.02
     - Mostrar segmentos asignados
   * - FR-042.03
     - Requerir motivo de revocacion
   * - FR-042.04
     - Eliminar de user_segments
   * - FR-042.05
     - Registrar en auditoria (BR_008)

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-004
   * - **BR Aplicables**
     - BR_008, BR_009
   * - **FR Derivados**
     - FR-042.01 a FR-042.05
   * - **Funcion RBAC**
     - ACC-004: Revocar Segmentos

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