.. _uc-log-06-parte-10:

==========================
Parte 10 — Patrones
==========================

Reuso P-15, P-29.

P-81 (nuevo): Health check con degradacion
controlada — un servicio sin respuesta NO
debe causar 5xx en el endpoint health
check; reportar ``unknown`` permite a
SRE distinguir "no se sabe" vs "se sabe
que esta caido".
