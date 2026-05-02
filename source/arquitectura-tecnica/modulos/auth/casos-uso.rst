.. _arq-mod-001-casos-uso:

==============================================
ARQ_MOD_001 — Casos de Uso y Requisitos
==============================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Casos de Uso Asociados
=======================

Especificaciones completas: :doc:`/requisitos/casos-uso/auth/index`

.. list-table::
 :widths: 12 35 53
 :header-rows: 1

 * - UC ID
   - Nombre
   - Descripcion
 * - UC_001
   - Iniciar_Sesion
   - Usuario ingresa credenciales y obtiene sesion valida
 * - UC_002
   - Cerrar_Sesion
   - Usuario cierra sesion, token se invalida
 * - UC_003
   - Recuperar_Contrasena
   - Usuario recupera acceso via preguntas de seguridad
 * - UC_004
   - Cambiar_Contrasena
   - Usuario cambia su contrasena actual
 * - UC_005
   - Gestionar_Sesiones_Activas
   - Usuario ve y cierra sus sesiones remotas

----

Requisitos Funcionales Derivados
==================================

.. list-table::
 :widths: 12 40 20 28
 :header-rows: 1

 * - FR ID
   - Nombre
   - Deriva de
   - Descripcion
 * - FR_001
   - Validar_Credenciales
   - UC_001
   - Verificar username/password contra base de datos
 * - FR_002
   - Generar_Token_Autenticacion
   - UC_001
   - Crear token de autenticación con claims de usuario
 * - FR_003
   - Registrar_Sesion_BD
   - UC_001
   - Insertar sesion en tabla UserSession
 * - FR_004
   - Invalidar_Token
   - UC_002
   - Agregar token a blacklist
 * - FR_005
   - Verificar_Preguntas_Seguridad
   - UC_003
   - Validar respuestas de seguridad
