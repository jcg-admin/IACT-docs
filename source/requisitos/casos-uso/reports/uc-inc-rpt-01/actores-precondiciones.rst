.. _uc-inc-rpt-01-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

Actores
-------

Este UC no tiene actores propios — es invocado como paso
interno de otro UC (``<<include>>``). El actor del UC
invocador (Analista de Datos, Supervisor, Administrador)
es el actor transitivo.

Precondiciones
--------------

- El usuario esta autenticado (JWT valido).
- El usuario tiene al menos un permiso de tipo
  ``view_*_reports``.

Postcondiciones
---------------

- Se retorna la lista de segmentos IVR accesibles para
  el usuario (minimo 1, maximo 3).
- Si el usuario tiene acceso total (administrador),
  se retorna la lista completa de segmentos.
