.. meta::
   :artefacto: UC_045
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-045:

==============================================================================
UC-045: Gestionar Catalogo de Agrupadores
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
     - UC-045
   * - **Nombre**
     - Gestionar Catalogo de Agrupadores
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

Permite gestionar el catalogo de agrupadores (roles/perfiles) del sistema RBAC.
Los agrupadores son conjuntos predefinidos de funciones que facilitan la
asignacion de permisos a usuarios.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-045 Gestionar Agrupadores
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
       usecase "UC-045:\nGestionar\nAgrupadores" as UC045
       usecase "Crear" as C
       usecase "Modificar" as M
       usecase "Desactivar" as D
       usecase "Asignar\nFunciones" as AF
   }

   ADM --> UC045
   UC045 ..> C : <<extends>>
   UC045 ..> M : <<extends>>
   UC045 ..> D : <<extends>>
   UC045 ..> AF : <<include>>
   UC045 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene funcion ACC-007 (Gestionar Agrupadores)

4.2 Trigger
^^^^^^^^^^^

Administrador accede a "Catalogo de Agrupadores".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Agrupador creado/modificado/desactivado
2. Evento GROUPER_MODIFIED registrado (BR_008)

----

5. Flujo Normal (Crear Agrupador)
---------------------------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a Catalogo Agrupadores
     -
   * - 2
     -
     - Muestra lista de agrupadores
   * - 3
     - Clic "Nuevo Agrupador"
     -
   * - 4
     - Ingresa codigo, nombre, descripcion
     -
   * - 5
     - Selecciona funciones a incluir
     -
   * - 6
     - Presiona "Guardar"
     -
   * - 7
     -
     - Valida codigo unico
   * - 8
     -
     - Inserta en groupers y grouper_functions
   * - 9
     -
     - Registra GROUPER_CREATED (BR_008)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-045 Crear Agrupador
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "GrouperController" as GC #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Crear agrupador\n{code, name, functions}
   FE -> GC: 2. POST /api/groupers
   activate GC

   GC -> DB: 3. Verificar codigo unico
   GC -> DB: 4. INSERT INTO groupers
   GC -> DB: 5. INSERT INTO grouper_functions\n(para cada funcion)

   GC -> AUD: 6. logEvent(GROUPER_CREATED)
   AUD -> DB: INSERT audit_log

   GC --> FE: 7. 201 Created
   deactivate GC
   FE --> ADM: 8. "Agrupador creado"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Modificar Agrupador
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Permite cambiar nombre, descripcion y funciones asociadas.

7.2 FA-2: Desactivar Agrupador
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Marca agrupador como inactivo (no elimina por trazabilidad).

----

8. Excepciones
--------------

8.1 EX-1: Codigo Duplicado
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "El codigo de agrupador ya existe"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-045 Gestionar Agrupadores
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Admin accede a Catalogo;
   :Verificar permiso ACC-007;

   if (Tiene permiso?) then (si)
       :Mostrar lista agrupadores;

       switch (Accion?)
       case (Crear)
           :Ingresar datos;
           :Seleccionar funciones;
           :Validar codigo unico;
           :Insertar agrupador;
       case (Modificar)
           :Cargar agrupador;
           :Modificar datos/funciones;
           :Actualizar BD;
       case (Desactivar)
           :Confirmar desactivacion;
           :Marcar inactive=true;
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
     - Cambios en agrupadores registrados

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-045.01
     - Verificar permiso ACC-007
   * - FR-045.02
     - Listar agrupadores existentes
   * - FR-045.03
     - Crear agrupador con codigo unico
   * - FR-045.04
     - Asignar funciones al agrupador
   * - FR-045.05
     - Modificar nombre y descripcion
   * - FR-045.06
     - Desactivar agrupador (baja logica)
   * - FR-045.07
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
     - FR-045.01 a FR-045.07
   * - **Funcion RBAC**
     - ACC-007: Gestionar Agrupadores

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