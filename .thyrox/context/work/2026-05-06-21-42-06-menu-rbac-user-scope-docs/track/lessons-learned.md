```yml
created_at: 2026-05-07 01:50:00
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Lessons Learned — WP menu-rbac-user-scope-docs

> Aprendizajes extraibles del WP. Generalizables a futuros
> WPs de THYROX en este proyecto (IACT-docs).

## L-1: Pre-validacion de catalogo antes de redactar ADRs

**Trigger:** ADR-BACK-010 §3.3 declaro 9 capabilities como
``is_critical=True`` pero 4 de ellas no existian en el
catalogo canonico (``manage_access_groups``,
``delete_function``, ``delete_access_group``, ``delete_user``
con nombre antiguo). Detectado en deep-review (DR-1).

**Aprendizaje:**

Antes de incluir codenames en un ADR, ejecutar:

::

   grep -E "<codename1>|<codename2>" \
     source/requisitos/reglas-negocio/rbac/catalogo-funciones.rst

Si algun codename retorna 0 matches:

- Es nuevo → declarar la capability en el catalogo en el
  mismo PR.
- Tiene otro nombre → usar el nombre canonico.
- No aplica al modelo IACT → no incluir.

**Aplicacion:** integrar al checklist de Phase 7 DESIGN — toda
referencia a un codename RBAC debe verificarse contra el
catalogo canonico antes del primer commit.

## L-2: BR-009 (baja logica) afecta semantica de capabilities

**Trigger:** ADR-BACK-010 incluyo "delete_*" capabilities
asumiendo borrado fisico, pero IACT aplica
**BR-009 baja logica** (soft delete via ``is_active=False``).
El catalogo no tiene ``delete_function``, ``delete_access_group``;
``delete_users`` fue renombrado a ``deactivate_users``
(RENAME v5.4.0).

**Aprendizaje:**

En IACT, "borrar" = "desactivar" (toggle ``is_active``). Las
capabilities de tipo ``delete_*`` no existen como tales —
quedan cubiertas por ``manage_*_catalog`` (que incluye
deactivate) o ``deactivate_*`` (capabilities especificas).

**Aplicacion:** al razonar sobre operaciones irreversibles
RBAC, considerar que IACT no las tiene como tales — el
sistema retiene historico via ``is_active=False`` para
auditabilidad.

## L-3: Razonamiento del ejecutor preservado verbatim

**Trigger:** En gap #3 y gap #4, el ejecutor aporto
razonamiento explicito sobre por que opcion b fue
seleccionada y por que las otras opciones fueron rechazadas.
Ese razonamiento se preservo en
``strategy/gap-3-4-decision-rationale.md`` con citas literales.

**Aprendizaje:**

Cuando el ejecutor toma decisiones arquitectonicas con
razonamiento detallado:

1. Documento separado ``rationale`` aparte de la decision
   tecnica.
2. Citas literales en bloque (``> "..."``) para preservar
   intencion.
3. Documento adversarial (lo que se rechazo + por que).

Beneficio: en revisiones futuras, no se reabren decisiones
discutidas — el rationale ya esta documentado.

**Aplicacion:** patron a replicar para futuras decisiones
arquitectonicas no triviales.

## L-4: STD-010 + STD-011 enforced en cada PR

**Trigger:** El ejecutor detecto violaciones de STD-011
(aliases ``Sched``, ``Svc``, ``DB``, ``UI``) en commits
intermedios. Tambien detecto inicialmente violacion de
STD-010 (mencion de "Celery") en discover/.

**Aprendizaje:**

Los estandares STD-010 (vocabulario abstracto) y STD-011
(aliases auto-documentados) son **enforced via grep** —
verificacion deterministica antes de commit. Si el commit
introduce nuevos diagramas o narrativa UC, ejecutar:

::

   # STD-010 (vocabulario)
   grep -rE "bcrypt|React|MySQL|Celery|Redis|..." \
     source/requisitos/casos-uso/<modulo>/ \
     --include="*.rst" \
     --exclude="implementacion-tecnica.rst"

   # STD-011 (aliases)
   grep -rn " as [A-Z][A-Z]\?$\| as [a-z][a-z]\?$" \
     source/<archivos-nuevos>/

Resultados vacios = conforme.

**Aplicacion:** ya integrado al filtro pre-commit de Phase 7
(strategy addendum §3 "filtro STD-010 ampliado").

## L-5: Paralelismo del DAG de Phase 7 reduce ~50% el tiempo

**Trigger:** Strategy addendum §6 documento DAG con 5 lotes;
L1 (3 ADRs) y L2 (3 supporting docs) fueron paralelos
logicamente — todos los miembros del lote sin dependencias
mutuas y consumiendo solo outputs de lotes anteriores.

**Aprendizaje:**

Antes de iniciar Phase 7, construir el DAG de artefactos:

1. Identificar quien depende de quien.
2. Agrupar artefactos sin dependencias mutuas en lotes.
3. Lotes mas anchos = mas paralelismo posible.

**Aplicacion:** patron a replicar en futuras Phase 7. Para
WPs grandes (10+ artefactos), graficar DAG explicito reduce
tiempo de ejecucion.

## L-6: Domain-model como punto de cierre

**Trigger:** Solo en Phase 11 (post-Phase 7) se detecto
que faltaban 4 clases en domain-model (``MenuItem``,
``MenuItemRepo``, ``UserCapabilityResolver``,
``MenuLifecycleService``).

**Aprendizaje:**

Cualquier WP que introduzca nuevos modelos persistidos o
servicios canonicos DEBE incluir actualizacion de
``source/arquitectura-tecnica/domain-model/`` como artefacto
explicito de Phase 7.

**Aplicacion:** integrar al checklist de Phase 7 DESIGN para
WPs que toquen el modelo de datos. Si el WP solo agrega UCs
sin nuevos modelos, no aplica.

## L-7: Conteo de capabilities como fuente de verdad

**Trigger:** El conteo "64 funciones activas / 77 declaradas"
estaba en 4+ ubicaciones (``catalogo-funciones``,
``mapeo-uc``, ``BR-006``, ``rbac-implementation-guide``
tests). Cualquier cambio en el catalogo requiere update
sincronizado.

**Aprendizaje:**

El conteo de capabilities es **una propiedad emergente** del
catalogo. Idealmente:

- Generado automaticamente desde el catalogo.
- O documentado en UN solo lugar (catalogo) con referencias
  ``:ref:`` desde otros archivos.

Mientras se mantenga manual: usar grep antes de cerrar el WP
para verificar consistencia:

::

   grep -rnE "[0-9]+ funciones (activas|declaradas|in-scope)" \
     source/requisitos/

**Aplicacion:** considerar agregar test de integridad que
parsea el catalogo y verifica conteos en otros archivos.

## L-8: Versionado del catalogo: baseline + extension

**Trigger:** Las 3 nuevas capabilities (v5.6.x extension) no
debian renombrar el conteo baseline v5.6.0. La Opcion B
(67/80 con label v5.6.x extension) preservo el baseline.

**Aprendizaje:**

Cambios al catalogo deben distinguir:

- **Baseline release** (v5.6.0): set canonico de la version.
- **Extension** (v5.6.x): adiciones trazables a un WP
  especifico.

Tabla diff baseline/extension/current evita confusion en
referencias historicas.

**Aplicacion:** patron a replicar para futuros cambios al
catalogo RBAC.

## L-9: Phase 11 deep-review como gate final

**Trigger:** El ejecutor pidio explicitamente un deep-review
post-Phase 7 antes del cierre. El review detecto DR-1 (lista
de capabilities is_critical desalineada con catalogo) que
hubiera sido bug latente en producccion.

**Aprendizaje:**

Phase 11 TRACK no es solo "documentar lo hecho" — es **gate
de calidad** que verifica:

1. Cobertura de cada decision en artefactos canonicos.
2. Consistencia entre artefactos (e.g., listas duplicadas).
3. Cross-refs entre ADRs/CNSTs.
4. Conformidad con STDs (STD-010, STD-011).
5. Conteos del catalogo (si cambiaron).

Sin este gate, los WPs cierran con deuda tecnica oculta.

**Aplicacion:** Phase 11 deep-review como obligatoria para
WPs que toquen RBAC, UCs nuevos, o domain-model.

## L-10: Aprendizaje meta — escalonamiento de revisiones

**Trigger:** El WP tuvo 3 niveles de review:

1. ``post-design-coverage-review.md`` (gaps G-1..G-10) —
   detecto desalineacion catalogo / mapeo / BR-006.
2. ``dependency-graph-and-domain-model-coverage.md`` (G-11..G-18)
   — detecto clases faltantes domain-model.
3. ``deep-review-coverage.md`` (DR-1..DR-4) — detecto la
   inconsistencia mas profunda (catalogo critico desalineado
   con realidad).

**Aprendizaje:**

Cada review tiene su propio nivel de profundidad:

- Review 1: cobertura de decisiones explicitas.
- Review 2: consistencia con artefactos arquitectonicos.
- Review 3: alineacion con catalogo canonico (mas profundo).

Las inconsistencias mas peligrosas son las que se detectan
solo cuando se combinan datos de multiples archivos. El
deep-review (review 3) es el que mas valor agrega.

**Aplicacion:** considerar en futuros WPs RBAC ejecutar las 3
revisiones secuencialmente, no solo una superficial.

## Refs

- ``track/post-design-coverage-review.md``
- ``track/dependency-graph-and-domain-model-coverage.md``
- ``track/deep-review-coverage.md``
- ``track/menu-rbac-user-scope-docs-changelog.md``
- ``strategy/gap-3-4-decision-rationale.md``
- STD-010, STD-011, BR-009.
