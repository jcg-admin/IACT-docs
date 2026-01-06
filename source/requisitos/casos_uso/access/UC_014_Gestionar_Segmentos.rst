.. meta::
   :artefacto: UC_014
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-014:

==============================================================================
UC-014: Gestionar Segmentos de Datos
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
     - UC-014
   * - **Nombre**
     - Gestionar Segmentos de Datos
   * - **Actor Primario**
     - Administrador de Datos
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Alta
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-005: Segmentacion de Datos

----

2. Descripcion
--------------

Permite gestionar los segmentos de datos (centros de costo, unidades de
negocio) que controlan la visibilidad de informacion contable. Los
segmentos implementan seguridad a nivel de fila (Row-Level Security)
segun BR_009. Cada usuario solo ve datos de los segmentos asignados.
Soporta estructura jerarquica de segmentos.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-014 Gestionar Segmentos
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
       usecase "UC-014:\nGestionar\nSegmentos" as UC014
       usecase "Crear\nSegmento" as CS
       usecase "Modificar\nSegmento" as MS
       usecase "Definir\nJerarquia" as DJ
       usecase "Activar/\nDesactivar" as AD
       usecase "Ver Usuarios\nAsignados" as VUA
   }

   ADM --> UC014
   UC014 ..> CS : <<extends>>
   UC014 ..> MS : <<extends>>
   UC014 ..> DJ : <<extends>>
   UC014 ..> AD : <<extends>>
   UC014 ..> VUA : <<extends>>
   UC014 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion SEG-001 (Gestionar Segmentos)
2. Estructura organizacional definida

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Administracion > Segmentos de Datos".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Segmento creado/modificado correctamente
2. Jerarquia de segmentos actualizada
3. Evento SEGMENT_* registrado en auditoria

----

5. Flujo Normal: Crear Segmento
-------------------------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a Gestion de Segmentos
     -
   * - 2
     -
     - Verifica permiso SEG-001
   * - 3
     -
     - Muestra arbol de segmentos existentes
   * - 4
     - Hace clic en "Nuevo Segmento"
     -
   * - 5
     -
     - Muestra formulario
   * - 6
     - Ingresa codigo unico
     -
   * - 7
     - Ingresa nombre descriptivo
     -
   * - 8
     - Selecciona segmento padre (opcional)
     -
   * - 9
     - Selecciona tipo (Centro Costo, UN, Region)
     -
   * - 10
     - Presiona "Guardar"
     -
   * - 11
     -
     - Valida unicidad de codigo
   * - 12
     -
     - Crea segmento con status=ACTIVE
   * - 13
     -
     - Actualiza arbol jerarquico
   * - 14
     -
     - Registra SEGMENT_CREATED

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-014 Crear Segmento
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "SegmentController" as SC #E8F5E9
   participant "SegmentService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a Segmentos
   FE -> SC: 2. GET /api/segments/tree
   activate SC

   SC -> DB: 3. WITH RECURSIVE tree AS (...)\nSELECT * FROM segments
   DB --> SC: [segmentTree]

   SC --> FE: 4. {tree}
   deactivate SC

   FE --> ADM: 5. Arbol de segmentos

   ADM -> FE: 6. Nuevo Segmento
   ADM -> FE: 7. Completa datos
   FE -> SC: 8. POST /api/segments\n{code, name, parentId, type}
   activate SC

   SC -> SS: 9. createSegment(data)
   activate SS

   SS -> DB: 10. SELECT id FROM segments WHERE code = ?
   DB --> SS: [] (no existe)

   SS -> DB: 11. INSERT INTO segments\n(code, name, parent_id, type, status, level)
   note right: level = parent.level + 1
   DB --> SS: {id: 10}

   SS -> SS: 12. updateTreePath()
   note right: path = parent.path + '/' + code

   SS -> AUD: 13. logEvent('SEGMENT_CREATED',\n{segmentId, code, parent})
   AUD -> DB: INSERT audit_log

   SS --> SC: 14. {segment}
   deactivate SS

   SC --> FE: 15. 201 Created
   deactivate SC

   FE --> ADM: 16. Arbol actualizado
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Modificar Jerarquia
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario arrastra segmento a nuevo padre

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Admin arrastra segmento en arbol
   * - 2
     - Sistema muestra preview de nueva ubicacion
   * - 3
     - Admin confirma movimiento
   * - 4
     - Sistema actualiza parent_id y path
   * - 5
     - Sistema recalcula niveles de hijos
   * - 6
     - Registra SEGMENT_MOVED

7.2 FA-2: Desactivar Segmento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Segmento activo sin hijos activos

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 1
     - Sistema verifica no hay hijos activos
   * - 2
     - Sistema verifica no hay usuarios asignados
   * - 3
     - Sistema cambia status = INACTIVE
   * - 4
     - Datos del segmento ya no visibles en reportes

7.3 FA-3: Ver Usuarios del Segmento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Clic en icono de usuarios

Sistema muestra lista paginada de usuarios asignados al segmento.

----

8. Excepciones
--------------

8.1 EX-1: Codigo Duplicado
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "El codigo de segmento '[CODE]' ya existe."

8.2 EX-2: Segmento con Hijos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Intento de eliminar segmento con hijos

**Mensaje:** "No se puede eliminar. El segmento tiene [N] sub-segmentos."

8.3 EX-3: Ciclo en Jerarquia
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Mover segmento a uno de sus descendientes

**Mensaje:** "Operacion invalida: crearia un ciclo en la jerarquia."

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-014 Gestionar Segmentos
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Verificar permiso SEG-001;

   if (Tiene permiso?) then (si)
       :Cargar arbol de segmentos;

       switch (Accion?)
       case (Crear)
           :Ingresar codigo y nombre;
           :Seleccionar padre (opcional);
           :Seleccionar tipo;

           if (Codigo unico?) then (si)
               :Crear segmento;
               :Actualizar path y level;
               #C8E6C9:SEGMENT_CREATED;
           else (no)
               #FFCDD2:Error duplicado;
           endif

       case (Mover)
           :Arrastrar a nuevo padre;

           if (Crea ciclo?) then (si)
               #FFCDD2:Error: ciclo;
           else (no)
               :Actualizar parent_id;
               :Recalcular paths hijos;
               #C8E6C9:SEGMENT_MOVED;
           endif

       case (Desactivar)
           if (Tiene hijos activos?) then (si)
               #FFCDD2:Error: tiene hijos;
           else (no)
               :status = INACTIVE;
               #C8E6C9:SEGMENT_DEACTIVATED;
           endif

       case (Eliminar)
           if (Tiene hijos?) then (si)
               #FFCDD2:Error: tiene hijos;
           elseif (Tiene usuarios?) then (si)
               #FFCDD2:Error: tiene usuarios;
           else (no)
               :Eliminar segmento;
               #C8E6C9:SEGMENT_DELETED;
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
   * - BR_009
     - Segmentacion
     - Base de Row-Level Security
   * - BR_031
     - Jerarquia Segmentos
     - Maximo 5 niveles de profundidad

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-014.01
     - Verificar permiso SEG-001
   * - FR-014.02
     - Mostrar segmentos en estructura de arbol
   * - FR-014.03
     - Permitir crear segmento con codigo, nombre, tipo
   * - FR-014.04
     - Soportar estructura jerarquica (padre-hijo)
   * - FR-014.05
     - Permitir mover segmento a nuevo padre (drag & drop)
   * - FR-014.06
     - Detectar y prevenir ciclos en jerarquia
   * - FR-014.07
     - Calcular nivel automaticamente segun padre
   * - FR-014.08
     - Mantener path materializado para queries
   * - FR-014.09
     - Permitir activar/desactivar segmentos
   * - FR-014.10
     - Impedir eliminar segmentos con hijos o usuarios
   * - FR-014.11
     - Mostrar usuarios asignados a cada segmento

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-005
   * - **BR Aplicables**
     - BR_008, BR_009, BR_031
   * - **FR Derivados**
     - FR-014.01 a FR-014.11
   * - **UC Relacionados**
     - UC-015 (Asignar Segmento)
   * - **Funcion RBAC**
     - SEG-001

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
     - Version completa. Jerarquia. Drag & drop. Path materializado.