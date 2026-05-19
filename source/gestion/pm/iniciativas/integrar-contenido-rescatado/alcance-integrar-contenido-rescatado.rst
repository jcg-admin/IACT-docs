.. meta::
   :artefacto: ALCANCE-INTEGRAR-CONTENIDO-RESCATADO
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/integrar-contenido-rescatado
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T23:37:34
   :ultimo_cambio: 2026-05-18T23:37:34
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-integrar-contenido-rescatado:

==================================================
Alcance: Integrar el contenido rescatado a source/
==================================================

Por que existe
==============

Al cerrar ``resolver-ramas-pendientes`` se registro la deuda
formal DEBT-008..011: contenido con valor de R2/R3 preservado
pero no integrado a ``source/``. Mientras no se integre, ese
contenido no es parte del producto vivo. Esta iniciativa
resuelve la parte verificable como correcta (DEBT-008 y
DEBT-009).

Criterio de completitud verificable
=====================================

* Los 12 archivos de la spec UC-SUP-01 de R2 estan en
  ``source/requisitos/casos-uso/supervision/uc-sup-01/``,
  reemplazando los stubs, con hash verificado contra la rama
  origen.
* Los 8 archivos nuevos de R3 estan en su ubicacion de
  ``source/`` y cada uno enlazado en el toctree de su seccion
  (cero huerfanos).
* El build ``sphinx-build -W -j 2`` produce 0 warnings con el
  contenido integrado (lo verifica el usuario en su local;
  ver nota de verificacion).
* DEBT-008 y DEBT-009 quedan marcadas como resueltas; DEBT-010
  y DEBT-011 siguen activas (out-of-scope, ver Analisis).

In-scope
========

* Integrar R2 spec UC-SUP-01 (12 archivos, riesgo bajo):
  reemplazo de stubs por contenido completo.
* Integrar R3 nuevos (8 archivos, riesgo medio): creacion +
  enlace en toctree de su seccion.
* Verificacion de hash de cada archivo contra su rama origen
  (R2 ``43250b49`` / R3 ``bc112cfd``).
* Actualizacion del registro de deuda (DEBT-008/009 ->
  resueltas).

Out-of-scope
============

* R3 que difieren (68 archivos, riesgo alto): requieren
  analisis de sustancia archivo por archivo. Siguen como
  **DEBT-010 activa**. Integrarlos en bloque seria incorrecto.
* R1 ``architecture-constraints.md``: md/ingles/borrador;
  requiere transformacion, no copia. Sigue como **DEBT-011
  activa**.
* La **verificacion de build**: la ejecuta el usuario en su
  local. El clon de trabajo no completa el build (PlantUML).

Nota de verificacion (restriccion conocida)
============================================

La integracion se prepara y commitea en el clon con hash
verificado y toctrees enlazados, pero la verificacion
``sphinx-build -W -j 2`` = 0 warnings la ejecuta el usuario en
su local ANTES del push (PROC-GOB-013 Fase 3 paso 5). No es
deuda oculta: es una restriccion de entorno documentada. El
modo de fallo principal (huerfano por toctree) se previene
verificando el enlace de cada archivo nuevo en el mismo paso
de su integracion.

Decisiones de contenido tomadas durante la lectura
====================================================

* El contenido se toma de las ramas origen R2/R3 del remoto
  (origen de verdad), no de ``wp-tmp/``, para no acoplar esta
  iniciativa con ``resolver-ramas-pendientes``.
* Tipo: documental (operacion sobre ``source/`` de
  IACT-docs, sin PMBOK).
* Rama limpia desde develop, independiente de las dos
  iniciativas anteriores.
