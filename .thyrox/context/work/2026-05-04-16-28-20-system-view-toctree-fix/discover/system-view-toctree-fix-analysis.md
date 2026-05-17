```yml
created_at: 2026-05-04 16:28:20
project: IACT-docs
work_package: 2026-05-04-16-28-20-system-view-toctree-fix
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# F-07 — system-view/ sin toctree principal: análisis

## 1. Hallazgo original

`system-view/index.rst` existe como documento RST válido con su propio
toctree de 12 archivos, pero **no está referenciado desde ningún documento
padre**. Es un índice huérfano (Sphinx orphan warning suprimido solo porque
nada lo enlaza).

---

## 2. Inventario de la situación actual

### 2.1 Archivos en system-view/

| Archivo | Artefacto ID | Tipo de diagrama |
|---------|-------------|-----------------|
| `casos-uso-sistema-iact.rst` | AT_UML_SISTEMA_03_CASOS_USO | Use Case — nivel sistema |
| `clases-sistema-iact.rst` | AT_UML_SISTEMA_04_CLASES | Class — capa de servicio |
| `actividad-flujo-principal.rst` | AT_UML_SISTEMA_05_ACTIVIDAD_PRINCIPAL | Activity — flujo principal |
| `actividad-autenticacion.rst` | AT_UML_SISTEMA_06* | Activity — autenticación |
| `maquina-estados-sistema-iact.rst` | AT_UML_SISTEMA_07_ESTADOS | State Machine — sistema |
| `secuencia-sistema-iact.rst` | AT_UML_SISTEMA_08* | Sequence — sistema |
| `comunicacion-sistema-iact.rst` | AT_UML_SISTEMA_09_COMUNICACION | Communication |
| `componentes-sistema-iact.rst` | AT_UML_SISTEMA_10_COMPONENTES | Component — nivel sistema |
| `despliegue-sistema-iact.rst` | AT_UML_SISTEMA_11_DESPLIEGUE | Deployment — estándar |
| `submaquina-etl.rst` | AT_UML_SISTEMA_12* | Sub-state machine — ETL |
| `submaquina-reporte.rst` | AT_UML_SISTEMA_13* | Sub-state machine — reporte |
| `despliegue-multicliente.rst` | AT_UML_SISTEMA_14_DESPLIEGUE_MULTICLIENTE | Deployment — multi-cliente |

**Fuente:** PROVEN — `find source/arquitectura-tecnica/system-view -type f | sort`

### 2.2 Cadena de navegación actual (diagramas-uml-sistema.rst)

```
arquitectura-tecnica/index.rst
  └── toctree → diagramas-uml-sistema.rst        ← referenciado
        └── toctree → system-view/casos-uso-sistema-iact
                   → system-view/clases-sistema-iact
                   → ...12 archivos directos...
                   → system-view/despliegue-multicliente

arquitectura-tecnica/index.rst
  └── toctree → vistas-kruchten.rst              ← referenciado
        └── toctree → context-view/index
                   → use-case-view/index
                   → domain-model/index
                   → process-view/index
                   → design-view/index
                   → implementation-view/index
                   → deploy-view/index
                   → operational-view/index
                   → perspectivas/index
                   ↑ system-view/index AUSENTE

system-view/index.rst                            ← HUÉRFANO
  └── toctree → casos-uso-sistema-iact
             → clases-sistema-iact
             → ...12 archivos...
```

**Fuente:** PROVEN — lectura directa de `arquitectura-tecnica/index.rst` (l.19-46),
`vistas-kruchten.rst` (l.71-83), `diagramas-uml-sistema.rst` (l.188-203),
`system-view/index.rst` (l.23-38).

### 2.3 El problema del doble toctree

Los 12 archivos de `system-view/` son accesibles **solo** a través de
`diagramas-uml-sistema.rst`. `system-view/index.rst` tiene el mismo toctree
pero no está en ningún padre — por eso no genera warnings de "multiple
toctrees". Si se agrega `system-view/index` a un padre sin eliminar el
toctree en `diagramas-uml-sistema.rst`, los 12 archivos quedarán referenciados
en dos toctrees distintos y Sphinx generará 12 nuevos warnings.

**Fuente:** INFERRED — lógica de comportamiento de Sphinx toctree documentada;
el patrón es el mismo que ya ocurre con `use-case-view/` (15 warnings actuales
observados en `make html` output).

---

## 3. Análisis de contenido — solapamiento con vistas 5+1

| Archivo system-view | Vista 5+1 que cubre mismo concern | Nivel de solapamiento |
|---------------------|-----------------------------------|-----------------------|
| `casos-uso-sistema-iact.rst` | `use-case-view/` (13 módulos) | Parcial — system-view es nivel sistema; use-case-view es por módulo |
| `clases-sistema-iact.rst` | `domain-model/` (26 clases) | Parcial — domain-model son entidades; system-view tiene clases de servicio (SistemaIACT, ServicioReportes, DisparadorETL) |
| `actividad-flujo-principal.rst` | `process-view/` (flujos concurrentes) | Bajo — process-view cubre concurrencia; actividad cubre flujo secuencial |
| `actividad-autenticacion.rst` | `process-view/` | Bajo — mismo razonamiento |
| `maquina-estados-sistema-iact.rst` | **Ninguna** | Cero solapamiento |
| `secuencia-sistema-iact.rst` | `design-view/` (secuencias por módulo) | Parcial — design-view es por módulo; este es sistema completo |
| `comunicacion-sistema-iact.rst` | **Ninguna** | Cero solapamiento |
| `componentes-sistema-iact.rst` | `implementation-view/` (por módulo) | Parcial — implementation-view es por módulo; este es sistema completo |
| `despliegue-sistema-iact.rst` | `deploy-view/` (3 variantes) | Alto — deploy-view ya tiene variante estándar |
| `submaquina-etl.rst` | **Ninguna** | Cero solapamiento |
| `submaquina-reporte.rst` | **Ninguna** | Cero solapamiento |
| `despliegue-multicliente.rst` | `deploy-view/` | Medio — deploy-view tiene variantes; este es una cuarta |

**Fuente:** PROVEN — lectura directa de los 12 archivos y de los índices de
cada vista 5+1.

### Conclusión de solapamiento

4 de los 12 archivos no tienen ninguna vista 5+1 equivalente (máquina de
estados, comunicación, sub-máquinas). 8 tienen solapamiento parcial o alto.
`system-view/` no es, por tanto, redundante — contiene contenido único y
contenido complementario (distinto nivel de granularidad).

**Fuente:** INFERRED — derivado de la tabla anterior con razonamiento explícito.

---

## 4. Raíz del problema — origen histórico

`system-view/` es una **colección UML pre-Kruchten**: fue creada antes de
que el modelo 5+1 IACT se estructurara (ÉPICA 17). Cuando ÉPICA 17 construyó
las 9 vistas en `vistas-kruchten.rst`, `system-view/` no fue integrada en
la nueva estructura. `diagramas-uml-sistema.rst` actuó como proxy ad-hoc
para seguir exponiendo los 12 archivos.

El resultado: dos rutas de navegación conceptualmente distintas hacia el
mismo contenido — una legacy (`diagramas-uml-sistema`) y una nueva sin padre
(`system-view/index`).

**Fuente:** INFERRED — basado en metadata `fecha_creacion: 2026-05-04` de
los 12 archivos y en el historial de construcción de ÉPICA 17.

---

## 5. Opciones de corrección

### Opción A — Agregar system-view/index a vistas-kruchten sin tocar diagramas-uml-sistema

**Cambios:** 1 archivo (`vistas-kruchten.rst`): añadir fila + entry en toctree.

**Consecuencia crítica:** Los 12 archivos quedan en dos toctrees simultáneos
(`diagramas-uml-sistema.rst` y `system-view/index.rst`). Sphinx genera
12 nuevos warnings "document is referenced in multiple toctrees".

**Veredicto:** DESCARTADA — empeora el estado del build.

---

### Opción B — Eliminar system-view/index.rst (mantener solo diagramas-uml-sistema como proxy)

**Cambios:** `git rm system-view/index.rst`.

**Consecuencia:** El huérfano desaparece. Los 12 archivos siguen accesibles
por `diagramas-uml-sistema.rst`. La inconsistencia estructural (no tener
index propio como las otras 9 vistas) queda sin resolver — no hay un
`system-view/index` como existe `deploy-view/index`, `design-view/index`, etc.

**Veredicto:** PARCIAL — elimina el síntoma pero no resuelve la inconsistencia
estructural con el resto de las vistas.

---

### Opción C — Hacer system-view/index el punto canónico (RECOMENDADA)

**Cambios coordinados (3 archivos):**

1. **`vistas-kruchten.rst`** — Agregar fila "System Overview" + entry en toctree
   apuntando a `system-view/index`.

2. **`diagramas-uml-sistema.rst`** — Eliminar el toctree de los 12 archivos
   (evita double-toctree). Reemplazar la sección 3 por un `seealso` que apunte
   a `system-view/index`. La narrativa (secciones 1 y 2: actores, UCs) se
   conserva — es contenido de especificación, no navegación.

3. **`system-view/index.rst`** — Sin cambios (ya es correcto; solo necesita
   un padre).

**Resultado:**
- `system-view/index` deja de ser huérfano → referenciado desde `vistas-kruchten`.
- Los 12 archivos tienen un único padre (`system-view/index`) → sin warnings.
- `diagramas-uml-sistema.rst` conserva su valor como documento narrativo
  (especificación de actores y UCs) sin duplicar la navegación.
- Consistencia estructural: `system-view/` tiene su index propio como todas
  las demás vistas.

**Veredicto:** APROBADA.

---

### Opción D — Migrar contenido único a las vistas correspondientes y retirar system-view/

**Cambios:** Mover 4 archivos únicos (estados, comunicación, sub-máquinas) a
`process-view/` o `design-view/`. Reclasificar los 8 restantes.

**Riesgo:** Alto — implica modificar toctrees de múltiples vistas, potencial
confusión de rol de cada vista, 12 movimientos de archivo, actualización de
seealso en cada archivo. Riesgo de introducir nuevos F-NN.

**Veredicto:** DESCARTADA por ahora — es una refactorización mayor que va
más allá de resolver el huérfano. Puede ser un WP futuro post-consolidación.

---

## 6. Clasificación Rozanski-Woods para system-view

Para la fila en `vistas-kruchten.rst`, la clasificación más honesta es:

| Campo | Valor |
|-------|-------|
| Tipo Rozanski | *Context (overview)* — colección transversal de UML pre-Kruchten |
| Descripción | Diagramas UML del sistema completo: casos de uso sistema, clases de servicio, actividad, máquina de estados, secuencia sistema, comunicación, componentes, despliegue y sub-máquinas ETL/Reporte. Colección de granularidad sistema (no por módulo). |

No encaja en ningún viewpoint puro de Rozanski porque abarca múltiples
concerns. La clasificación más honesta es marcarlo como "System Overview"
o "UML System Collection" — análogo a cómo `perspectivas/` se clasifica
como "transversal".

**Fuente:** INFERRED — derivado del análisis de contenido en sección 3.

---

## 7. Plan de corrección (Opción C)

### Cambio 1 — `vistas-kruchten.rst`

Agregar fila en la tabla list-table:

```rst
 * - :doc:`system-view/index`
   - System Overview (UML)
   - Coleccion de diagramas UML a nivel sistema: casos de uso,
     clases de servicio, actividad, maquina de estados, secuencia,
     comunicacion, componentes, despliegue estandar, despliegue
     multi-cliente y sub-maquinas ETL/Reporte.
```

Agregar entry en toctree (después de `perspectivas/index`):

```rst
 system-view/index
```

### Cambio 2 — `diagramas-uml-sistema.rst`

Reemplazar sección "3. Diagramas UML (uno por archivo)" y su toctree por:

```rst
3. Diagramas UML (uno por archivo)
====================================

Los diagramas estan organizados en :doc:`system-view/index`.

.. seealso::

 :doc:`system-view/index`
 :doc:`vistas-kruchten`
```

### Cambio 3 — sin cambios en system-view/index.rst

Ya tiene el toctree correcto. Solo necesita que un padre lo referencie.

---

## 8. Verificación post-corrección

- `make html` — verificar que los 12 warnings de "multiple toctrees" no aparezcan
- `system-view/index` accesible desde `vistas-kruchten`
- `diagramas-uml-sistema.rst` conserva secciones 1 y 2 (narrativa de actores y UCs)
- Build succeeded sin nuevos warnings

---

## 9. Riesgos identificados

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|-----------|
| Romper seealso en archivos que apuntan a diagramas-uml-sistema | Baja | Los seealso apuntan a `vistas-kruchten` y `requisitos/casos-uso/index`, no a diagramas-uml-sistema |
| Introducir doble-toctree si el edit en diagramas-uml-sistema es incompleto | Media | Verificar con make html inmediatamente después del cambio 2 |
| system-view/index no mapea a ninguna categoría Rozanski pura | Aceptado | Documentado como "System Overview" — categoría honesta, no forzada |

---

## 10. Criterios de salida

- [ ] `vistas-kruchten.rst` tiene fila y toctree entry para `system-view/index`
- [ ] `diagramas-uml-sistema.rst` no tiene toctree de system-view files (solo seealso)
- [ ] `make html` succeeds sin nuevos warnings (≤15 warnings pre-existentes)
- [ ] `system-view/index` navegable desde la tabla de vistas Kruchten
