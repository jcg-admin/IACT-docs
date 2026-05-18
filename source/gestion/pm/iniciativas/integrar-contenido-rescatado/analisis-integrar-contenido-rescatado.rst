.. meta::
   :artefacto: ANALISIS-INTEGRAR-CONTENIDO-RESCATADO
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/integrar-contenido-rescatado
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T23:37:34
   :ultimo_cambio: 2026-05-18T23:37:34
   :autor: NestorMonroy
   :clasificacion: Interno

.. _analisis-integrar-contenido-rescatado:

============================================================
Analisis: Integrar el contenido rescatado a source/
============================================================

Origen
======

Deuda formal DEBT-008..011
(:doc:`/risks-technical-debt/deuda-integracion-wp-tmp`),
generada al cerrar ``resolver-ramas-pendientes``. El analisis
de **como** integrar ya se hizo alli
(``analisis-integracion-wp-tmp``); este documento lo
operacionaliza como iniciativa propia con alcance acotado.

Decision de origen del contenido (correccion de enfoque)
=========================================================

``wp-tmp/`` fue un repositorio de paso; vive solo en la rama
``resolver-ramas-pendientes``, no en develop. Tomar el
contenido desde ``wp-tmp/`` acoplaria esta iniciativa a que
aquella se integre primero.

**Decision**: el contenido se toma directamente de las ramas
origen en el remoto, que existen de forma independiente:

* R2 = ``feature/arquitectura-tecnica-content``
  (``43250b49``)
* R3 = ``integration/backup-20260517_021658`` (``bc112cfd``)

Es el origen de verdad (``wp-tmp/`` era copia verificada por
hash de estas). Elimina la dependencia entre iniciativas y
permite verificar hash contra la rama origen al integrar.

Alcance acotado (integrar SOLO lo verificable como correcto)
=============================================================

El analisis previo clasifico el contenido en 4 grupos por
riesgo. Integrar los 89 en bloque seria **incorrecto**. Esta
iniciativa integra unicamente lo que se puede integrar bien
con certeza:

.. list-table::
   :header-rows: 1
   :widths: 14 10 30 46

   * - Grupo
     - N
     - Riesgo
     - Decision para ESTA iniciativa
   * - R2 spec UC-SUP-01
     - 12
     - BAJO
     - **IN-SCOPE**. develop tiene stubs (10-19 lin),
       R2 spec completa (90-358). Nomenclatura ya
       correcta, ruta existente.
   * - R3 nuevos
     - 8
     - MEDIO
     - **IN-SCOPE**. Ausentes en develop; cada uno se
       enlaza en su toctree o genera huerfano.
   * - R3 difieren
     - 68
     - ALTO
     - **OUT-OF-SCOPE**. "Mas reciente por fecha" no es
       "mejor"; requiere analisis de sustancia archivo
       por archivo. Integrar en bloque seria incorrecto.
   * - R1 architecture-constraints
     - 1
     - —
     - **OUT-OF-SCOPE**. md/ingles/borrador obsoleto;
       requiere transformacion, no copia.

Lo out-of-scope NO se silencia: queda como deuda viva en
DEBT-010 (R3 difieren) y DEBT-011 (R1), ya registradas. Esta
iniciativa resuelve DEBT-008 (R2) y DEBT-009 (R3 nuevos);
DEBT-010/011 siguen activas para una fase posterior con su
propio analisis de sustancia.

Estrategia de integracion correcta (por archivo)
=================================================

Para cada archivo in-scope:

1. Obtener el contenido de la rama origen (R2/R3) y verificar
   su hash de objeto git (debe coincidir con lo analizado).
2. Determinar destino real en ``source/`` y si existe toctree
   que ya lo referencia.
3. Si el destino existe (R2 stubs): reemplazar.
   Si es nuevo (R3): crear y **enlazarlo en el toctree** de
   su seccion (un archivo sin enlazar = warning de huerfano,
   el modo de fallo principal).
4. Verificacion de build ``sphinx-build -W -j 2`` = 0
   warnings antes de commitear el grupo.

Modo de fallo principal y su prevencion
========================================

Anadir un archivo sin enlazarlo en un toctree genera
"document isn't included in any toctree" (warning -> con
``-W`` rompe el build). Por eso cada archivo nuevo (R3) exige
verificar/crear su entrada de toctree en el mismo paso. Es la
causa de deuda mas probable y el analisis la previene
explicitamente.

Criterio de integracion correcta
================================

* Cero archivos huerfanos (todo nuevo enlazado en toctree).
* Cero retroceso (no sobrescribir develop con contenido
  inferior; R2 verificado stub->completo, no al reves).
* Hash verificado contra rama origen (no integrar algo
  distinto a lo analizado).
* Build 0 warnings por grupo antes de commit.
* Nomenclatura vigente (R2 ya correcta; R3 nuevos
  verificados, incl. ``modelo-rbac-iact.rst`` v5.4.0 M2M).
