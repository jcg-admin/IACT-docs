.. _uc-inc-rpt-01-parte-05:

========================
Parte 5 — Excepciones
========================

5.1 EX-01: JWT invalido o expirado
====================================

PASO 1 no puede obtener el usuario autenticado.
Respuesta: 401 UNAUTHORIZED. El UC invocador
propaga el error al cliente.

5.2 EX-02: Usuario sin segmento asignado
==========================================

PASO 3 — el usuario no tiene ningun DID asignado
y no es administrador global. Respuesta: 400
USER_WITHOUT_SEGMENT con mensaje "El usuario no
tiene segmentos asignados. Contacte al administrador."

5.3 EX-03: Error de acceso al servicio RBAC
=============================================

PASO 1 — el servicio RBAC no responde en el
timeout configurado. Respuesta: 503 SERVICE_UNAVAILABLE.
El UC invocador no puede continuar — propaga el error.

5.4 EX-04: Error de acceso a la tabla de mapeo
================================================

PASO 2 — la tabla DID→segmento no esta disponible.
Respuesta: 503 SERVICE_UNAVAILABLE con detalle del
error de infraestructura. Se registra en audit log.
