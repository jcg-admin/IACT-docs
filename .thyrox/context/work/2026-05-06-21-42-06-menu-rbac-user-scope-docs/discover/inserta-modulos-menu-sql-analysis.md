```yml
created_at: 2026-05-06 22:10:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
parent_analysis: discover/cmenu2-legacy-archeology.md
script_origin: Inserta_modulos_menu.sql (legacy IACT)
```

# Arqueología SQL: `Inserta_modulos_menu.sql` — patrón de inserción legacy

## Contexto

Tras el análisis arqueológico de la tabla `C_MENU2`
(``cmenu2-legacy-archeology.md``), el ejecutor compartió un
script SQL legacy real — ``Inserta_modulos_menu.sql`` — que
muestra **cómo se insertaban menús nuevos en producción**.

Este artefacto es el **puente operativo** entre el modelo de
datos de `C_MENU2` (analizado antes) y la práctica real del
equipo: cómo agregaban un módulo de UI al sistema legacy.

## Script analizado (verbatim)

```sql
BEGIN TRAN

/*INSERTA  EL MENU LLAMADO REPORTE_APP */
SELECT *
FROM C_MENU2
WHERE NIVEL = 1 AND ID_PARENT = 90 AND STATUS = 'ACTIVO'
ORDER BY ORDEN ASC

INSERT INTO C_MENU2 (NIVEL,ID_PARENT,DES_MENU,DES_NAME,STATUS,TARGET,IMAGE,HREF,ORDEN)
VALUES (1,90,'REPORTE_APP','Acceso a la Aplicación ', 'ACTIVO','main',NULL, 'menu.asp',22 )

SELECT *
FROM C_MENU2
WHERE NIVEL = 1 AND ID_PARENT = 90 AND STATUS = 'ACTIVO'
ORDER BY ORDEN ASC

---------------------------------------------
/*INSERTA  LOS SUBMENUS LLAMADO REPORTE_DIARIO Y REPORTE_ACUMULADO  */

SELECT *
FROM  C_MENU2
WHERE ID_PARENT IN(447)

BEGIN TRAN
INSERT INTO C_MENU2 (NIVEL,ID_PARENT,DES_MENU,DES_NAME,STATUS,TARGET,IMAGE,HREF,ORDEN)
VALUES (2,447,'REPORTE_DIARIO','Reporte diario', 'ACTIVO','main',NULL, 'index.asp',1)

INSERT INTO C_MENU2 (NIVEL,ID_PARENT,DES_MENU,DES_NAME,STATUS,TARGET,IMAGE,HREF,ORDEN)
VALUES (2,447,'REPORTE_ACUMULADO','Reporte Acumulado', 'ACTIVO','main',NULL, 'index.asp',2)

SELECT *
FROM  C_MENU2
WHERE ID_PARENT IN(447)


ROLLBACK TRAN
------------------------------------------

INSERT INTO C_MENU2 (NIVEL,ID_PARENT,DES_MENU,DES_NAME,STATUS,TARGET,IMAGE,HREF,ORDEN)
VALUES (1,90,'REPORTE_ONBOARDING','Reporte OnBoarding', 'ACTIVO','main',NULL, 'menu.asp',24 )


INSERT INTO C_MENU2 (NIVEL,ID_PARENT,DES_MENU,DES_NAME,STATUS,TARGET,IMAGE,HREF,ORDEN)
VALUES (2,458,'MATRIZ_ASESOR','Matriz de asesores', 'ACTIVO','main',NULL, 'index.asp',1)
```

## Análisis sección por sección

### Sección 1 — Inserción del módulo padre `REPORTE_APP`

```sql
INSERT INTO C_MENU2 (NIVEL, ID_PARENT, DES_MENU, DES_NAME, STATUS, TARGET, IMAGE, HREF, ORDEN)
VALUES (1, 90, 'REPORTE_APP', 'Acceso a la Aplicación ', 'ACTIVO', 'main', NULL, 'menu.asp', 22)
```

**Decodificación:**

| Campo | Valor | Semántica |
|---|---|---|
| `NIVEL` | `1` | Es un nodo de nivel 1 (sección bajo el padre raíz) |
| `ID_PARENT` | `90` | Cuelga de un nodo raíz preexistente con `ID_MENU=90` |
| `DES_MENU` | `'REPORTE_APP'` | Codename interno (UPPERCASE_WITH_UNDERSCORES) |
| `DES_NAME` | `'Acceso a la Aplicación '` | Display name (con espacio trailing — bug menor de captura) |
| `STATUS` | `'ACTIVO'` | Visible para los usuarios |
| `TARGET` | `'main'` | Frame target (frameset HTML legacy) |
| `IMAGE` | `NULL` | Sin icono |
| `HREF` | `'menu.asp'` | URL = página intermedia (no destino final) |
| `ORDEN` | `22` | Orden visual entre hermanos |

**Observación clave del HREF:** ``'menu.asp'`` para
``NIVEL=1`` es **siempre la página intermedia que renderiza
los hijos**. Es decir, los nodos NIVEL=1 son **carpetas**, no
destinos finales.

### Sección 2 — Inserción de submenús `REPORTE_DIARIO` y `REPORTE_ACUMULADO`

```sql
INSERT INTO C_MENU2 (...)
VALUES (2, 447, 'REPORTE_DIARIO', 'Reporte diario', 'ACTIVO', 'main', NULL, 'index.asp', 1)

INSERT INTO C_MENU2 (...)
VALUES (2, 447, 'REPORTE_ACUMULADO', 'Reporte Acumulado', 'ACTIVO', 'main', NULL, 'index.asp', 2)
```

**Decodificación:**

| Aspecto | Observación |
|---|---|
| `NIVEL=2` | Hojas de la jerarquía (destinos reales) |
| `ID_PARENT=447` | El `ID_MENU` autogenerado del `REPORTE_APP` recién insertado |
| `HREF='index.asp'` | URL = página real con la vista del reporte |
| `ORDEN=1, 2` | Orden visual dentro de los hijos del padre |

**Pattern crítico:** el script asume que el INSERT previo
generó `ID_MENU=447`. **Esto significa que el script NO es
re-ejecutable en otro ambiente** — el autoincrement varía
entre BD/staging/prod. El DBA debe leer el ID generado y
sustituirlo manualmente. Es **deuda técnica operacional grave**.

### Sección 3 — `BEGIN TRAN` ... `ROLLBACK TRAN` (testing pattern)

El script incluye `BEGIN TRAN` ... `ROLLBACK TRAN` envolviendo
los inserts. Esto significa que **el bloque era de prueba** —
el DBA validaba el efecto del INSERT, lo revertía con
`ROLLBACK`, y solo después lo aplicaba en producción quitando
el `ROLLBACK`.

**Implicación:** el flujo operativo era:

1. Escribir INSERTs en un script con BEGIN TRAN.
2. Ejecutar en staging/dev → revisar SELECT antes/después.
3. ROLLBACK para dejar limpia la base.
4. Pasar a producción quitando el ROLLBACK (manualmente).

**Riesgos heredados:**

- El paso 4 (quitar ROLLBACK) era manual → riesgo de:
  (a) ejecutar con ROLLBACK en producción (no se aplica nada,
  bug silencioso), o
  (b) olvidar el ROLLBACK en staging y romper los tests.
- Sin migration tooling formal (vs Django ``RunPython``).

### Sección 4 — Tercer insert: `REPORTE_ONBOARDING` + `MATRIZ_ASESOR`

```sql
INSERT INTO C_MENU2 (...)
VALUES (1, 90, 'REPORTE_ONBOARDING', 'Reporte OnBoarding', 'ACTIVO', 'main', NULL, 'menu.asp', 24)

INSERT INTO C_MENU2 (...)
VALUES (2, 458, 'MATRIZ_ASESOR', 'Matriz de asesores', 'ACTIVO', 'main', NULL, 'index.asp', 1)
```

**Confirmación del patrón:**

- Otro módulo padre (`NIVEL=1`, `ID_PARENT=90`, `ORDEN=24`) — el ORDEN=22 anterior + ORDEN=24 confirma espaciamiento de 2 entre hermanos para permitir intercalar.
- Otro hijo (`NIVEL=2`, `ID_PARENT=458`) → 458 es el ID autogenerado del `REPORTE_ONBOARDING` previo (acoplamiento autoincrement otra vez).

## Reconstrucción del árbol que el script construye

Tras ejecutar las cuatro inserciones (asumiendo no-rollback):

```
C_MENU2
└── ID_MENU=90 (raíz preexistente, probablemente "Sistema" o "Reportes")
    │
    ├── ID_MENU=447 — REPORTE_APP — "Acceso a la Aplicación" (NIVEL=1, ORDEN=22, HREF=menu.asp)
    │   ├── ID_MENU=??? — REPORTE_DIARIO — "Reporte diario" (NIVEL=2, ORDEN=1, HREF=index.asp)
    │   └── ID_MENU=??? — REPORTE_ACUMULADO — "Reporte Acumulado" (NIVEL=2, ORDEN=2, HREF=index.asp)
    │
    └── ID_MENU=458 — REPORTE_ONBOARDING — "Reporte OnBoarding" (NIVEL=1, ORDEN=24, HREF=menu.asp)
        └── ID_MENU=??? — MATRIZ_ASESOR — "Matriz de asesores" (NIVEL=2, ORDEN=1, HREF=index.asp)
```

**Nota:** el script no muestra los IDs de los nietos (los
NIVEL=2). Se infiere que el DBA volvía a leer el ID generado
y lo usaba para insertar nietos de la misma forma.

## Hallazgos analíticos

### F-01 — El menú es estado mutable de la BD, NO código

El script INSERTa rows en producción para agregar un módulo
de UI. Esto significa:

- **Cada nueva sección de UI = release de SQL en producción.**
- **No hay versionado del menú en código** — el menú vive en
  la BD y solo se documenta a través del script
  `Inserta_modulos_menu.sql` que se entrega al DBA.
- **No hay tests automatizados** del estado del menú.

Comparado con v5.6.0 actual:

- Frontend tiene `ALL_NAV_LINKS` como **constante en código**.
- Cualquier cambio en el menú = commit + PR + CI + deploy normal.
- Estado del menú es **versionado, testeable, reversible**.

### F-02 — HREF acoplado al backend ASP legacy

`HREF='menu.asp'` (NIVEL=1) y `HREF='index.asp'` (NIVEL=2)
son **rutas de servidor ASP**, no rutas de SPA moderna.

Implicaciones:

- En el sistema legacy, `menu.asp` recibía `?id=XXX` para
  saber qué hijos renderizar (no visible en el script pero
  inferible).
- Migrar a SPA implica **eliminar HREF del schema** —
  Frontend conoce sus rutas (React Router), no las consulta
  al backend.

### F-03 — Acoplamiento de jerarquía con autoincrement

El script reutiliza `ID_MENU=447` y `ID_MENU=458` como
`ID_PARENT` en inserts subsiguientes. Estos son IDs
**generados por el motor de DB** en la sesión donde se
ejecutó el script.

Riesgos heredados:

- **No portable**: el mismo script ejecutado en otra BD genera
  IDs distintos. El DBA debe ajustar manualmente.
- **No idempotente**: re-ejecutar duplica los menús (no hay
  `IF NOT EXISTS` ni `ON CONFLICT`).
- **Difícil de revertir**: para borrar lo creado, hay que saber
  los IDs ad-hoc.

Comparado con v5.6.0:

- AGRs identificados por `agr_code` natural key (`'AGR-001'`,
  no autoincrement).
- Migration RunPython usa `get_or_create` → idempotente.
- Reverse function explícita en cada migration.

### F-04 — Codename UPPERCASE legacy ASP vs snake_case Django

Legacy: `'REPORTE_APP'`, `'REPORTE_DIARIO'`,
`'REPORTE_ACUMULADO'`, `'REPORTE_ONBOARDING'`,
`'MATRIZ_ASESOR'`.

Patrón observado:

- Todo UPPERCASE.
- Underscore separador.
- Sin verbo (sustantivo simple o sustantivo compuesto).

v5.6.0 actual:

- snake_case lowercase.
- Verbo + sustantivo (`view_reports`, `export_csv`).
- "Función" (acción), no "módulo" (sección).

Esto refleja el **cambio de paradigma** confirmado en la
arqueología `C_MENU2` previa: legacy = menu-centric (módulo
es la unidad), actual = function-centric (acción es la
unidad).

### F-05 — Pattern de ORDEN con espaciamiento

`ORDEN=22` y `ORDEN=24` (delta 2) sugiere que el equipo
**reservaba números intermedios** para intercalar nuevos
módulos sin reordenar todos los hermanos.

Este es un anti-patrón típico de schemas con orden manual:
funciona hasta que se llena el espacio, luego requiere
"renumeración masiva" → bug-prone.

v5.6.0 evita esto: el frontend conoce su propio orden via
agrupación lógica del codename (module + verbo) o
configuración explícita en el componente.

### F-06 — El script tiene **ZERO referencias a permisos**

Crítico: el script `Inserta_modulos_menu.sql` **solo crea
nodos en `C_MENU2`**. NO inserta filas en `BD_MENU2` (M2M
user-menu con privilegios) ni en `BD_MENU_CONVENIO`.

**Implicación:** después de ejecutar este script, los nuevos
menús **existen pero ningún user los puede ver** — necesita
un script SEPARADO que inserte en `BD_MENU2` para asignar
privilegios.

Esto confirma el paradigma menu-centric:

1. El equipo crea el menú (este script).
2. Otro proceso asigna privilegios per-user-per-convenio.
3. El menú emerge como intersección.

vs paradigma actual:

1. Las funciones se bootstrap automáticamente con `migrate`.
2. Los AGRs predefinidos ya tienen las funciones asociadas.
3. Asignar un user a un AGR → automáticamente ve los menús
   correspondientes en frontend.

## Comparación operativa: legacy vs v5.6.0

| Operación | Legacy (este script) | v5.6.0 actual |
|---|---|---|
| Agregar módulo de UI | Escribir INSERT SQL + entregar a DBA + ejecutar en prod | Agregar entrada a `ALL_NAV_LINKS` (constante React) + commit + PR |
| Identidad del nodo | `ID_MENU` autoincrement | Codename del Function + ruta React (independientes) |
| Cambio de URL | INSERT/UPDATE en `C_MENU2.HREF` (release SQL) | Cambio en React Router (release frontend) |
| Asignar visibilidad a un user | Otro INSERT en `BD_MENU2` | Asignar AGR al user (UC_PERM_06) |
| Testear el cambio | Manual (BEGIN TRAN/ROLLBACK ad-hoc) | Tests unitarios + e2e en CI |
| Revertir el cambio | Manual (DBA recuerda los IDs) | git revert + redeploy |
| Idempotencia | NO (re-ejecutar duplica) | Sí (frontend constante; backend `get_or_create`) |
| Auditoría del cambio | Bitácora del DBA (off-system) | Git history (estructurada) |

## Implicaciones para el WP `menu-rbac-user-scope-docs`

### Implicación 1 — Refuerzo absoluto de la decisión Lectura B

El análisis arqueológico previo (`cmenu2-legacy-archeology.md`)
ya recomendaba **Lectura B** (jerarquía derivable del codename
sin metadata extra). El script SQL **refuerza** esta decisión
empíricamente:

- F-03 muestra que **acoplar jerarquía con autoincrement** fue
  fuente real de problemas operativos.
- F-01 muestra que **menú-en-BD** = release SQL por cada
  cambio de UI.
- F-02 muestra que **HREF en backend** acopla Frontend a
  Backend de forma indeseable.

Cualquier diseño v5.6.0 que reintroduzca **alguno** de estos
patrones (tabla `Menu` con `HREF`/`ORDEN`/`PARENT_ID`) sería
**regresión arquitectónica directa al modelo legacy**.

### Implicación 2 — Riesgo: "necesitamos preservar la jerarquía"

Un argumento posible para mantener jerarquía en backend:
*"el menú legacy era jerárquico de 2-3 niveles; debemos
preservar eso"*.

Respuesta canónica:

- **La jerarquía es UX, no permisos.** El frontend puede
  decidir su propia jerarquía a partir de los codenames del
  user.
- **Codenames v5.6.0 ya transportan jerarquía implícita**: el
  prefijo `module_` (`auth.`, `users.`, `access.`, `reports.`)
  + el verbo (`view_`, `export_`) + el sustantivo construyen
  4 niveles derivables sin metadata adicional.

### Implicación 3 — Documentar el anti-patrón explícitamente

El WP `menu-rbac-user-scope-docs` debería incluir, en Phase 7
DESIGN, una sección **"Anti-patrones heredados del legacy
C_MENU2 — NO replicar"**:

1. ❌ Tabla `Menu` con `HREF` (acopla frontend a schema BD).
2. ❌ Jerarquía con `parent_id` autoincrement (no portable).
3. ❌ ORDEN manual con espaciamiento (renumeración masiva).
4. ❌ INSERT manual en producción (sin migration tooling).
5. ❌ M2M user-menu con flags `can_*` (función atómica > flags).

### Implicación 4 — Adoptar lessons del cambio de paradigma

| Lesson | Aplicación |
|---|---|
| Estado mutable en BD = release SQL = frágil | Frontend `ALL_NAV_LINKS` versionado en git ✅ |
| HREF en backend = acoplamiento | Frontend conoce sus rutas (React Router) ✅ |
| Autoincrement = no portable | `agr_code` natural key (AGR-NNN) ✅ |
| ORDEN manual = renumeración | Orden por agrupación lógica del codename ✅ |
| BEGIN TRAN + ROLLBACK manual | Migration RunPython idempotente con reverse ✅ |
| Sin tests del menú | Tests del bootstrap + DRF integration ✅ |

## Refs

- Script analizado: ``Inserta_modulos_menu.sql`` (legacy IACT,
  proporcionado por ejecutor 2026-05-06).
- Arqueología previa: ``discover/cmenu2-legacy-archeology.md``.
- Análisis principal: ``discover/menu-rbac-user-scope-docs-analysis.md``.
- Backend pre-corpus relevante:
  ``temp-holding/Modules/call_center_privilege_models.py``
  (clase ``CallCenterModule`` que "extiende C_MENU2").
- Corpus vigente:

  - UC_PERM_08: :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`.
  - CNST-032: :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`.
  - ADR-BACK-001 (modelo flat): :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia`.
  - ADR-BACK-007 (custom RBAC): :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`.
  - RBAC implementation guide:
    :doc:`/backend/rbac-implementation-guide`.
