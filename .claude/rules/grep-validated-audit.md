```yml
type: Convención de Proyecto
category: Auditorías y Heurísticas de Grep
version: 1.0.0
created_at: 2026-05-19 20:55:43
updated_at: 2026-05-19 20:55:43
applies_to: IACT-docs v1.0.0+
origin_iniciativas:
  - implementar-uc-rpt-05-06-programacion-reportes
  - declarar-tst-ref-en-58-frs-sin-marcar
```

# Grep-Validated Audit — Protocolo obligatorio

> Cargado automáticamente. Aplica a TODA auditoría que use `grep`
> como heurística para afirmar presencia/ausencia de un patrón.

## Por qué existe esta regla

Durante la sesión 2026-05-19, dos auditorías producieron claims
falsos por **grep ciego** — el patrón buscado no contemplaba la
variabilidad real del corpus:

| # | Auditoría | Claim falso | Causa raíz |
|---|---|---|---|
| 1 | `auditar-cobertura-uc-implementacion` | "UC_RPT_05/06 sin implementación" | Asunción de mapping lineal docs `uc-NNN` ↔ código `UC_<DOM>_NN` |
| 2 | `auditar-conformidad-fr-tests-aceptacion` | "58/103 FRs sin TST ref" | Asunción de case (`TST-FR-` vs `TST-fr-`) |

Ambos claims se invalidaron al inspeccionar archivos del bucket
"negativo" — algo que debió hacerse **antes** de publicar el conteo.

Ambos eran claims **SPECULATIVE** disfrazados de PROVEN (el grep
"probó" 0 hits, pero la regex era incorrecta).

## Regla principal

**Antes de afirmar ausencia de un patrón en un corpus con grep:**

1. **Inspeccionar al menos un archivo del bucket "negativo"** que
   el grep clasificó como sin-patrón.
2. **Verificar visualmente** que el archivo efectivamente carece
   del concepto buscado — no solo del literal exacto.
3. **Si el archivo SÍ tiene el concepto pero con sintaxis distinta**,
   ampliar la regex y re-ejecutar antes de publicar.
4. **Reportar el grep exacto** que produjo el número en el documento
   de la auditoría.

## Protocolo paso a paso

### Paso 1 — Antes de grep ciego, enumerar variantes

Si buscás un marker, antes del grep:

- ¿Existe en uppercase? `UC_RPT_07`
- ¿En lowercase? `uc_rpt_07`
- ¿Mixed case? `Uc_Rpt_07`
- ¿Con guiones? `UC-RPT-07`
- ¿Con punto? `UC.RPT.07`
- ¿Con prefijo extra? `UC_INC_RPT_07`, `TST-FR-NNN.NN`

Si la respuesta es "no sé", **no asumas** — abre algunos archivos
del corpus y verifica el formato real antes de fijar la regex.

### Paso 2 — Grep amplio primero, refinar después

```bash
# CORRECTO — case-insensitive + alternativas conocidas
grep -irE "(TST-FR-|TST-fr-|tst_fr_)[0-9]" corpus/

# PROHIBIDO — case-sensitive + asunción ciega
grep -rE "TST-FR-[0-9]" corpus/
```

Si el grep amplio retorna más resultados que el estricto,
**investiga la diferencia** antes de descartar resultados.

### Paso 3 — Validar muestreando ambos buckets

Antes de publicar "N archivos con X, M archivos sin X":

```bash
# Tomar 1-2 muestras del bucket "con X"
xargs grep -l "PATTERN" archivos.txt | head -2 | xargs head -20

# Tomar 1-2 muestras del bucket "sin X"
xargs grep -L "PATTERN" archivos.txt | head -2 | xargs head -20
```

Verificar manualmente que la clasificación es correcta. Si la
muestra del bucket "sin X" **tiene el concepto** pero en otra
forma, **la regex está mal** — corrige antes de publicar.

### Paso 4 — Reportar el comando exacto

En el deep-analysis o iniciativa que publica el número, incluir
el bloque `.. code-block:: bash` con el comando exacto:

```rst
.. code-block:: bash

   cat /tmp/fr-all.txt | xargs grep -iE "TST-(fr|FR)-" \\
     | wc -l
   # => 103

```

Cualquier lector puede reproducir y descubrir el error si la
regex es defectuosa.

## Anti-patrones prohibidos

### AP-1 — Afirmar "0 hits" sin inspeccionar el corpus

```bash
grep -r "UC_RPT_05" apps/ | wc -l   # → 0
# Conclusión apresurada: "UC_RPT_05 sin implementar"
```

**Problema:** 0 hits puede significar (a) feature no implementada,
(b) implementada bajo otro marker, (c) implementada bajo otra
convención de naming.

**Solución:** antes de afirmar (a), inspeccionar el archivo o
módulo donde se espera la implementación y verificar si existe
bajo otra forma.

### AP-2 — Asumir linearidad en mappings numéricos

```bash
# Docs: uc-032, uc-033, ..., uc-047
# Código: UC_RPT_01, UC_RPT_02, ..., UC_RPT_17
# Asunción: uc-032 = UC_RPT_01, uc-033 = UC_RPT_02, ...
```

**Problema:** los códigos pueden saltarse números (deprecaciones,
reservas) y los docs pueden agregar UCs entre versiones. La
correspondencia no es lineal a menos que se valide por
descripción textual.

**Solución:** extraer la descripción textual del marker (después
del `—` o en el docstring) y compararla con el nombre del UC en
docs.

### AP-3 — Case-sensitive sin validar la convención del corpus

```bash
grep -r "TST-FR-" archivos.rst | wc -l
```

**Problema:** si el corpus mezcla `TST-FR-` y `TST-fr-`, el grep
case-sensitive cuenta solo una mitad.

**Solución:** `grep -i` por default en auditorías, y solo
case-sensitive cuando se haya validado que el corpus es uniforme.

### AP-4 — Publicar conteos sin reproducibilidad

Decir "encontré 58 archivos sin X" sin documentar el comando
exacto deja al lector sin forma de validar. Es claim SPECULATIVE
performativo (suena PROVEN pero no es reproducible).

**Solución:** todo conteo en un artefacto debe ir acompañado del
comando que lo produjo, en bloque `code-block:: bash`.

## Clasificación de claims por grep

Combina con `evidence-classification.md` (PROVEN / INFERRED /
SPECULATIVE):

| Tipo de claim | Calificación |
|---|---|
| "X aparece N veces" con comando explícito reproducible y muestra del corpus inspeccionada | PROVEN |
| "X aparece N veces" con comando explícito, sin muestra inspeccionada | INFERRED |
| "X no aparece" sin muestra del bucket negativo inspeccionada | **SPECULATIVE** |
| "X no se implementa" basado en 0 hits sin investigar alternativas | **SPECULATIVE** |
| Mapping derivado por linearidad numérica sin validación textual | **SPECULATIVE** |

Claims SPECULATIVE bloquean gates Stage → Stage por I-012 de
`thyrox-invariants.md`.

## Lista de verificación pre-publicación

Antes de publicar un conteo o claim "sin X" en una auditoría:

- [ ] Comando grep exacto documentado en el artefacto
- [ ] Comando es case-insensitive O justificación de por qué
      case-sensitive es correcto
- [ ] Al menos 1 muestra del bucket positivo inspeccionada
- [ ] Al menos 1 muestra del bucket negativo inspeccionada
- [ ] Variantes de naming consideradas (uppercase, lowercase,
      mixed, separadores)
- [ ] Si hay mapping entre dos corpus, validado por descripción
      textual, no por linealidad numérica

Si alguna casilla no está marcada, el claim queda SPECULATIVE
hasta cerrarla.

## Casos históricos documentados

### 2026-05-19: UC_RPT_05/06 falsos gaps

`auditar-cobertura-uc-implementacion/deep-analisis-*` reportó
"UC_RPT_05/06 sin implementación". La iniciativa
`implementar-uc-rpt-05-06-programacion-reportes` descubrió que
los UCs documentados `uc-036/uc-037` están implementados bajo
markers `UC_RPT_07/UC_RPT_08` (gap de numeración en código).

Causa raíz: asunción implícita de mapping lineal
`uc-032 + offset = UC_RPT_01 + offset`. El código salta del 04
al 07 sin documentación de la razón.

### 2026-05-19: 58 FRs falsos sin TST

`auditar-conformidad-fr-tests-aceptacion` reportó "58/103 FRs
sin TST ref". La iniciativa
`declarar-tst-ref-en-58-frs-sin-marcar` descubrió que los 58
usan `TST-fr-NNN-NN` (lowercase) en lugar de `TST-FR-NNN.NN`
(uppercase). Los 103 declaran TST ref.

Causa raíz: case-sensitive grep sobre corpus con dos
convenciones de naming coexistentes por dominio.

## Relación con otras reglas

- **`calibration-verified-numbers.md`**: complementaria —
  esta regla ataca el caso especial donde el "verificable"
  parece serlo pero la regla es defectuosa.
- **`thyrox-invariants.md`** I-012: claims SPECULATIVE no
  avanzan gates. Esta regla agrega criterios para detectar
  SPECULATIVE camuflado de PROVEN.
- **`evidence-classification.md`** (referencia en
  skills/thyrox): la tabla de clasificación arriba extiende
  los criterios para el caso grep.
