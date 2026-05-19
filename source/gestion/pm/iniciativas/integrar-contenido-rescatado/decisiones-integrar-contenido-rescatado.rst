.. meta::
   :artefacto: DECISIONES-INTEGRAR-CONTENIDO-RESCATADO
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/integrar-contenido-rescatado
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T23:37:34
   :ultimo_cambio: 2026-05-18T23:37:34
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-integrar-contenido-rescatado:

==================================================
Decisiones: Integrar el contenido rescatado
==================================================

Decisiones de diseno
====================

D1 — Origen del contenido: ramas R2/R3, no wp-tmp/
---------------------------------------------------

``wp-tmp/`` vive solo en la rama ``resolver-ramas-pendientes``,
no en develop. Tomar de ``wp-tmp/`` acoplaria esta iniciativa a
que aquella se integre primero. Se toma de las ramas origen
R2 (``43250b49``) / R3 (``bc112cfd``) del remoto: es el origen
de verdad (``wp-tmp/`` era copia verificada por hash de estas)
y existen independientemente. Alternativa descartada: rama
desde ``resolver-ramas-pendientes`` (acoplamiento de orden de
integracion).

D2 — Alcance acotado a lo verificable como correcto
----------------------------------------------------

Solo R2 (12, riesgo bajo) y R3 nuevos (8, riesgo medio)
in-scope. R3 difieren (68, riesgo alto) y R1 (transformacion)
out-of-scope, siguen como DEBT-010/011 activas. Integrar los
89 en bloque seria integrar incorrectamente: 68 sin analisis
de sustancia y 1 que contradice la politica RST-only. Acotar
no deja deuda oculta: la deuda out-of-scope ya esta registrada
formalmente.

D3 — Una tarea por archivo; toctree en el mismo paso
-----------------------------------------------------

Cada archivo es una tarea atomica. Para los nuevos (R3), la
creacion y el enlace en el toctree de su seccion van en la
MISMA tarea. Razon: un archivo nuevo sin enlazar genera
"document isn't included in any toctree" (warning -> con
``-W`` rompe el build). Separar creacion y enlace dejaria una
ventana de huerfano.

D4 — Verificacion de build delegada al usuario
-----------------------------------------------

El clon de trabajo no completa ``sphinx-build`` (PlantUML se
cuelga; verificado toda la sesion). La preparacion (copia con
hash + toctree) se hace y commitea en el clon; la verificacion
``-W -j 2`` = 0 warnings la ejecuta el usuario en su local
antes del push. No es deuda oculta: es restriccion de entorno
documentada en el Alcance. El criterio de "integracion
correcta" incluye esta verificacion como paso del usuario, no
como algo omitido.

Hallazgos surgidos durante la ejecucion
========================================

(Se completara durante la ejecucion de la integracion.)

Verificacion post-ejecucion con evidencia
==========================================

(Se completara al cierre, con tabla criterio del
alcance / PASA-FALLA / evidencia, conforme PROC-GOB-013
Fase 5 Paso 3. Incluira el resultado de build reportado por
el usuario.)
