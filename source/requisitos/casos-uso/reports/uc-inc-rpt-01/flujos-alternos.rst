.. _uc-inc-rpt-01-parte-04:

==========================
Parte 4 — Flujos alternos
==========================

4.1 FA-01: Usuario con acceso a un solo segmento
=================================================

PASO 2 retorna un unico DID. El filtro resultante
restringe la consulta al segmento correspondiente.
El UC invocador recibe lista con un elemento.

4.2 FA-02: Administrador global
================================

Usuario con permiso ``view_all_segments``. PASO 2
omite el filtro por DID y retorna los tres segmentos
sin restriccion.

4.3 FA-03: Nuevo DID no mapeado
================================

PASO 2 detecta un DID sin segmento asignado en la
tabla de mapeo. El DID se ignora en el filtro. Se
emite log de advertencia para revision del administrador.
El UC invocador continua con los segmentos validos
restantes.
