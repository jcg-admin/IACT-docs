.. _arq-mod-001-restricciones:

==============================================
ARQ_MOD_001 — Restricciones Aplicables
==============================================

.. list-table::
 :widths: 15 85
 :header-rows: 1

 * - CNST
   - Descripcion y Aplicacion
 * - CNST_001
   - **Comunicaciones Prohibidas**: No enviar email para recuperacion.
     Usar preguntas de seguridad + buzon interno.
 * - CNST_002
   - **Gestion Sesiones BD**: Sesiones en base de datos relacional, no caché en memoria.
     Sesion unica por usuario. Timeout 15 min. Validar IP+UA.
 * - CNST_005
   - **Seguridad API REST**: token de autenticación con librería de tokens. Lista negra de tokens.
     HTTPS obligatorio.
