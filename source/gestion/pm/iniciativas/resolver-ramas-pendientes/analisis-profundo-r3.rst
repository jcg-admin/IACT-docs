.. meta::
   :artefacto: ANALISIS-PROFUNDO-R3
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-ramas-pendientes
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:46:00
   :ultimo_cambio: 2026-05-18T18:46:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _analisis-profundo-r3:

============================================================
Analisis Profundo: Rama R3 (backup-20260517_021658)
============================================================

Contexto
========

R3 = ``integration/backup-20260517_021658``. ahead=1,
behind=705 vs develop. Un commit unico ``bc112cfd``
"feat(docs): portar delta de backup 20260517_021658
(21 nuevos + 92 modificados)". Merge-base ``44bfd900``.

Hallazgo: patron INVERSO al esperado
=====================================

La hipotesis previa era: "R3 esta behind 705, los 68 que
difieren seran versiones viejas (ruido obsoleto)". **Los datos
la refutan**:

* De 68 archivos ``source/`` que difieren: **68 tienen R3 mas
  reciente** (2026-05-17) que develop (2026-05-05..05-09).
  **0 tienen develop mas reciente.**
* R3 no es una rama de trabajo antigua: es un *port-delta de
  backup* del 17-mayo que porto contenido mas completo que el
  de develop en esos archivos.

Leccion: la fecha/posicion ``behind`` no determina por si sola
si una rama aporta. R3 esta behind por no haberse integrado,
pero su contenido es posterior. Verificar siempre con datos,
no asumir por ``behind``.

Contenido de R3
===============

**8 archivos NUEVOS** (ausentes en develop), sustantivos:

.. list-table::
   :header-rows: 1
   :widths: 70 15 15

   * - Archivo
     - Lineas
     - Naturaleza
   * - ``arquitectura-tecnica/rbac/modelo-rbac-iact.rst``
     - 2897
     - Modelo RBAC completo
   * - ``normativa/restricciones/cnst-030-...-sod.rst``
     - 334
     - Restriccion SoD
   * - ``casos-uso/access/uc-acc-01/diagramas-uml.rst``
     - 291
     - Diagramas UML UC
   * - ``casos-uso/access/uc-acc-03/diagramas-uml.rst``
     - 228
     - Diagramas UML UC
   * - ``casos-uso/access/uc-acc-04/diagramas-uml.rst``
     - 254
     - Diagramas UML UC
   * - ``casos-uso/access/uc-acc-05/diagramas-uml.rst``
     - 177
     - Diagramas UML UC
   * - ``casos-uso/access/uc-acc-08/diagramas-uml.rst``
     - 225
     - Diagramas UML UC
   * - ``casos-uso/permissions/uc-perm-06/diagramas-uml.rst``
     - 200
     - Diagramas UML UC

**68 archivos que difieren** con R3 mas reciente: ADRs de
backend/devops/frontend, indices, etc. (muestra: adr-back-004,
adr-devops-001/003, devops/index.rst, adr-front-002).

**33 archivos identicos** a develop: ya integrados, no aportan.

Riesgo pendiente de verificar (NO integrar a ciegas)
=====================================================

R3 es un *port-delta de backup*. Dos preguntas criticas sin
resolver antes de decidir rescate:

1. **Relacion con PR #20**: hubo un PR #20
   (``feature/restore-devops-infra-pm-docs``, merge
   ``22a9c66f``) que integro un port-delta del **mismo backup**.
   ¿R3 es un intento duplicado/paralelo, o un delta distinto/
   complementario? Si PR #20 ya integro parte, hay que
   delimitar que parte cubre R3.

2. **Vigencia de nomenclatura/modelo**: R3 es del 17-mayo pero
   develop tiene 705 commits adicionales. Riesgo concreto:
   ``modelo-rbac-iact.rst`` (2897 lineas) podria usar el
   modelo RBAC v5.2.1 FK binario (deprecado) en vez del v5.4.0
   M2M vigente. Integrar contenido con modelo obsoleto seria
   deuda, no rescate.

Estado: analisis de inventario completo. Decision de rescate
**supeditada** a resolver los dos riesgos. No se rescata a
ciegas (leccion de R1: contenido aparentemente valioso puede
arrastrar nomenclatura/modelo obsoleto).

Verificacion siguiente
======================

* Comparar contenido sustantivo de muestra de los 68 (R3 vs
  develop): ¿mejora real o solo formato?
* Revisar ``modelo-rbac-iact.rst`` de R3: ¿v5.4.0 M2M o v5.2.1
  FK binario?
* Determinar relacion R3 vs PR #20 (que delta cubre cada uno).
