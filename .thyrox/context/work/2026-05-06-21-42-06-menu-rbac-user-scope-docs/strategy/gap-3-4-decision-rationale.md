```yml
created_at: 2026-05-06 23:58:00
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
phase: Phase 5 — STRATEGY
author: NestorMonroy
status: Aprobado
version: 1.0.0
parent: strategy/strategy-addendum-gaps-and-module.md
```

# Decision Rationale — Gap #3, Gap #4 y D-MOD-001

> Razonamiento textual del ejecutor sobre las dos decisiones
> arquitectónicas críticas del addendum + la pregunta de si
> se necesita un módulo nuevo. Documenta el "por qué" detrás
> del "qué" del addendum para preservar el razonamiento ante
> futuras revisiones o reapertura de las decisiones.

## Sección 1 — Pregunta del ejecutor: ¿se necesita un nuevo módulo?

### Análisis

| Criterio | MOD_Admin existente | MOD_MEN hipotético |
|---|---|---|
| UCs propuestos | UC_ADM_04, UC_ADM_05 (2) | Idem (2) |
| Función v5.6.0 de MOD_Admin | "catch-all administrativo cross-module" — diseñado precisamente para esto | — |
| Volumen para justificar módulo propio | Bajo (2 UCs administrativos + 1 endpoint en MOD_PERM) | — |
| Consume slot reservado AGR-011/012 | No | Sí (gasta 1 de 2 reservados) |
| CNST-029 modelo plano | Preservado | Presión a expandir sin orthogonalidad |
| Separación de concerns | UC_ADM_04/05 son admin-only — MOD_Admin es el sitio canónico | Marketing más que arquitectura |

### Localización canónica

| Capability / artefacto | Módulo |
|---|---|
| `manage_menu_catalog` (UC_ADM_04) | **MOD_Admin** (catálogo CRUD) |
| `manage_menu_lifecycle` (UC_ADM_05) | **MOD_Admin** (transiciones DRAFT/ACTIVE/DEPRECATED/ARCHIVED) |
| Endpoint `GET /api/v1/menu/` (UC_PERM_08 ext.) | **MOD_PERM** (parte de la resolución de permisos) |
| `MenuItem` (modelo) | `apps/access/` (mismo app que `Function`/`AccessGroup`) |
| Render frontend (ALL_NAV_LINKS + filter) | Sin capability nueva — consume las existentes |

### Cuándo sí carving out a MOD_MEN

Solo si surge una de estas condiciones en el futuro:

- **i18n del catálogo** con flujo editorial (>3 UCs).
- **A/B testing** o variantes por segmento del menú.
- **Auditoría de uso del menú** con telemetría dedicada como producto.
- **Menu marketplace** o customización por tenant.

Mientras MOD_Admin absorba con 2 UCs, no hay caso. Esto se
documenta en el addendum como **decisión D-MOD-001: no nuevo
módulo MOD_MEN en este WP**.

## Sección 2 — Gap #3: Razonamiento de la decisión

**Pregunta:** ¿quién tiene autoridad de forzar archivado tras
90 días en estado DEPRECATED?

**Decisión adoptada:** Opción b — auto-archive con opt-out.

### Por qué se rechazaron las otras opciones

**Opción a — escalamiento a CIO/product owner:**

> *"Convierte un problema técnico en un proceso político. Si
> el product owner no responde, el item queda en DEPRECATED
> indefinidamente de todas formas, y el escalamiento se
> vuelve ruido que se ignora con el tiempo."*

El escalamiento como mecanismo único depende de que un
humano accionable reciba, lea y actúe sobre la notificación.
En sistemas con muchos items, las notificaciones se vuelven
ruido y se ignoran. La inacción tiene el mismo resultado que
no tener política.

**Opción c — release-block:**

> *"Es demasiado agresiva para este caso. Bloquear un deploy
> de producción por un item de menú en estado DEPRECATED
> durante 91 días mezcla la cadencia de releases con la
> gestión del catálogo de menú. Son dos concerns distintos
> y no deben bloquearse mutuamente."*

Acoplar la cadencia de releases con la higiene del catálogo
de menú viola separación de concerns. El cost de oportunidad
de un release bloqueado por un MenuItem deprecado supera el
beneficio de forzar acción.

### Por qué Opción b es la correcta

> *"Invierte la carga de acción: el sistema archiva por
> defecto y quien quiere mantener el item en DEPRECATED debe
> tomar una acción explícita con `block_auto_archive=True`.
> Eso fuerza una decisión consciente en lugar de permitir la
> inacción indefinida."*

**Principio aplicado:** *default safe action + explicit
opt-out*. El default debe ser el comportamiento que el sistema
prefiere (archive); el comportamiento alternativo requiere
acción explícita y trazable.

### Condición adicional del ejecutor

> *"El flag `block_auto_archive=True` debe requerir
> justificación obligatoria en un campo `block_reason` y
> debe generar una entrada en el audit log con la identidad
> de quien lo puso. Sin eso, el flag se convierte en una
> forma de silenciar el sistema sin responsabilidad."*

**Mitigación implementada en el addendum §4:**

- Campo `block_reason` (CharField, obligatorio, ≥ 20 chars).
- Campo `block_set_by` (FK a User, obligatorio).
- Campo `block_set_at` (DateTimeField, obligatorio).
- Audit log entry en cada cambio del flag.
- Validación en `MenuItem.clean()` que rechaza
  `block_auto_archive=True` sin `block_reason` válido.

**Trade-off explícito aceptado:** un admin puede mantener un
item bloqueado para siempre, pero ahora con responsabilidad
trazable. El sistema no decide políticamente; trazabilidad sí
garantiza accountability.

## Sección 3 — Gap #4: Razonamiento de la decisión

**Pregunta:** ¿el cache TTL 300s es seguro para capabilities
de escritura tras revocación?

**Decisión adoptada:** Opción b — bypass selectivo con
`Function.is_critical`.

### Por qué se rechazaron las otras opciones

**Opción a — bypass total para writes:**

> *"Es innecesariamente costosa. La mayoría de los endpoints
> de escritura en un sistema administrativo tienen baja
> frecuencia de uso. Ir a DB en cada request mutating para
> todas las write capabilities agrega latencia donde
> estadísticamente no hay riesgo real."*

Costo de latencia generalizado para mitigar riesgos puntuales.
Trata todas las writes como si tuvieran el mismo perfil de
riesgo, lo cual es falso (e.g., `update_user_profile` ≠
`assign_functions`).

**Opción c — TTL corto para writes:**

> *"Es una solución a medias. TTL de 10 segundos sigue siendo
> eventual consistency, solo más corta. En 10 segundos una
> capability revocada de emergencia sigue siendo explotable.
> Si el riesgo justifica TTL corto, justifica bypass directo."*

10 segundos es una ventana suficiente para que un atacante
con sesión activa cause daño significativo en operaciones
críticas. La consistency más débil con un timer no es la
solución correcta cuando el riesgo justifica strong consistency.

**Opción d — aceptar eventual consistency total:**

> *"Es aceptable para capabilities de lectura, pero hay al
> menos dos capabilities en el catálogo v5.6.0 donde cache
> stale es un riesgo real: `assign_functions` y
> `manage_menu_catalog`. Si alguien con esa capability es
> comprometido y se le revoca el acceso, los 300 segundos de
> ventana son suficientes para causar daño."*

Demostrado por contraejemplo: existen capabilities específicas
en el catálogo donde 300s de ventana es inaceptable. Una
política única no puede manejar el espectro completo.

### Por qué Opción b es la correcta

> *"Es el balance correcto porque:
>
> - Distingue el riesgo real por capability, no por tipo de
>   verbo HTTP.
> - El campo `Function.is_critical` es un dato del catálogo,
>   no lógica en el middleware.
> - Las capabilities marcadas como críticas hacen bypass de
>   cache. Las demás mantienen TTL 300s.
> - El catálogo inicial de `is_critical=True` debería incluir
>   como mínimo: `assign_functions`, `manage_menu_catalog`,
>   `manage_menu_lifecycle`, `revoke_function_group`, y
>   cualquier capability que permita modificar permisos de
>   otros usuarios."*

**Principios aplicados:**

1. *Risk by capability, not by HTTP verb.* No todas las
   writes son iguales; modelar el riesgo en el catálogo, no
   en el middleware.
2. *Data-driven security.* Mover la decisión de seguridad al
   modelo de datos lo hace versionable, auditable y
   migrable. No vive como hardcoded list en código.
3. *Default cache, explicit bypass.* La mayoría de
   capabilities siguen el comportamiento eficiente; solo las
   marcadas explícitamente pagan el costo de DB-direct.

### Condición adicional del ejecutor — governance del flag

> *"`is_critical` no debería ser editable en runtime por un
> admin común. Cambiar ese flag debe requerir el mismo nivel
> de acceso que modificar una constraint normativa, o de lo
> contrario un atacante con acceso a `manage_function_catalog`
> podría marcar su propia capability como
> `is_critical=False` antes de ser revocado."*

**Vector de ataque mitigado:**

```
Atacante tiene `manage_function_catalog` (compromiso o insider).
Sabe que va a ser revocado.
Acción 1: edita `Function.is_critical=False` en sus capabilities.
Acción 2: cache TTL 300s ahora aplica a las que antes eran críticas.
Acción 3: el admin revoca, pero el cache permite usar las caps por 300s.
```

**Mitigación implementada en el addendum §5:**

1. Cambios al flag `is_critical` SOLO via Django RunPython
   data migration (canónica), nunca via endpoint admin.
2. UI admin de `Function` muestra `is_critical` como
   read-only.
3. Pull request al repositorio de migrations RBAC con review
   ≥ 2 aprobaciones.
4. Capability dedicada `manage_critical_function_flag`
   restringida a un AGR especial; ningún rol del catálogo
   v5.6.0 actual la tiene.
5. Decisión sobre AGR-013 (slot reservado) vs hardcoded
   queda diferida a Phase 7 (ADR-BACK-010 nuevo).

**Principio aplicado:** *defense-in-depth aplicada al
mecanismo de seguridad mismo*. La política de seguridad debe
ser inmutable desde la superficie que protege. Si el flag
que protege fuera editable por el rol que protege, la
defensa colapsa.

## Sección 4 — Resumen de decisiones del ejecutor

| Gap | Opción elegida | Condición adicional |
|---|---|---|
| Gap #3 — autoridad tras 90d en DEPRECATED | b. Auto-archive con opt-out | `block_auto_archive=True` requiere campo `block_reason` obligatorio (≥ 20 chars) y entrada en audit log con `block_set_by` + `block_set_at` |
| Gap #4 — cache para capabilities de escritura | b. Bypass selectivo con `Function.is_critical` | El flag `is_critical` no debe ser editable por el mismo rol que gestiona el catálogo de funciones; requiere acceso equivalente a constraint normativa (migration-only) |

## Sección 5 — Catálogo inicial de capabilities críticas

Capabilities con `is_critical=True` desde el día 1:

| Capability | Razón |
|---|---|
| `assign_functions` | Modifica permisos de otros usuarios |
| `revoke_function_group` | Modifica permisos de otros usuarios |
| `manage_menu_catalog` | Modifica catálogo UX que afecta a todos |
| `manage_menu_lifecycle` | Idem (transiciones de estado afectan render para todos) |
| `manage_function_catalog` | Modifica el catálogo RBAC mismo |
| `manage_access_groups` | Modifica composición de AGRs |
| `delete_user`, `delete_function`, `delete_access_group` | Acciones irreversibles sobre RBAC |

> Catálogo definitivo se cierra en Phase 7 al especificar
> UC_ADM_04 y la extensión de UC_PERM_08.

## Sección 6 — Trazabilidad

| Razonamiento del ejecutor | Implementado en |
|---|---|
| "default safe action + explicit opt-out" | addendum §4 — auto-archive default + block_auto_archive flag |
| "block_reason obligatorio + audit log" | addendum §4 — modelo MenuItem extension + clean() validation |
| "risk by capability, not by HTTP verb" | addendum §5 — Function.is_critical en catálogo |
| "data-driven security" | addendum §5 — flag versionable via migration |
| "default cache, explicit bypass" | addendum §5 — AP-2a vs AP-2b, has_capability() decide via catálogo |
| "defense-in-depth aplicada al mecanismo mismo" | addendum §5 — governance restrictiva del flag is_critical |
| "MOD_Admin absorbe sin presión" | addendum §1 — D-MOD-001 |
| "carving out MOD_MEN solo si i18n / A/B / marketplace" | addendum §1 — trigger de revisión futura |

## Refs

- Addendum técnico: `strategy/strategy-addendum-gaps-and-module.md`.
- Strategy principal: `strategy/menu-rbac-user-scope-solution-strategy.md`.
- Review pre-gate del ejecutor (mensaje 2026-05-06 23:50).
- Decisiones del ejecutor (mensaje 2026-05-06 23:55).
