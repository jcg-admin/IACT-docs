.. meta::
   :artefacto: UC_046
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-046:

==============================================================================
UC-046: Gestionar Catalogo de Funciones
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
     - UC-046
   * - **Nombre**
     - Gestionar Catalogo de Funciones
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

Permite gestionar el catalogo de funciones atomicas del sistema RBAC. Las
funciones son los permisos granulares que controlan acceso a acciones
especificas del sistema. Basado en RBAC_v5_1_1 con 44 funciones.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-046 Gestionar Funciones
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
       usecase "UC-046:\nGestionar\nFunciones" as UC046
       usecase "Crear" as C
       usecase "Modificar" as M
       usecase "Desactivar" as D
       usecase "Ver\nUso" as VU
   }

   ADM --> UC046
   UC046 ..> C : <<extends>>
   UC046 ..> M : <<extends>>
   UC046 ..> D : <<extends>>
   UC046 ..> VU : <<extends>>
   UC046 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene funcion ACC-008 (Gestionar Funciones)

4.2 Trigger
^^^^^^^^^^^

Administrador accede a "Catalogo de Funciones".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Funcion creada/modificada/desactivada
2. Evento FUNCTION_MODIFIED registrado (BR_008)

----

5. Flujo Normal (Crear Funcion)
-------------------------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a Catalogo Funciones
     -
   * - 2
     -
     - Muestra lista por modulo
   * - 3
     - Clic "Nueva Funcion"
     -
   * - 4
     - Ingresa: codigo, nombre, modulo, descripcion
     -
   * - 5
     - Presiona "Guardar"
     -
   * - 6
     -
     - Valida codigo unico
   * - 7
     -
     - Valida formato codigo (XXX-NNN)
   * - 8
     -
     - Inserta en functions
   * - 9
     -
     - Registra FUNCTION_CREATED (BR_008)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-046 Gestionar Funciones
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "FunctionController" as FC #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Ver catalogo funciones
   FE -> FC: 2. GET /api/functions?groupBy=module
   activate FC
   FC -> DB: SELECT * FROM functions\nORDER BY module, code
   DB --> FC: [functions]
   FC --> FE: 3. {functionsByModule}
   deactivate FC

   FE --> ADM: 4. Lista agrupada por modulo
   note right: AUT (5), USR (4),\nACC (8), RPT (14), etc.

   ADM -> FE: 5. Crear nueva funcion
   FE -> FC: 6. POST /api/functions\n{code, name, module, description}
   activate FC

   FC -> DB: 7. Validar codigo unico
   FC -> DB: 8. INSERT INTO functions

   FC -> AUD: 9. logEvent(FUNCTION_CREATED)
   AUD -> DB: INSERT audit_log

   FC --> FE: 10. 201 Created
   deactivate FC
   FE --> ADM: 11. "Funcion creada"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Ver Uso de Funcion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

cat >> /mnt/user-data/outputs/casos_uso_v2/access/UC_046_Gestionar_Funciones.rst << 'EOF'

Muestra usuarios y agrupadores que tienen asignada la funcion.

7.2 FA-2: Desactivar Funcion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Marca funcion como inactiva. Sistema advierte si hay usuarios afectados.

----

8. Excepciones
--------------

8.1 EX-1: Codigo Duplicado
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "El codigo de funcion ya existe"

8.2 EX-2: Formato Invalido
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "Codigo debe ser XXX-NNN (ej: AUT-001)"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-046 Gestionar Funciones
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Admin accede a Catalogo;
   :Verificar permiso ACC-008;

   if (Tiene permiso?) then (si)
       :Mostrar funciones por modulo;

       switch (Accion?)
       case (Crear)
           :Ingresar datos;
           :Validar codigo unico;
           :Validar formato XXX-NNN;
           :Insertar funcion;
       case (Modificar)
           :Actualizar nombre/descripcion;
       case (Desactivar)
           :Verificar uso actual;
           :Advertir usuarios afectados;
           :Marcar inactive=true;
       case (Ver Uso)
           :Mostrar usuarios con funcion;
           :Mostrar agrupadores con funcion;
       endswitch

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
     - Cambios en funciones registrados

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-046.01
     - Verificar permiso ACC-008
   * - FR-046.02
     - Listar funciones agrupadas por modulo
   * - FR-046.03
     - Crear funcion con codigo formato XXX-NNN
   * - FR-046.04
     - Validar unicidad de codigo
   * - FR-046.05
     - Modificar nombre y descripcion
   * - FR-046.06
     - Desactivar funcion (baja logica)
   * - FR-046.07
     - Mostrar uso de funcion (usuarios/agrupadores)
   * - FR-046.08
     - Registrar cambios en auditoria

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-004
   * - **BR Aplicables**
     - BR_008
   * - **FR Derivados**
     - FR-046.01 a FR-046.08
   * - **Funcion RBAC**
     - ACC-008: Gestionar Funciones

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
