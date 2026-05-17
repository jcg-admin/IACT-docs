```yml
created_at: 2026-05-05 04:12:45
project: THYROX
work_package: 2026-05-05-04-12-45-alias-fix-uc-numericos
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP alias-fix-uc-numericos — Scope Analysis

## Problema

Dos grupos de aliases numéricos siguen sin cumplir STD-011 (SCREAMING_SNAKE_CASE
con significado descriptivo):

| Grupo | Ejemplos actuales | Forma correcta |
|-------|-------------------|---------------|
| AC / ACC | `AC01`, `ACC04` | `UC_ACC_01`, `UC_ACC_04` |
| UC numérico | `UC01`, `UC07` | `UC_AUTH_01`, `UC_PERM_07` |

A diferencia de los grupos anteriores (ABREV_CORTA, F_FUNCIONES, etc.), estos
aliases **no tienen un diccionario global único**: el alias `UC01` en un archivo
del módulo AUTH significa `UC_AUTH_01`, pero en un archivo del módulo USR
significa `UC_USR_01`. La corrección es **por archivo**, derivando el módulo
del path del archivo.

## Patrón de corrección — PROVEN (observado en los archivos)

El display name de cada usecase ya contiene el UC ID completo:

```
usecase "UC_AUTH_01\nIniciar Sesion" as UC01   → as UC_AUTH_01
usecase "UC_AUTH_04\nCambiar Contrasena" as UC04  → as UC_AUTH_04
usecase "UC_ALR_02\nAlertas Activas" as UC02   → as UC_ALR_02
usecase "UC_PERM_08\nGenerar Menu" as UC08     → as UC_PERM_08
```

Regla:
- `UC0N` en `uc-{mod}-*/` → `UC_{MOD}_0N` (mismo número, prefijo de módulo del path)
- `AC0N` → `UC_ACC_0N`
- `ACC0N` → `UC_ACC_0N`

## Casos especiales verificados

| Archivo | Aliases declarados | Observación |
|---------|-------------------|-------------|
| `uc-auth-01/diagrama-de-caso-de-uso.rst` | `UC01`, `UC04` | Muestra 2 UCs del módulo AUTH: el principal (01) y uno relacionado (04) |
| `uc-alr-02/caso-de-uso.rst` | `UC02`, `UC03` | Muestra 2 UCs adyacentes del módulo ALR |
| `uc-perm-08/diagrama-de-caso-de-uso.rst` | `UC07`, `UC08` | Muestra UC07 y UC08 del módulo PERM |

El número del alias **siempre coincide** con el número del UC en el display name.
La regla de conversión es directa y no tiene excepciones.

## Grupo A — AC01..AC09 y ACC01..ACC08

**5 archivos, 11 alias-declaraciones**

| Archivo | Aliases actuales | Aliases correctos |
|---------|-----------------|------------------|
| `arquitectura-tecnica/use-case-view/uc-access.rst` | `AC01,AC02,AC03,AC04,AC05,AC08,AC09` | `UC_ACC_01..UC_ACC_09` |
| `requisitos/_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` | `ACC01` | `UC_ACC_01` |
| `requisitos/casos-uso/permissions/uc-perm-01/diagramas-uml/diagrama-de-coexistencia-acc-perm.rst` | `ACC04` | `UC_ACC_04` |
| `requisitos/casos-uso/permissions/uc-perm-02/diagramas-uml/diagrama-de-coexistencia-acc-perm.rst` | `ACC02` | `UC_ACC_02` |
| `requisitos/casos-uso/permissions/uc-perm-03/diagramas-uml/diagrama-de-coexistencia-acc-perm.rst` | `ACC08` | `UC_ACC_08` |

## Grupo B — UC01..UC09 por módulo

**49 archivos** distribuidos en 10 módulos:

### MODULE: ACC (7 archivos)
| Archivo | Declarados |
|---------|-----------|
| `uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC01 → UC_ACC_01 |
| `uc-acc-02/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC02 → UC_ACC_02 |
| `uc-acc-03/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC03 → UC_ACC_03 |
| `uc-acc-04/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC04 → UC_ACC_04 |
| `uc-acc-05/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC05 → UC_ACC_05 |
| `uc-acc-08/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC08 → UC_ACC_08 |
| `uc-acc-09/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC09 → UC_ACC_09 |

### MODULE: ALR (5 archivos)
| Archivo | Declarados |
|---------|-----------|
| `uc-alr-01/diagramas-uml/caso-de-uso.rst` | UC01 → UC_ALR_01 |
| `uc-alr-02/diagramas-uml/caso-de-uso.rst` | UC02 → UC_ALR_02, UC03 → UC_ALR_03 |
| `uc-alr-03/diagramas-uml/caso-de-uso.rst` | UC03 → UC_ALR_03 |
| `uc-alr-04/diagramas-uml/caso-de-uso.rst` | UC04 → UC_ALR_04 |
| `uc-alr-05/diagramas-uml/caso-de-uso.rst` | UC05 → UC_ALR_05 |

### MODULE: AUD (4 archivos)
| Archivo | Declarados |
|---------|-----------|
| `uc-aud-01/diagramas-uml/caso-de-uso.rst` | UC01 → UC_AUD_01 |
| `uc-aud-02/diagramas-uml/caso-de-uso.rst` | UC02 → UC_AUD_02 |
| `uc-aud-03/diagramas-uml/caso-de-uso.rst` | UC03 → UC_AUD_03 |
| `uc-aud-04/diagramas-uml/caso-de-uso.rst` | UC04 → UC_AUD_04 |

### MODULE: AUTH (5 archivos)
| Archivo | Declarados |
|---------|-----------|
| `uc-auth-01/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC01 → UC_AUTH_01, UC04 → UC_AUTH_04 |
| `uc-auth-02/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC02 → UC_AUTH_02 |
| `uc-auth-03/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC03 → UC_AUTH_03 |
| `uc-auth-04/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC04 → UC_AUTH_04 |
| `uc-auth-05/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC05 → UC_AUTH_05 |

### MODULE: LOG (7 archivos)
| Archivo | Declarados |
|---------|-----------|
| `uc-log-01/diagramas-uml/caso-de-uso.rst` | UC01 → UC_LOG_01 |
| `uc-log-02/diagramas-uml/caso-de-uso.rst` | UC02 → UC_LOG_02 |
| `uc-log-03/diagramas-uml/caso-de-uso.rst` | UC03 → UC_LOG_03 |
| `uc-log-04/diagramas-uml/caso-de-uso.rst` | UC04 → UC_LOG_04 |
| `uc-log-05/diagramas-uml/caso-de-uso.rst` | UC05 → UC_LOG_05 |
| `uc-log-06/diagramas-uml/caso-de-uso.rst` | UC06 → UC_LOG_06 |
| `uc-log-07/diagramas-uml/caso-de-uso.rst` | UC07 → UC_LOG_07 |

### MODULE: OPR (1 archivo)
| Archivo | Declarados |
|---------|-----------|
| `uc-opr-01/diagramas-uml/caso-de-uso.rst` | UC01 → UC_OPR_01 |

### MODULE: PERM (5 archivos)
| Archivo | Declarados |
|---------|-----------|
| `uc-perm-04/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC04 → UC_PERM_04 |
| `uc-perm-06/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC06 → UC_PERM_06 |
| `uc-perm-07/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC07 → UC_PERM_07 |
| `uc-perm-08/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC07 → UC_PERM_07, UC08 → UC_PERM_08 |
| `uc-perm-09/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC09 → UC_PERM_09 |

### MODULE: PIP (4 archivos)
| Archivo | Declarados |
|---------|-----------|
| `uc-pip-01/diagramas-uml/caso-de-uso.rst` | UC01 → UC_PIP_01 |
| `uc-pip-02/diagramas-uml/caso-de-uso.rst` | UC02 → UC_PIP_02 |
| `uc-pip-03/diagramas-uml/caso-de-uso.rst` | UC03 → UC_PIP_03 |
| `uc-pip-04/diagramas-uml/caso-de-uso.rst` | UC04 → UC_PIP_04 |

### MODULE: RPT (7 archivos)
| Archivo | Declarados |
|---------|-----------|
| `uc-rpt-01/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC01 → UC_RPT_01 |
| `uc-rpt-02/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC02 → UC_RPT_02 |
| `uc-rpt-03/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC03 → UC_RPT_03 |
| `uc-rpt-04/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC04 → UC_RPT_04 |
| `uc-rpt-07/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC07 → UC_RPT_07 |
| `uc-rpt-08/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC08 → UC_RPT_08 |
| `uc-rpt-09/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC09 → UC_RPT_09 |

### MODULE: USR (4 archivos)
| Archivo | Declarados |
|---------|-----------|
| `uc-usr-01/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC01 → UC_USR_01 |
| `uc-usr-02/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC02 → UC_USR_02 |
| `uc-usr-03/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC03 → UC_USR_03 |
| `uc-usr-04/diagramas-uml/diagrama-de-caso-de-uso.rst` | UC04 → UC_USR_04 |

## Totales

| Grupo | Archivos | Alias-declaraciones |
|-------|----------|---------------------|
| AC/ACC | 5 | 11 |
| UC01-UC09 por módulo | 49 | ~55 (algunos files declaran 2) |
| **Total** | **54** | **~66** |

## Estrategia de implementación

El script del grupo ABREV_CORTA (`fix-abrev-corta.py`) aplica la misma lógica:
buscar `as ALIAS` en el bloque y reemplazar todas las ocurrencias fuera de strings.

Para este WP, la diferencia es que el diccionario de reemplazo **se construye
por archivo** en lugar de ser global:

```python
def build_per_file_mapping(fpath):
    """Deriva el módulo del path y construye el dict alias→nuevo_alias."""
    rel = os.path.relpath(fpath)
    # Extraer módulo del patrón uc-{mod}-NN en el path
    m = re.search(r'uc-([a-z]+)-\d+', rel)
    module = m.group(1).upper() if m else None

    mapping = {}
    # AC0N y ACC0N → UC_ACC_0N (siempre ACC, independiente del path)
    for i in [1,2,3,4,5,8,9]:
        mapping[f'AC{i:02d}']  = f'UC_ACC_{i:02d}'
        mapping[f'ACC{i:02d}'] = f'UC_ACC_{i:02d}'

    # UC0N → UC_{MODULE}_0N
    if module:
        for i in range(1, 10):
            mapping[f'UC{i:02d}'] = f'UC_{module}_{i:02d}'

    return mapping
```

## Aliases descartados del catálogo original

Los grupos de conflictos `A01-A05`, `P01-P04`, `U01-U04` del catálogo **no
existen** en el código como declaraciones PlantUML — búsqueda exhaustiva
retornó 0 hits. No requieren corrección.

## Criterios de exit

- `make html` → `build succeeded.` EXIT:0, 0 warnings
- Los 54 archivos usan `UC_MOD_NN` en lugar de `UC0N` / `AC0N` / `ACC0N`
- Build log guardado en `logs/`
