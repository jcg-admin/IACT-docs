```yml
created_at: 2026-05-07 00:30:00
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
phase: Phase 11 — TRACK (review pre-cierre)
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Post-Design Coverage Review — gaps detectados

> Auditoria post-Phase 7 DESIGN antes de cerrar el WP.
> Verifica que los nuevos artefactos del WP se integraron
> correctamente en el corpus existente.

## Sección 1 — Metodología

Verificaciones ejecutadas con grep sobre el corpus para
detectar puntos donde los nuevos UCs / capabilities /
ADRs deberian aparecer pero no aparecen.

## Sección 2 — Gaps detectados

### G-1 (Crítico) — Catálogo de funciones desactualizado

**Archivo:** ``source/requisitos/reglas-negocio/rbac/catalogo-funciones.rst``
§3.11 MOD_Admin.

**Problema:** sigue declarando "3 funciones" (NUEVO v5.6.0)
con UC_ADM_01..03. No incluye:

- ``manage_menu_catalog`` (UC_ADM_04, ``is_critical=True``).
- ``manage_menu_lifecycle`` (UC_ADM_05, ``is_critical=True``).
- ``manage_critical_function_flag`` (sin titular,
  ``is_critical=True``).

**Impacto:** los UCs nuevos referencian capabilities que
formalmente no existen en el catalogo. Inconsistencia entre
ADRs/UCs nuevos y catalogo canonico RBAC.

**Accion requerida:**

- Actualizar §3.11 MOD_Admin con tabla de las 6 funciones
  (3 originales + 3 nuevas).
- Marcar ``is_critical=True`` en las 3 nuevas.
- Marcar ``manage_critical_function_flag`` con
  "AGR titular: ninguno (gobernanza via migration)".
- Actualizar el conteo "64 funciones activas / 77 declaradas"
  → "67 funciones activas / 80 declaradas" si las 3 nuevas
  cuentan como activas. **Decision pendiente del ejecutor**.

### G-2 (Crítico) — mapeo-uc.rst sin UC_ADM_04/05

**Archivo:** ``source/requisitos/reglas-negocio/rbac/mapeo-uc.rst``.

**Problema:** la tabla de mapeo function → UC no incluye
las 3 nuevas capabilities ni los 2 nuevos UCs.

**Accion requerida:**

- Agregar filas: ``manage_menu_catalog`` → UC_ADM_04;
  ``manage_menu_lifecycle`` → UC_ADM_05;
  ``manage_critical_function_flag`` → (sin UC,
  governance via migration).

### G-3 (Crítico) — Conteo "64 funciones" en BR-006 desactualizado

**Archivo:** ``source/requisitos/reglas-negocio/br-006-rbac-flat-nist.rst``.

**Problema:** declara "64 funciones atomicas activas" en
varios lugares (lineas 135, 168, 214). Si las nuevas se
incorporan al catalogo activo, el conteo cambia.

**Accion requerida:** actualizar conteos a 67/80 si la
decision es incluir las nuevas como activas en v5.6.x.

### G-4 (Importante) — Use-case-view/admin sin UC_ADM_04/05

**Archivo:** ``source/arquitectura-tecnica/use-case-view/admin/index.rst``.

**Problema:** el diagrama PlantUML de UCs del modulo MOD_Admin
solo incluye UC_ADM_01/02/03. La tabla de UCs tampoco lista
los nuevos.

**Accion requerida:**

- Agregar UC_ADM_04 y UC_ADM_05 al diagrama PlantUML.
- Agregar filas a la tabla con resumen de cada UC nuevo.
- Crear ``uc-adm-04-gestionar-catalogo-menuitems.rst`` y
  ``uc-adm-05-gestionar-lifecycle-menuitem.rst`` en el mismo
  directorio (resumen de vista UC, no la spec completa).

### G-5 (Importante) — Matriz de dependencias UC sin nuevos UCs

**Archivo:** ``source/arquitectura-tecnica/matriz-dependencias-uc-iact.rst``.

**Problema:** sin entradas para UC_ADM_04 y UC_ADM_05.

**Accion requerida:** agregar filas con dependencias:

- UC_ADM_04 depende de UC_ADM_02 (Function existe).
- UC_ADM_05 depende de UC_ADM_04 (MenuItem existe).
- UC_PERM_08 ext consumido por todos los users autenticados.

### G-6 (Medio) — Technical debt sin TD-RBAC-03

**Archivo:** ``.thyrox/context/technical-debt.md``.

**Problema:** ADR-BACK-010 declara TD-RBAC-03
(``manage_critical_function_flag`` sin titular runtime),
pero no esta registrado en el archivo de deuda tecnica
del proyecto.

**Accion requerida:** agregar entrada:

::

   - [ ] **TD-RBAC-03** — `manage_critical_function_flag`
     declarada en catalogo v5.6.x sin AGR titular. Cambios
     al flag `Function.is_critical` solo via Django RunPython
     data migration con review obligatoria.
     Trigger de revision: si se requiere via runtime de
     cambios al flag, abrir ADR explicito.
     Origen: ADR-BACK-010 §3.6.

### G-7 (Medio) — STD-010 menor en UC_PERM_08 ext

**Archivo:** ``source/requisitos/casos-uso/permissions/uc-perm-08/extension-v560-menu-item-wrapper.rst``.

**Problema:** linea 242 menciona "Django ORM" en la tabla
diff v5.0.0 vs v5.6.0. Aunque el contexto es comparativo
(documenta el cambio tecnologico), STD-010 §3 prohibe
``\bDjango\b`` en archivos en ambito.

**Accion requerida:** sustituir "Query Django ORM via
``MenuItem.objects.for_user``" por "Query del Servicio de
Aplicacion sobre el Almacen de Datos via
``MenuItem.objects.for_user``" o mover la nota tecnica a
``implementacion-tecnica.rst`` del UC.

### G-8 (Bajo) — CNST-033 sin referencia a CNST-032 v2.0.0

**Archivo:** ``source/normativa/restricciones/cnst-033-conformidad-uml-iact.rst``.

**Problema:** CNST-033 (conformidad UML) no referencia
CNST-032 v2.0.0 ni los nuevos UCs / ADRs. No es bloqueante,
pero CNST-033 podria mencionar el patron del diagrama de
estados de UC_ADM_05 como ejemplo canonico.

**Accion sugerida:** agregar referencia cruzada en sección
de "Diagramas validados" si CNST-033 lo soporta.

### G-9 (Bajo) — Bootstrap test de implementation-guide

**Archivo:** ``source/backend/rbac-implementation-guide.rst``
sección "Tests obligatorios" (linea 668-).

**Problema:** los tests obligatorios cuentan
``Function.objects.count() == 64`` y
``AccessGroup.objects.filter(is_system=True).count() == 10``.
Si las 3 nuevas se agregan, hay que actualizar a 67.

**Accion requerida:** alineado con G-3 — actualizar conteos
en los tests de bootstrap.

### G-10 (Bajo) — uc-adm-04 datos-involucrados con typo

**Archivo:** ``source/requisitos/casos-uso/admin/uc-adm-04/patrones-diseno.rst``.

**Problema:** detectado y corregido durante L3
(``.. meta">`` → ``.. meta::``). Confirmar que no quedaron
typos similares en otros archivos.

**Estado:** Resuelto durante build L3.

## Sección 3 — Severity matrix

.. list-table::
 :widths: 8 30 12 50
 :header-rows: 1

 * - ID
   - Gap
   - Severidad
   - Resolver donde / cuando
 * - G-1
   - Catalogo de funciones desactualizado
   - **Critico**
   - Antes de cerrar Phase 11 — actualizar §3.11
 * - G-2
   - mapeo-uc.rst sin UC_ADM_04/05
   - **Critico**
   - Antes de cerrar Phase 11
 * - G-3
   - Conteos 64/77 desactualizados en BR-006
   - **Critico**
   - Antes de cerrar Phase 11 (decision sobre conteo)
 * - G-4
   - use-case-view/admin sin nuevos UCs
   - Importante
   - Antes de cerrar Phase 11
 * - G-5
   - matriz-dependencias-uc-iact sin nuevos UCs
   - Importante
   - Antes de cerrar Phase 11
 * - G-6
   - TD-RBAC-03 no registrado
   - Medio
   - Antes de cerrar Phase 11
 * - G-7
   - "Django ORM" en uc-perm-08 ext
   - Medio
   - Antes de cerrar Phase 11
 * - G-8
   - CNST-033 sin referencia cruzada
   - Bajo
   - Diferible — no bloqueante
 * - G-9
   - Tests bootstrap con conteo 64
   - Bajo
   - Junto con G-3
 * - G-10
   - typo .. meta">
   - Resuelto
   - —

## Sección 4 — Decision arquitectonica pendiente

**¿Las 3 nuevas capabilities cuentan como "activas" en
v5.6.x?**

- Opcion A: SI, son v5.6.0 (in-scope). Conteo: 67/80.
- Opcion B: SI, pero documentar como "v5.6.x extension"
  (in-scope desde el WP menu-rbac-user-scope, no del v5.6.0
  inicial). Conteo: 67/80 con nota.
- Opcion C: ``manage_critical_function_flag`` no cuenta
  como activa porque NO tiene titular en v5.6.x — esta
  declarada pero sin uso runtime. Conteo: 66/80.

**Recomendacion:** Opcion B — son legitimamente del
catalogo v5.6.x con trazabilidad explicita al WP de origen.
``manage_critical_function_flag`` es activa
(``is_active=True``) aunque sin titular (``is_critical=True``,
sin AGR asignado).

Decision pendiente del ejecutor antes de aplicar G-1, G-3, G-9.

## Sección 5 — Plan propuesto

Si el ejecutor aprueba:

1. **Resolver decision §4** (conteo 67/80 con Opcion B).
2. **Aplicar G-1, G-2, G-3, G-9** en una sola pasada
   (catalogo coherente).
3. **Aplicar G-4, G-5** (use-case-view + matriz).
4. **Aplicar G-6** (technical-debt.md).
5. **Aplicar G-7** (correccion STD-010 menor).
6. **Diferir G-8** (no bloqueante).
7. Build sphinx strict EXIT=0.
8. Commit "Close coverage gaps post Phase 7 DESIGN".
9. Phase 11 TRACK con changelog del WP completo.

Volumen estimado: ~10 archivos modificados, 1 archivo nuevo
(o 2 si se crean los resumenes uc-adm-04/05 en
use-case-view/).

## Refs

- Estrategia: ``strategy/menu-rbac-user-scope-solution-strategy.md``.
- Addendum: ``strategy/strategy-addendum-gaps-and-module.md``.
- Phase 7 commits: cd224ee5, 8ed97a16, 86b1696f, 43624501.
- Catalogo de funciones:
  ``source/requisitos/reglas-negocio/rbac/catalogo-funciones.rst``.
- Mapeo: ``source/requisitos/reglas-negocio/rbac/mapeo-uc.rst``.
- BR-006: ``source/requisitos/reglas-negocio/br-006-rbac-flat-nist.rst``.
