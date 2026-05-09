.. meta::
 :artefacto: BR_007
 :tipo: Regla de Negocio
 :dominio: requisitos
 :subdominio: reglas_negocio
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-01-04
 :ultimo_cambio: 2026-01-04
 :autor: Equipo IACT
 :clasificacion: Interno

.. _br-007:

========================================================
BR_007: Separacion de Funciones (separation of duties)
========================================================


Resumen Ejecutivo
-----------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - BR_007
 * - **Nombre**
   - Separacion de Funciones (separation of duties)
 * - **Tipo**
   - Restriccion
 * - **Categoria**
   - Seguridad
 * - **Criticidad**
   - Alta
 * - **Estado**
   - Vigente

----

1. Definicion Formal
--------------------

1.1 Enunciado de la Regla
^^^^^^^^^^^^^^^^^^^^^^^^^

Ciertas combinaciones de funciones NO PUEDEN ser asignadas al mismo usuario
para prevenir conflictos de interes y fraude. El sistema DEBE validar
restricciones de separacion antes de cualquier asignacion de funciones.

1.2 Formulacion SBVR
^^^^^^^^^^^^^^^^^^^^

::

 VOCABULARIO:
 - Separation of Duties (Segregacion de Funciones)
 - Restriccion de separacion: Par de funciones mutuamente excluyentes
 - Conflicto de separacion: Usuario con funciones que violan restriccion

 REGLA:
 Es prohibido que un usuario tenga funciones que violen una restriccion de separacion.
 Es obligatorio que el sistema valide separacion antes de asignar funciones.

1.3 Justificacion
^^^^^^^^^^^^^^^^^

Separacion de deberes es control fundamental de seguridad que previene fraude y errores.
Ej: quien crea usuarios no debe poder asignar permisos administrativos.
Cumple con principios de auditoria y control interno.

----

2. Clasificacion
----------------

2.1 Tipo de Regla
^^^^^^^^^^^^^^^^^

[X] **Restriccion**: Limita acciones o valores permitidos

2.2 Naturaleza
^^^^^^^^^^^^^^

- **Estatica/Dinamica**: Dinamica - restricciones configurables
- **Automatizable**: Si - validacion en asignacion
- **Alcance**: MOD_Access

----

3. Origen y Autoridad
---------------------

3.1 Fuente Primaria
^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Documento**
   - CNST_005_Seguridad_DRF_Checklist
 * - **Seccion**
   - Segregacion de Funciones
 * - **Version**
   - 1.0.0
 * - **Tipo Fuente**
   - CNST + Estandar NIST

3.2 Autoridad de Modificacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Responsable**: permission_admin (AGR-007 — ``permission_admin_group``)
- **Proceso de Cambio**: Configuracion via UC_ADM_01 (ciclo de vida de
  reglas de separacion) y vista operativa via UC_ACC_05
- **Frecuencia de Revision**: Semestral

----

4. Aplicacion en Sistema
------------------------

4.1 Donde Aplica
^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Descripcion de Aplicacion
 * - MOD_Access
   - Valida separacion en asignacion de funciones
 * - Tabla sod_restrictions
   - Almacena pares de funciones incompatibles
 * - API asignacion
   - Rechaza asignacion si viola separacion

4.2 Actores Afectados
^^^^^^^^^^^^^^^^^^^^^

- **Roles**: AGR-001 (asigna funciones), AGR-008 (configura separacion)

4.3 Excepciones
^^^^^^^^^^^^^^^

Sin excepciones automaticas. Casos especiales requieren aprobacion
documentada del sponsor y registro en auditoria.

----

5. Trazabilidad
---------------

5.1 Restricciones Origen (CNST)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 20 80
 :header-rows: 1

 * - CNST
   - Relacion
 * - CNST_005
   - Define requisitos de separacion

5.2 BReq Influenciados
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 20 80
 :header-rows: 1

 * - BReq
   - Descripcion
 * - BReq-004
   - Cumplimiento de Seguridad

5.3 Casos de Uso Afectados (UC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 20 80
 :header-rows: 1

 * - UC
   - Donde Aplica
 * - UC-010
   - Asignar Funciones - validacion de separacion
 * - UC_ADM_01
   - Gestionar Ciclo de Vida de Reglas de Separacion (crear, actualizar,
     activar/desactivar)
 * - UC_ACC_05
   - Vista operativa de reglas de separacion vigentes
 * - UC_ACC_03
   - Consultar Permisos Efectivos - muestra conflictos de separacion

----

6. Verificacion
---------------

6.1 Criterios de Cumplimiento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. No existen usuarios con funciones que violen separacion
2. Intentos de asignacion violatoria son rechazados
3. Restricciones de separacion documentadas y vigentes

6.2 Metodo de Verificacion
^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Tipo**: Automatizado
- **Frecuencia**: Por transaccion de asignacion
- **Responsable**: MOD_Access

6.3 Consecuencias de Incumplimiento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Asignacion bloqueada con mensaje de error
- Registro en log de auditoria
- Notificacion a ``permission_admin_group`` (AGR-007)

----

7. Restricciones de separacion Definidas
------------------------------------------

::

 SOD-001 (pipeline_audit_separation):
   view_pipeline_status vs view_audit_log

 SOD-002 (user_audit_separation):
   create_users vs view_audit_log

 SOD-003 (access_audit_separation):
   assign_functions vs view_audit_log

----

8. Historial de Cambios
-----------------------

.. list-table::
 :widths: 15 15 20 50
 :header-rows: 1

 * - Version
   - Fecha
   - Autor
   - Descripcion del Cambio
 * - 1.0.0
   - 2026-01-04
   - Equipo IACT
   - Version inicial
