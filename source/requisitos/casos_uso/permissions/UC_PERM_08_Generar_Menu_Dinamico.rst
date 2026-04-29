.. meta::
 :artefacto: UC_PERM_08
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: casos_uso/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-11-09
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Alta

.. _uc-perm-08:

=================================
UC_PERM_08: Generar Menu Dinamico
=================================



1. Resumen
----------


El sistema genera una estructura de menú jerárquica basada en todas las funciones que tiene un usuario, facilitando la navegación en el frontend.


2. Precondiciones
-----------------


- Usuario autenticado
- Usuario tiene al menos 1 funcion


3. Algoritmo
------------


.. code-block:: text

 1. Obtener todas las funciones del usuario (grupos + excepcionales)
 2. Para cada funcion con formato "dominio.subdominio.funcion.accion":
 - Agrupar por dominio → subdominio → funcion → [acciones]
 3. Construir estructura jerárquica tipo árbol
 4. Retornar JSON con estructura navegable



4. SQL Function
---------------


.. code-block:: sql

 CREATE OR REPLACE FUNCTION obtener_menu_usuario(
 p_usuario_id INTEGER
 ) RETURNS JSONB AS $$
 DECLARE
 v_menu JSONB;
 BEGIN
 SELECT jsonb_object_agg(
 dominio,
 funciones
 ) INTO v_menu
 FROM (
 SELECT
 split_part(capacidad_codigo, '.', 2) AS dominio,
 jsonb_object_agg(
 split_part(capacidad_codigo, '.', 3),
 array_agg(split_part(capacidad_codigo, '.', 4))
 ) AS funciones
 FROM vista_capacidades_usuario
 WHERE usuario_id = p_usuario_id
 GROUP BY dominio
 ) AS menu_data;
 
 RETURN COALESCE(v_menu, '{}'::jsonb);
 END;
 $$ LANGUAGE plpgsql STABLE;



5. API Endpoint
---------------


.. code-block:: text

 GET /api/permisos/verificar/{usuario_id}/menu/
 Authorization: Bearer <token>
 
 Response:
 {
 "vistas": {
 "dashboards": ["ver", "editar"],
 "reportes": ["ver", "crear", "exportar"],
 "calidad": ["ver", "evaluar"]
 },
 "administracion": {
 "usuarios": ["ver", "crear", "editar"],
 "grupos": ["ver", "crear"]
 }
 }



6. Performance
--------------


- **SQL Function**: 20-40ms (p95)
- **Con Cache (5 min)**: < 5ms
- **Target**: < 50ms


7. Uso en Frontend
------------------


.. code-block:: typescript

 const { menu, loading } = useMenu;
 
 return (
 <nav>
 {Object.entries(menu).map(([dominio, funciones]) => (
 <MenuSection key={dominio} title={dominio}>
 {Object.entries(funciones).map(([funcion, acciones]) => (
 <MenuItem key={funcion}
 to={`/${dominio}/${funcion}`}
 actions={acciones}
 />
 ))}
 </MenuSection>
 ))}
 </nav>
 );



8. Casos de Prueba
------------------



Caso 1: Usuario con múltiples dominios
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Given: Usuario tiene funciones en "vistas" y "administracion"
- When: Generar menú
- Then: Retorna estructura con 2 dominios principales


Caso 2: Usuario sin funciones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Given: Usuario nuevo sin grupos ni excepciones
- When: Generar menú
- Then: Retorna objeto vacío {}


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

