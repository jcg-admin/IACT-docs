.. meta::
 :artefacto: UC_PERM_04
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: casos_uso/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-11-09
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Alta

.. _uc-perm-04:

=======================================
UC_PERM_04: Revocar Permiso Excepcional
=======================================

**Funcion RBAC backing:** ACC-009 ``revoke_exceptional_permission`` (NUEVA v5.3.0)



1. Resumen
----------


El Administrador de Sistema crea una excepción de tipo "revocar" que BLOQUEA una funcion específica que el usuario tendría por sus grupos. Tiene prioridad sobre las concesiones de grupos.


2. Actores
----------


- **Actor Primario**: Administrador de Sistema
- **Actores Secundarios**: Usuario afectado


3. Precondiciones
-----------------



.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - ID
   - Descripción
 * - PRE-004.1
   - Admin autenticado con `sistema.administracion.permisos.excepcionales.revocar`
 * - PRE-004.2
   - Usuario objetivo existe
 * - PRE-004.3
   - Usuario TIENE la funcion (por grupo) que se desea revocar
 * - PRE-004.4
   - No existe ya una revocación excepcional activa para esta funcion



4. Postcondiciones
------------------



.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - ID
   - Descripción
 * - POST-004.1
   - Se crea registro en `permisos_excepcionales` con tipo='revocar'
 * - POST-004.2
   - Usuario pierde acceso a la funcion INMEDIATAMENTE
 * - POST-004.3
   - Revocación tiene prioridad sobre cualquier concesión de grupo
 * - POST-004.4
   - Se registra en auditoría
 * - POST-004.5
   - Cache de permisos se invalida



5. Flujo Principal
------------------



.. list-table::
 :widths: 25 25 25 25
 :header-rows: 1

 * - Paso
   - Actor
   - Acción
   - Sistema
 * - 1
   - Admin
   - Accede a gestión de excepcionales
   - Muestra interfaz
 * - 2
   - Admin
   - Selecciona usuario
   - Muestra funciones actuales del usuario
 * - 3
   - Admin
   - Selecciona funcion a revocar
   - Valida que usuario la tenga por grupo
 * - 4
   - Admin
   - Ingresa motivo de revocación (obligatorio)
   - Valida longitud mínima
 * - 5
   - Admin
   - Opcionalmente establece fecha_fin
   - Valida fecha futura
 * - 6
   - Admin
   - Confirma revocación
   - Verifica permisos de admin
 * - 7
   - Sistema
   - Crea registro tipo='revocar', activo=True
   - INSERT en permisos_excepcionales
 * - 8
   - Sistema
   - Invalida cache del usuario
   - DELETE cache
 * - 9
   - Sistema
   - Registra en auditoría
   - INSERT con tipo='REVOCAR_EXCEPCIONAL'
 * - 10
   - Sistema
   - Notifica usuario
   - Email con explicación
 * - 11
   - Sistema
   - Confirma revocación
   - Mensaje de éxito



6. Reglas de Negocio
--------------------



.. list-table::
 :widths: 33 33 33
 :header-rows: 1

 * - ID
   - Regla
   - Tipo
 * - RN-004.1
   - Revocación excepcional SIEMPRE tiene prioridad sobre grupos
   - Crítica
 * - RN-004.2
   - Usuario debe tener la funcion por grupo para poder revocarla
   - Alta
 * - RN-004.3
   - Motivo obligatorio mínimo 20 caracteres
   - Alta
 * - RN-004.4
   - Revocación es inmediata
   - Alta



7. Datos de Entrada
-------------------


.. code-block:: json

 {
 "usuario_id": 456,
 "capacidad_codigo": "sistema.administracion.usuarios.eliminar",
 "tipo": "revocar",
 "motivo": "Usuario no debe eliminar usuarios durante período de auditoría por política de seguridad corporativa",
 "fecha_fin": "2025-02-01T00:00:00Z",
 "asignado_por_id": 1
 }



8. Datos de Salida
------------------


.. code-block:: json

 {
 "success": true,
 "message": "Permiso excepcional revocado",
 "data": {
 "id": 999,
 "usuario_id": 456,
 "capacidad_codigo": "sistema.administracion.usuarios.eliminar",
 "tipo": "revocar",
 "motivo": "Usuario no debe eliminar...",
 "fecha_inicio": "2025-01-09T11:00:00Z",
 "fecha_fin": "2025-02-01T00:00:00Z",
 "activo": true
 }
 }



9. Especificaciones Técnicas
----------------------------



API Endpoint
^^^^^^^^^^^^


.. code-block:: text

 POST /api/permisos/excepcionales/
 Content-Type: application/json
 
 {
 "usuario_id": 456,
 "capacidad_codigo": "sistema.administracion.usuarios.eliminar",
 "tipo": "revocar",
 "motivo": "...",
 "fecha_fin": "2025-02-01T00:00:00Z"
 }



Lógica de Verificación
^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: sql

 -- Al verificar permiso, primero verificar revocaciones
 SELECT EXISTS (
 SELECT 1 FROM permisos_excepcionales
 WHERE usuario_id = 456
 AND capacidad_id = (SELECT id FROM funciones WHERE codigo = '...')
 AND tipo = 'revocar'
 AND activo = TRUE
 AND (fecha_fin IS NULL OR fecha_fin > NOW)
 ) AS esta_revocado;
 
 -- Si esta_revocado = TRUE, denegar acceso inmediatamente
 -- Sin importar grupos o concesiones



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

