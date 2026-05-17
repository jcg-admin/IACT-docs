.. _uc-rpt-16-parte-10:

==========================
Parte 10 — Patrones
==========================

Reuso P-15, P-25, P-29, P-51, P-58.

P-74 (nuevo): Triple SP por sub-vista

- Cada vista del reporte (redirigidos /
  menu_centro / errores) mapea a un SP
  distinto en BD_IVR.
- Backend solo dispatcha vista → SP y
  parsea filas. Sin path mining ni
  agregacion en codigo.
- Trade-off: cualquier nuevo breakdown
  requiere un SP nuevo en BD_IVR; la
  complejidad de agregacion vive en el
  SP, no en el servicio Python.
