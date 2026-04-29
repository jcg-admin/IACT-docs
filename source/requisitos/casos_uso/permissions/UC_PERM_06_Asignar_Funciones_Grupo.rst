.. meta::
 :artefacto: UC_PERM_06
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: casos_uso/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-11-09
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Media

.. _uc-perm-06:

=======================================
UC_PERM_06: Asignar Funciones a Grupo
=======================================

.. note:: Vista alternativa (coexistencia ACC ↔ PERM)

 Este UC representa una vista del modelo RBAC. La
 vista funcional / catalogo cerrado del mismo concepto esta en
 :doc:`/requisitos/casos_uso/access/UC_ACC_04_Asignar_Agrupador`
 (o equivalente). Ambas coexisten per
 :doc:`/normativa/gobernanza/ADR-GOB-008-rbac-coexistencia-acc-perm`.




1. Resumen
----------


El Administrador modifica las funciones asociadas a un grupo existente, agregando o removiendo funciones según necesidades del negocio.


2. Flujo Principal
------------------



.. list-table::
 :widths: 33 33 33
 :header-rows: 1

 * - Paso
   - Actor
   - Sistema
 * - 1
   - Selecciona grupo existente
   - Muestra funciones actuales
 * - 2
   - Agrega nuevas funciones
   - Valida que no estén ya asociadas
 * - 3
   - Opcionalmente remueve funciones
   - Muestra impacto en usuarios
 * - 4
   - Confirma cambios
   - Valida grupo tenga al menos 1 funcion
 * - 5
   - -
   - Actualiza asociaciones (INSERT/DELETE)
 * - 6
   - -
   - Invalida cache de todos los usuarios del grupo
 * - 7
   - -
   - Registra auditoría
 * - 8
   - -
   - Notifica usuarios afectados



3. Reglas de Negocio
--------------------


- RN-006.1: Grupo debe mantener al menos 1 funcion
- RN-006.2: Cambios afectan inmediatamente a todos los usuarios del grupo
- RN-006.3: Se debe auditar cada cambio


4. Datos de Entrada
-------------------


.. code-block:: json

 {
 "grupo_id": 5,
 "agregar_capacidades": [
 "sistema.vistas.reportes.avanzados.ver"
 ],
 "remover_capacidades": [
 "sistema.vistas.dashboards.editar"
 ]
 }



5. API Endpoint
---------------


.. code-block:: text

 PUT /api/permisos/grupos/5/funciones/
 Authorization: Bearer <token>



6. Impacto
----------


Al modificar funciones de un grupo, TODOS los usuarios con ese grupo se ven afectados inmediatamente. El sistema debe:
- Invalidar cache de TODOS los usuarios del grupo
- Notificar cambios a usuarios activos
- Registrar en auditoría con lista de usuarios afectados


Changelog
---------



.. list-table::
 :widths: 25 25 25 25
 :header-rows: 1

 * - Versión
   - Fecha
   - Autor
   - Cambios
 * - 1.0.0
   - 2025-01-09
   - Sistema
   - Creación inicial

