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
funciones son permisos granulares (44 en total segun RBAC_v5_1_1).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: UC-046 Gestionar Funciones
   :align: center

   @startuml
   left to right direction
   skinparam actorStyle awesome
   skinparam backgroundColor #FAFAFA

   actor "Admin\nSeguridad" as ADM

   rectangle "MOD_Access" {
       usecase "UC-046:\nGestionar\nFunciones" as UC046
       usecase "Crear" as C
       usecase "Modificar" as M
       usecase "Desactivar" as D
   }

   ADM --> UC046
   UC046 ..> C : <<extends>>
   UC046 ..> M : <<extends>>
   UC046 ..> D : <<extends>>
   @enduml

----

4. Contexto
-----------

**Precondiciones:** Tiene funcion ACC-008 (Gestionar Funciones)

**Trigger:** Accede a "Catalogo de Funciones"

**Postcondiciones:** Funcion creada/modificada en BD, evento en auditoria

----

5. Flujo Normal
---------------

1. Admin accede a Catalogo de Funciones
2. Sistema muestra lista agrupada por modulo
3. Admin crea/modifica/desactiva funcion
4. Sistema valida codigo unico (formato XXX-NNN)
5. Sistema registra en auditoria (BR_008)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-046
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "FunctionController" as FC #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Ver/Crear funcion
   FE -> FC: 2. GET/POST /api/functions
   FC -> DB: 3. SELECT/INSERT functions
   FC --> FE: 4. Response
   FE --> ADM: 5. Confirmacion
   @enduml

----

7. Flujos Alternos
------------------

- **Ver Uso:** Muestra usuarios y agrupadores con la funcion
- **Desactivar:** Advierte usuarios afectados antes de desactivar

----

8. Excepciones
--------------

- **Codigo duplicado:** "El codigo ya existe"
- **Formato invalido:** "Codigo debe ser XXX-NNN"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-046
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   start
   :Verificar ACC-008;
   if (Permiso?) then (si)
       :Mostrar catalogo;
       :Admin realiza accion;
       :Validar y guardar;
       #C8E6C9:Registrar auditoria;
   else (no)
       #FFCDD2:403 Forbidden;
   endif
   stop
   @enduml

----

10. Reglas de Negocio
---------------------

- BR_008: Cambios registrados en auditoria

----

11. Requerimientos Funcionales
------------------------------

- FR-046.01: Verificar permiso ACC-008
- FR-046.02: Listar funciones por modulo
- FR-046.03: Crear con codigo XXX-NNN
- FR-046.04: Validar unicidad
- FR-046.05: Modificar nombre/descripcion
- FR-046.06: Desactivar (baja logica)
- FR-046.07: Ver uso de funcion
- FR-046.08: Registrar en auditoria

----

12. Trazabilidad
----------------

- **BReq:** BReq-004
- **BR:** BR_008
- **Funcion RBAC:** ACC-008

----

13. Historial
-------------

- 2.0.0 (2026-01-06): Version con PlantUML

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
