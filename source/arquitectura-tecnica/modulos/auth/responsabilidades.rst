.. _arq-mod-001-responsabilidades:

==============================================
ARQ_MOD_001 — Responsabilidades del Modulo
==============================================

.. contents:: Contenido
 :local:
 :depth: 1

----

PUEDE Hacer
===========

.. list-table::
 :widths: 60 20 20
 :header-rows: 1

 * - Responsabilidad
   - UC Relacionado
   - CNST Aplicable
 * - Validar credenciales (username + password)
   - UC_001
   - CNST_005
 * - Generar token de autenticación con claims básicos
   - UC_001
   - CNST_005
 * - Registrar sesion en base de datos
   - UC_001
   - CNST_002
 * - Invalidar sesion previa (sesion unica)
   - UC_001
   - CNST_002
 * - Cerrar sesion y blacklist de token
   - UC_002
   - CNST_002
 * - Validar preguntas de seguridad
   - UC_003
   - CNST_001
 * - Generar contrasena temporal
   - UC_003
   - CNST_001
 * - Cambiar contrasena con validacion
   - UC_004
   - CNST_005
 * - Listar sesiones activas del usuario
   - UC_005
   - CNST_002
 * - Cerrar sesiones remotas
   - UC_005
   - CNST_002
 * - Aplicar timeout de 15 minutos
   - UC_005
   - CNST_002

----

NO PUEDE Hacer (Violaciones)
=============================

.. warning::

 Las siguientes acciones **violan la separacion de responsabilidades**
 y NO deben implementarse en este modulo:

- **Decidir si un usuario puede ver un modulo**

  - Ejemplo: "Si es ADMIN puede ver X modulo"
  - Responsabilidad de → :ref:`arq-mod-003`

- **Validar permisos especificos**

  - Ejemplo: "Si no tiene rol R017 no puede ver auditoria"
  - Responsabilidad de → :ref:`arq-mod-003`

- **Generar alertas por fallos de login**

  - Ejemplo: "Si falla 5 veces, generar alerta"
  - Responsabilidad de → :ref:`arq-mod-006`

- **Bloquear usuario por intentos fallidos**

  - La logica de bloqueo es de seguridad avanzada
  - Responsabilidad de → :ref:`arq-mod-003` (enforcers)

- **Enviar notificaciones por email**

  - Viola restriccion critica CNST_001
  - Solo se usa buzon interno → :ref:`arq-mod-006`

- **Registrar eventos de auditoria**

  - AUTH emite el evento, pero no lo registra
  - Responsabilidad de → :ref:`arq-mod-007`
