```yml
created_at: 2026-04-30 00:30:00
project: IACT-docs
work_package: 2026-04-30-00-07-08-rbac-functions-count-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Auditoria conteo de funciones — Resultado: 42 es CORRECTO

## Conclusion

**El conteo "42 funciones" del modelo RBAC IACT v5.2.1 es
CORRECTO y CONSISTENTE.** La sospecha del ejecutor era infundada
(falsa alarma documentada).

La matriz RACI, ADR-GOB-009, ADR-BACK-006, CNST-029/033 y todos
los artefactos derivados estan **correctamente calibrados**.

## Evidencia (3 fuentes verificadas)

### Fuente 1: Suma de cifras declaradas por seccion (modelo § 3)

```
3.1 MOD_Auth      (4 funciones)
3.2 MOD_Users     (9 funciones)
3.3 MOD_Access    (5 funciones)
3.4 MOD_Pipeline  (4 funciones)
3.5 MOD_Reports   (8 funciones)
3.6 MOD_Alerts    (6 funciones)
3.7 MOD_Audit     (4 funciones)
3.8 MOD_Logs      (2 funciones)
                 ----
                  42  ✓
```

### Fuente 2: Filas en seed SQL § 8.8

```bash
$ sed -n '/^8\.8 Datos Iniciales - 42 Funciones/,/^8\.9/p' \
    source/arquitectura-tecnica/rbac/modelo-rbac-iact.rst | \
    grep -oE "(AUTH|USR|ACC|PIP|RPT|ALR|AUD|LOG)-[0-9]{3}" | wc -l
42  ✓
```

Suma por prefijo:

```
AUTH-001..004   (4)
USR-001..009    (9)
ACC-001..005    (5)
PIP-001..004    (4)
RPT-001..008    (8)
ALR-001..006    (6)
AUD-001..004    (4)
LOG-001..002    (2)
                ----
                 42  ✓
```

### Fuente 3: IDs unicos via grep generico (44 = falsa alarma)

Un grep generico inicial encontro 44 IDs unicos (no 42). Los 2
extras eran:

- ``USR-010`` — aparece SOLO en la frase
  ``"- Sin función USR-010 (eliminada en v5.2.0)"``
- ``ACC-006`` — aparece SOLO en la frase
  ``"- Sin función ACC-006 (eliminada en v5.2.0)"``

**Ambas son negaciones explicitas** que documentan que esas
funciones NO existen en v5.2.1 (se eliminaron al pasar de v5.2.0
a v5.2.1). El grep las conto como menciones positivas — falso
positivo.

## Lecciones

1. **Cifras consistentes en 3 fuentes independientes** (titulos
   de seccion + filas seed SQL + IDs unicos -2 anotaciones
   historicas) = **42 funciones**.

2. **Las anotaciones "Sin funcion X (eliminada en v5.2.0)"** son
   utiles para trazabilidad historica pero pueden confundir
   lecturas automatizadas. Documentado como caveat.

3. **La matriz RACI creada en Z.1** esta correctamente calibrada
   contra 42 funciones. NO requiere actualizacion.

## Auditoria de cifras derivadas en otros artefactos (cross-check)

.. (informacion duplicada en seccion siguiente)

| Artefacto | Cita "42 funciones" | Status |
|-----------|---------------------|--------|
| modelo-rbac-iact (v5.2.1) | titulo § 4.1, § 8.8, § 12.1 | Correcto |
| raci-rbac-iact (Z.1) | secciones 3.1-3.8 (8 sub-tablas con 42 entries) | Correcto |
| adr-gob-009-rbac-modelo-conceptual (Z.1) | § 2.1 punto 3 | Correcto |
| adr-back-006-rbac-estrategia-implementacion (Z.1) | (sin cifra explicita) | N/A |
| ADR-GOB-008 | § "Vista funcional MOD_Access" | Correcto |
| CNST-033 § 1.2 Justificacion | "MODELO_RBAC_IACT_v5_2_1" | Correcto |
| Glosario § H | "42 funciones + 10 grupos AGR-001..010 + 3 SoD" | Correcto |
| SBVR-01 | "42 funciones atomicas + 10 grupos AGR-001..010 + 3 SoD" | Correcto |
| MTM-03 § 1 | "modelo NIST RBAC Flat" + suma | Correcto |

Todos los artefactos del corpus citan 42 funciones consistentemente.

## Recomendacion (preventiva)

Para evitar futuras falsas alarmas, podria agregarse al modelo
v5.2.1 una **nota explicita en § 3** indicando:

   "Las anotaciones del tipo 'Sin funcion USR-010 (eliminada en
   v5.2.0)' son trazabilidad historica de funciones eliminadas
   en la migracion v5.2.0 -> v5.2.1. NO son funciones del
   catalogo vigente. El catalogo definitivo son las 42 funciones
   listadas en § 3.1-3.8 + § 8.8."

Esta nota ayudaria a future-proofing contra interpretaciones
erroneas. **OPCIONAL** — no es deuda critica.

## Cierre Z.1.C

Z.1.C cierra sin cambios al corpus. La sospecha era infundada;
el conteo "42" es correcto en 3 fuentes independientes.

**Tiempo total Z.1.C:** ~20 min (auditoria pura, sin
modificaciones).
