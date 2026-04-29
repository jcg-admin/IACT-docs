.. meta::
 :artefacto: UC_PERM_07
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: casos_uso/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-11-09
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Critica

.. _uc-perm-07:

========================================
UC_PERM_07: Verificar Permiso de Usuario
========================================

.. note:: Vista alternativa (coexistencia ACC ↔ PERM)

 Este UC representa una vista del modelo RBAC. La
 vista funcional / catalogo cerrado del mismo concepto esta en
 :doc:`/requisitos/casos_uso/access/UC_ACC_03_Consultar_Permisos`
 (o equivalente). Ambas coexisten per
 :doc:`/normativa/gobernanza/ADR-GOB-008-rbac-coexistencia-acc-perm`.




1. Resumen
   ----------


El sistema verifica si un usuario tiene una funcion específica, evaluando en orden: revocaciones excepcionales, concesiones excepcionales, y grupos asignados.


2. Precondiciones
   -----------------


- Usuario autenticado
- Funcion a verificar existe


3. Algoritmo de Verificación (Orden de Precedencia)
   ---------------------------------------------------


.. code-block:: text

 1. SI existe revocación excepcional activa → DENEGAR (prioridad máxima)
 2. SI existe concesión excepcional activa → CONCEDER
 3. SI usuario tiene funcion por algún grupo activo → CONCEDER
 4. SINO → DENEGAR



4. Performance Target
   ---------------------


- **Con SQL Function**: 5-10ms
- **Con ORM**: 30-50ms
- **Con Cache**: < 1ms


5. SQL Function
   ---------------


.. code-block:: sql

 CREATE OR REPLACE FUNCTION usuario_tiene_permiso(
 p_usuario_id INTEGER,
 p_capacidad_codigo VARCHAR(200)
 ) RETURNS BOOLEAN AS $$
 DECLARE
 v_tiene_permiso BOOLEAN;
 BEGIN
 -- Verificar usando vista optimizada
 SELECT EXISTS (
 SELECT 1 FROM vista_capacidades_usuario
 WHERE usuario_id = p_usuario_id
 AND capacidad_codigo = p_capacidad_codigo
 ) INTO v_tiene_permiso;
 
 RETURN v_tiene_permiso;
 END;
 $$ LANGUAGE plpgsql STABLE PARALLEL SAFE;



6. API Endpoint
   ---------------


.. code-block:: text

 GET /api/permisos/verificar/{usuario_id}/tiene-permiso/?funcion={codigo}
 Authorization: Bearer <token>
 
 Response:
 {
 "usuario_id": 123,
 "funcion": "sistema.vistas.dashboards.ver",
 "tiene_permiso": true,
 "origen": "grupo", // o "excepcional_conceder" o "excepcional_revocar"
 "verificado_en": "2025-01-09T12:00:00Z"
 }



7. Casos de Uso
   ---------------



Caso 1: Usuario con funcion por grupo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Given: Usuario en grupo "Agentes" que tiene "dashboards.ver"
- When: Verificar "dashboards.ver"
- Then: tiene_permiso=true, origen="grupo"


Caso 2: Usuario con revocación excepcional
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Given: Usuario en grupo con funcion, PERO tiene revocación excepcional
- When: Verificar esa funcion
- Then: tiene_permiso=false, origen="excepcional_revocar"


Caso 3: Usuario con concesión excepcional
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Given: Usuario sin grupo que tenga la funcion, PERO tiene concesión
- When: Verificar esa funcion
- Then: tiene_permiso=true, origen="excepcional_conceder"


8. Integración
   --------------


Este caso de uso es invocado por:
- Decoradores (@require_permission)
- Permission classes (DRF)
- Frontend (hooks usePermisos)
- Middleware de auditoría


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

