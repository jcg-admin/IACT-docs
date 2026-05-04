```yml
created_at: 2026-05-04 04:22:56
updated_at: 2026-05-04 04:35:00
project: IACT-docs
author: NestorMonroy
status: Aprobado
version: 1.1.0
```

# ADR: Estrategia de Edicion de FRs — Quirurgica vs. Reescritura Total

## Contexto

Durante el trabajo de documentacion de FRs (Functional Requirements) en
`source/requisitos/`, surgio la necesidad de corregir FRs con diferentes
grados de completitud. Dos patrones de edicion emergieron como optimos
segun el estado del FR.

## Protocolo completo — Antes de tocar cualquier FR

Estos pasos son obligatorios en orden:

1. **Leer el UC** — entender QUE debe documentar el FR antes de tocar nada.
2. **Leer el FR actual** — ver exactamente que hay, que esta bien y que esta mal.
3. **Decidir el enfoque** (ver Decision abajo).
4. **Aplicar el cambio.**
5. **Verificar el resultado** — leer el archivo modificado y confirmar que el
   cambio quedo como se esperaba antes de hacer commit.

No saltarse los pasos 1, 2 y 5. La verificacion previa al commit es obligatoria.

## Decision

La estrategia de edicion se elige segun el estado del FR:

### Caso A — Edicion quirurgica (`Edit` / `str_replace`)

**Cuando:** El FR ya tiene estructura aceptable y solo una seccion esta mal.

**Criterios para elegir este caso:**
- La identificacion del FR es correcta
- Los escenarios BDD tienen datos concretos
- La trazabilidad esta presente
- Solo hay un bloque especifico incorrecto (ej. codigo Python en descripcion)

**Accion:** Reemplazar solo la seccion problematica. No tocar lo que esta bien.

**Ejemplo aplicado:** `FR-COM-01.02`, `FR-COM-02.02`, `FR-COM-03.02` — solo
el bloque `code-block:: python` dentro de la descripcion fue reemplazado por
prosa; el resto se preservo intacto.

### Caso B — Reescritura total (`Write`)

**Cuando:** El FR es tan delgado que no hay nada que salvar.

**Criterios para elegir este caso:**
- La declaracion copia literalmente el titulo sin aportar contenido
- Los escenarios son genericos sin datos concretos
- Faltan 4 o mas de las 6 secciones obligatorias
- La estructura completa seria mas lenta de rescatar que de reescribir

**Accion:** Reescritura completa del archivo con todas las secciones.

**Ejemplo aplicado:** FRs del batch `notifications/` — `NOT-01.02` tenia 103
lineas, declaracion copiada literalmente, escenarios genericos, y le faltaban
5 de 6 secciones obligatorias.

### Caso C — Mixto (`Edit` para secciones malas + adiciones para secciones faltantes)

**Cuando:** El FR tiene algunas secciones buenas y otras completamente ausentes.

**Criterios para elegir este caso:**
- Hay al menos 2 secciones con contenido valido
- Hay al menos 1 seccion completamente ausente (no solo incompleta)
- No conviene reescribir todo porque se perderia el contexto valido existente

**Accion:** `Edit` (str_replace) para corregir lo que esta mal + agregar
las secciones faltantes al final o en la posicion correcta.

**Regla:** No usar Caso B si se puede salvar mas de la mitad del FR existente.

## Regla de contenido de FRs

Los FRs documentan **QUE** hace el sistema y **POR QUE**, nunca **COMO**.

- **Permitido:** Pseudocodigo, lenguaje natural estructurado, diagramas
- **Prohibido:** Codigo Python real, SQL ejecutable, comandos shell, batch
- **Prohibido:** Bloques `code-block:: python` en secciones de descripcion
  o comportamiento (solo permitido en seccion de testing como referencia de
  implementacion, no como especificacion del comportamiento)

Si la logica es compleja, se describe en lenguaje natural estructurado:

```
CUANDO el sistema detecta N intentos fallidos consecutivos
  Y el periodo es inferior a T minutos
ENTONCES bloquear el acceso temporalmente
  Y registrar el evento en audit_log
  Y notificar al usuario via InternalMailbox
```

No:

```python
if attempts >= MAX_ATTEMPTS and delta < LOCKOUT_WINDOW:
    user.locked = True
    audit_log.record(...)
```

## Consecuencias

- Ediciones mas rapidas y seguras: se toca solo lo que esta mal
- Trazabilidad preservada en FRs que ya tenian estructura valida
- FRs nuevos/delgados se reescriben completos desde el template
- Eliminacion de dependencias de implementacion en especificaciones

## Referencias

- `source/requisitos/` — directorio de FRs
- Template de FR: `.claude/skills/thyrox/assets/fr-template.md` (si existe)
- Regla STD_010: abstraccion de vocabulario en documentacion
