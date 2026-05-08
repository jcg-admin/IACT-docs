```yml
created_at: 2026-05-07 18:00:00
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 10 — EXECUTE
author: NestorMonroy
status: Borrador
version: 1.0.0
type: T-VERIFY Protocol
```

# T-VERIFY — Protocolo de verificacion semantica

## 1. Criterio binario por archivo

Para cada archivo clase A:

1. Leer ``flujo-principal.rst`` del UC consumidor.
2. Leer el bloque ``@startuml..@enduml`` del diagrama.
3. Pregunta:

   *El diagrama refleja **fielmente** el flujo principal del UC?*

   - **Si:** queda clasificado A. Se marca [x] en task-plan
     sin commit.
   - **No:** reclasifica a B. Se crea T-CO-EX-NN con la
     correccion necesaria, ejecutado inmediatamente.

## 2. Sampling por UC (eficiencia)

Dado que cada UC tiene 1-5 diagramas hermanos que comparten
contexto semantico, la verificacion se hace **por UC**:

1. Para cada UC con archivos clase A: leer el
   ``flujo-principal.rst`` UNA vez.
2. Verificar el archivo mas representativo (orden de
   prioridad: ``caso-de-uso`` > ``secuencia`` > ``actividad``
   > ``estados``).
3. Si el archivo representativo refleja fielmente el flujo:
   los hermanos tambien lo hacen (mismo dominio semantico,
   verificado por T-003 mecanicamente).
4. Si no: investigar todos los hermanos.

## 3. Casos especiales

- Archivos sin UC consumidor directo (e.g.,
  ``diagrama-de-estados-{entidad}.rst`` para entidades
  RBAC en uc-perm-04/05) — ya complementados en T-CO-38/39
  con seealso a domain-model. Ejes UML-07 cumplidos
  mecanicamente.

- ``diagrama-de-impacto.rst`` y otros sub-tipos especiales —
  validar contra el contexto especifico del UC, no contra
  flujo-principal.

## 4. Output

Un solo archivo ``track/verify-report.md`` con tabla:

| UC | Archivo representativo | Veredicto | Hermanos OK? | Notas |
|---|---|---|---|---|

## 5. Reclasificaciones

Si una verificacion produce reclasificaciones B, se ejecutan
T-CO-EX-NN inmediatamente (1 commit por reclasificacion) en
lugar de batchearlas.
