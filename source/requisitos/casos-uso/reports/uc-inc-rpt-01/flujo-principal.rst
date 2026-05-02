.. _uc-inc-rpt-01-parte-03:

==========================
Parte 3 — Flujo principal
==========================

Este UC es ejecutado como paso de inclusion dentro de los
UCs de reporte (UC_RPT_01..UC_RPT_17).

PASO 1 — El sistema consulta la configuracion RBAC del usuario
          para obtener los DIDs IVR asignados.

PASO 2 — El sistema mapea cada DID a su segmento:

  - DID ``19028031`` → segmento ``nacional_A``
  - DID ``19020001`` → segmento ``nacional_B``
  - DID ``19020084`` → segmento ``Puebla``

PASO 3 — El sistema retorna la lista de segmentos accesibles.

  - Si el usuario tiene acceso a todos los DIDs (o el
    permiso de administrador global), retorna los tres
    segmentos.
  - Si el usuario no tiene ningun DID asignado y no es
    administrador: retorna error EX-02 (sin segmento).

El resultado de PASO 3 se usa como filtro en la consulta
al Servicio de Reportes del UC invocador.
