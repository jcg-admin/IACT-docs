.. meta::
   :artefacto: UC_043
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-043:

==============================================================================
UC-043: Configurar Restricciones SoD
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
     - UC-043
   * - **Nombre**
     - Configurar Restricciones SoD
   * - **Actor Primario**
     - Administrador de Seguridad
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Alta
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

2. Descripcion
--------------

Permite configurar reglas de Segregacion de Funciones (SoD) que definen
combinaciones de funciones mutuamente excluyentes. Estas reglas previenen
que un usuario tenga funciones que generen conflicto de intereses.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-043 Configurar SoD
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
       usecase "UC-043:\nConfigurar\nSoD" as UC043
       usecase "Crear\nRegla" as CR
       usecase "Modificar\nRegla" as MR
       usecase "Eliminar\nRegla" as ER
       usecase "Verificar\nImpacto" as VI
   }

   ADM --> UC043
   UC043 ..> CR : <<extends>>
   UC043 ..> MR : <<extends>>
   UC043 ..> ER : <<extends>>
   UC043 ..> VI : <<include>>
   UC043 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene funcion ACC-005 (Configurar SoD)
2. Catalogo de funciones disponible

4.2 Trigger
^^^^^^^^^^^

Administrador accede a "Configuracion SoD" en modulo de seguridad.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Regla SoD creada/modificada/eliminada en sod_rules
2. Evento SOD_CONFIGURED registrado (BR_008)
3. Regla aplicada en futuras asignaciones

----

5. Flujo Normal (Crear Regla)
-----------------------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a Configuracion SoD
     -
   * - 2
     -
     - Muestra reglas existentes
   * - 3
     - Clic "Nueva Regla"
     -
   * - 4
     -
     - Muestra formulario de regla
   * - 5
     - Selecciona Funcion A
     -
   * - 6
     - Selecciona Funcion B (conflictiva)
     -
   * - 7
     - Ingresa descripcion/motivo
     -
   * - 8
     - Presiona "Guardar"
     -
   * - 9
     -
     - Verifica impacto (usuarios afectados)
   * - 10
     -
     - Muestra usuarios en conflicto si existen
   * - 11
     - Confirma creacion
     -
   * - 12
     -
     - Inserta en sod_rules
   * - 13
     -
     - Registra SOD_RULE_CREATED (BR_008)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-043 Crear Regla SoD
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "SoDController" as SC #E8F5E9
   participant "SoDService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Crea nueva regla\n{funcA, funcB, descripcion}
   FE -> SC: 2. POST /api/sod/rules
   activate SC

   SC -> SS: 3. createRule(funcA, funcB)
   activate SS

   SS -> DB: 4. Verificar si regla existe
   SS -> DB: 5. Buscar usuarios con ambas funciones
   DB --> SS: [usersInConflict]

   alt Hay usuarios en conflicto
       SS --> SC: {conflicts: [users]}
       SC --> FE: 6. 409 Conflict {users}
       FE --> ADM: 7. "X usuarios tienen conflicto"
       ADM -> FE: 8. Confirma de todas formas
       FE -> SC: 9. POST /api/sod/rules?force=true
   end

   SS -> DB: 10. INSERT INTO sod_rules\n(function_a, function_b, description)

   SS -> AUD: 11. logEvent(SOD_RULE_CREATED)
   AUD -> DB: INSERT audit_log

   SS --> SC: 12. {rule}
   deactivate SS
   SC --> FE: 13. 201 Created
   deactivate SC
   FE --> ADM: 14. "Regla SoD creada"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Usuarios Ya en Conflicto
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si existen usuarios que ya tienen ambas funciones, el sistema:
- Muestra lista de usuarios afectados
- Permite crear regla de todas formas (no retroactivo)
- O cancelar para resolver primero

7.2 FA-2: Eliminar Regla
^^^^^^^^^^^^^^^^^^^^^^^^

Admin puede eliminar reglas existentes con confirmacion.

----

8. Excepciones
--------------

8.1 EX-1: Regla Duplicada
^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "Ya existe una regla entre estas funciones"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-043 Configurar SoD
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Admin accede a Config SoD;
   :Verificar permiso ACC-005;

   if (Tiene permiso?) then (si)
       :Mostrar reglas existentes;

       switch (Accion?)
       case (Crear)
           :Seleccionar funciones A y B;
           :Verificar impacto;
           if (Usuarios en conflicto?) then (si)
               :Mostrar advertencia;
               if (Admin confirma?) then (si)
               else (no)
                   stop
               endif
           else (no)
           endif
           :Insertar regla;
       case (Modificar)
           :Actualizar descripcion;
       case (Eliminar)
           :Confirmar eliminacion;
           :Eliminar regla;
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
     - Cambios en reglas SoD registrados
   * - BR_010
     - Segregacion Funciones
     - Define funciones mutuamente excluyentes

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-043.01
     - Verificar permiso ACC-005
   * - FR-043.02
     - Listar reglas SoD existentes
   * - FR-043.03
     - Crear regla con par de funciones
   * - FR-043.04
     - Validar no duplicidad de reglas
   * - FR-043.05
     - Verificar impacto antes de crear
   * - FR-043.06
     - Permitir modificar descripcion
   * - FR-043.07
     - Permitir eliminar reglas
   * - FR-043.08
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
     - BR_008, BR_010
   * - **FR Derivados**
     - FR-043.01 a FR-043.08
   * - **UC Relacionados**
     - UC-010 (usa reglas al asignar)
   * - **Funcion RBAC**
     - ACC-005: Configurar SoD

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