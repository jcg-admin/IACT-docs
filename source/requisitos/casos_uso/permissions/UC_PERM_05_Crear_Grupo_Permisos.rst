.. meta::
   :artefacto: UC_PERM_05
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/permissions
   :estado: Aprobado
   :version: 1.0.0
   :fecha_creacion: 2025-11-09
   :ultimo_cambio: 2026-04-29
   :autor: NestorMonroy
   :clasificacion: Alta

.. _uc-perm-05:

===================================
UC_PERM_05: Crear Grupo de Permisos
===================================



1. Resumen
----------


El Administrador crea un nuevo grupo de permisos que agrupa múltiples funciones relacionadas, facilitando la asignación masiva de permisos a usuarios.


2. Precondiciones
-----------------


- Admin autenticado con `sistema.administracion.grupos.crear`
- Código del grupo no existe


3. Flujo Principal
------------------



.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a gestión de grupos
     - Muestra formulario
   * - 2
     - Ingresa código único (ej: "agentes_nivel_2")
     - Valida formato y unicidad
   * - 3
     - Ingresa nombre descriptivo
     - Valida no vacío
   * - 4
     - Opcionalmente ingresa descripción
     - Valida longitud
   * - 5
     - Selecciona funciones a incluir (búsqueda)
     - Muestra funciones disponibles
   * - 6
     - Confirma creación
     - Valida al menos 1 funcion
   * - 7
     - -
     - Crea grupo (INSERT)
   * - 8
     - -
     - Asocia funciones (INSERT en grupo_capacidades)
   * - 9
     - -
     - Registra en auditoría
   * - 10
     - -
     - Muestra confirmación



4. Reglas de Negocio
--------------------



.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - ID
     - Regla
   * - RN-005.1
     - Código del grupo debe ser único y alfanumérico con guiones bajos
   * - RN-005.2
     - Debe tener al menos 1 funcion asociada
   * - RN-005.3
     - Nombre y descripción son obligatorios



5. Datos de Entrada
-------------------


.. code-block:: json

   {
     "codigo": "analistas_calidad",
     "nombre": "Analistas de Calidad",
     "descripcion": "Grupo para analistas que revisan calidad de llamadas",
     "activo": true,
     "capacidades_codigos": [
       "sistema.vistas.calidad.ver",
       "sistema.vistas.calidad.evaluar",
       "sistema.vistas.reportes.calidad.ver"
     ]
   }



6. Datos de Salida
------------------


.. code-block:: json

   {
     "success": true,
     "data": {
       "id": 15,
       "codigo": "analistas_calidad",
       "nombre": "Analistas de Calidad",
       "descripcion": "Grupo para analistas...",
       "activo": true,
       "total_capacidades": 3,
       "created_at": "2025-01-09T11:30:00Z"
     }
   }



7. API Endpoint
---------------


.. code-block:: text

   POST /api/permisos/grupos/
   Authorization: Bearer <token>
   
   Body: Ver sección 5



8. SQL Operation
----------------


.. code-block:: sql

   BEGIN;
   
   -- Crear grupo
   INSERT INTO grupos_permisos (codigo, nombre, descripcion, activo)
   VALUES ('analistas_calidad', 'Analistas de Calidad', '...', TRUE)
   RETURNING id;
   
   -- Asociar funciones
   INSERT INTO grupo_capacidades (grupo_id, capacidad_id)
   SELECT 15, id FROM funciones
   WHERE codigo IN ('sistema.vistas.calidad.ver', ...);
   
   COMMIT;



9. Escenarios de Prueba
-----------------------



Caso 1: Creación exitosa
^^^^^^^^^^^^^^^^^^^^^^^^

- Given: Código único, 3 funciones válidas
- When: Admin crea grupo
- Then: HTTP 201, grupo creado con 3 funciones


Caso 2: Código duplicado
^^^^^^^^^^^^^^^^^^^^^^^^

- Given: Código "agentes_nivel_1" ya existe
- When: Admin intenta crear grupo con mismo código
- Then: HTTP 400, error de unicidad


Caso 3: Sin funciones
^^^^^^^^^^^^^^^^^^^^^^^

- Given: Grupo sin funciones
- When: Admin intenta crear
- Then: HTTP 400, "Debe seleccionar al menos 1 funcion"


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

