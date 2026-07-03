```yml
created_at: 2026-07-03 22:55:00
project: IACT-docs
work_package: 2026-07-03-22-15-30-auditar-implementacion-ucs-api-ui
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Aprobado
```

# Estado de ramas y PRs — multirepo (2026-07-03)

Pedido del ejecutor: hay PRs abiertos sin considerar y IACT-docs tiene
ramas que solo agregan confusión. Análisis verificado (comandos abajo).

## PRs abiertos (GitHub API, list_pull_requests state=open)

| Repo | PRs abiertos | Detalle |
|---|---|---|
| iact-docs | 4 | #47 actions bump, #46 rpds-py, #39 packaging, #38 more-itertools — todos dependabot → develop |
| iact-ui | 1 | #1 actions bump (dependabot, 2026-05-05) |
| iact-api | 0 | — |
| iact-db | 0 | — |

Observación relacionada (PROVEN): los dependabot pip ya mergeados en
docs (#43 tabulate, #44 click, #45 watchfiles) actualizaron
`pyproject.toml` pero NO `uv.lock` — `uv sync` en esta sesión regeneró
el lock con esas versiones (cambio revertido por estar fuera de scope).
Al mergear #38/#39/#46 conviene regenerar `uv.lock` en el mismo PR.

## Ramas IACT-docs (GitHub: 34 ramas)

```bash
git fetch origin '+refs/heads/*:refs/remotes/origin/*'
git branch -r --merged origin/develop   # => 28 feature/* mergeadas
git branch -r --no-merged origin/develop # => solo 4 dependabot/*
```

- **28 ramas `feature/*` 100% mergeadas en develop** (ancestros
  directos; verificado con `--merged`). Corresponden a iniciativas
  cerradas de 2026-05-19/20 → superan los 30 días de retención de
  git-flow R-08. **Eliminables**.
- 4 `dependabot/*`: conservar (tienen PR abierto).
- `main`, `develop`: conservar.

**Intento de eliminación en esta sesión: BLOQUEADO.** El push de
deleción retorna `HTTP 403` (las credenciales del entorno remoto no
permiten borrar refs). Comando listo para ejecutar desde un clon con
permisos completos:

```bash
cd IACT-docs
git fetch origin '+refs/heads/*:refs/remotes/origin/*'
git branch -r --merged origin/develop | grep 'origin/feature/' \
  | sed 's|.*origin/||' | xargs -I{} git push origin --delete {}
```

Los SHAs de respaldo (tabla abajo) permiten recrear cualquier rama:
`git push origin <sha>:refs/heads/<rama>`.

### SHAs de respaldo de las ramas eliminadas (iact-docs)

| Rama | SHA |
|---|---|
| feature/aclarar-duplicacion-perm-03-acc-08 | 7db3c895465e54aea534c3e24fa2444afbd4878e |
| feature/aclarar-uc-047-resolver-segmento | 4e140a2cb272289ad44a97681d4700d93b7b69f8 |
| feature/adoptar-protocolo-grep-validado-en-auditorias | c5d4aa08c8253fb96d98091d50e6eff879bacef4 |
| feature/alinear-numeracion-uc-api-ui | 4003d13e2633d6b0a077e3bb2e2472ce05599ba4 |
| feature/auditar-cobertura-uc-implementacion | 736475c33acfee3541e0d246d2f0cb60f4da85ed |
| feature/auditar-conformidad-fr-tests-aceptacion | d959047a9519265c0fd3ddc9b3c11631a7b6ca07 |
| feature/declarar-tst-ref-en-58-frs-sin-marcar | b435248914d09979a36348d4e3697d77aff796ee |
| feature/dedupe-fixtures-alerts-iact-api | 7abee2a31f15c1a599bcb6716f41beb9135937f9 |
| feature/documentar-stubs-en-rst-de-uc | 39d8622f522cd338e3b01fd12eaaab313300ae91 |
| feature/documentar-ucs-implementados-no-declarados | b612e23d226c9340d5c65a36c3393118814bb762 |
| feature/enumerar-otros-ucs-inclusion | 1b13e664dc8b07b7153fff61e377d291dff58a84 |
| feature/evolucionar-proc-gob-013-multirepo | 59488403c098cc5e5572c0c477947ef398b089fe |
| feature/habilitar-jest-iact-ui | 54d804b1a5f971530049a61296d00249c9167ae5 |
| feature/habilitar-pytest-iact-api | 76f5d49ec0545cb166d1b73cf7779acf5896208b |
| feature/implementar-uc-rpt-05-06-programacion-reportes | 8fc2b5cd77c8c05d69fcf19590f4d766d681e29d |
| feature/plan-maestro-iniciativas-pendientes | f3dc114a4f07b0d5df0c9fe5131195e224721205 |
| feature/preparar-entorno-mariadb-ivr-legacy | 34c057984af355a1c42306c24942ae8c08b2d796 |
| feature/preparar-entorno-postgresql-iact-analytics | 6551af7f5b3f49cc7b52e1e901e0078a4543b9d6 |
| feature/resolver-tests-alerts-residual-iact-api | 93ebfcce537cfee3b3e954b50144ff6bc85e49d5 |
| feature/resolver-tests-dashboard-iact-api | 60d638bf43d300077377878641704155ba79a63f |
| feature/resolver-tests-dashboard-residual-iact-api | b21d56640f592a3c555695b73c2bcc77029ad34f |
| feature/resolver-tests-fallidos-pytest-iact-api | f89020438bae20d0fe4fab0903501d6e9bdd8d6d |
| feature/resolver-tests-pipeline-residual-iact-api | f1fa67a8a2259fccead93aac9a8987570da11007 |
| feature/sanear-deuda-runtime-multirepo | 8e24d43f5434d9cfc96adb80474bfb3ad3cdf70f |
| feature/sanear-eslint-warnings-iact-ui | d312f6f049242bb95fc42a4a4561816dbcb1cbba |
| feature/sanear-pytest-config-iact-api | c41fa3eac12d81407aadda3a9b099c48a27ea08b |
| feature/separar-ucs-inclusion-de-user-facing | 7e97ac253f5e47afbc4c2b121cabb603c1a14604 |
| feature/verificar-mapping-docs-codigo-todos-los-dominios | 8c893f32bb392c980c94f249326c3774fbddf06a |

## Ramas IACT-api (19)

Las 17 `feature/*` están contenidas en develop (16 por `--merged`;
`feature/e2e-tests-domains-without-integration` con
`rev-list --count origin/develop..rama = 0`). **Candidatas a eliminar
en bloque** — pendiente confirmación del ejecutor (fuera del repo
señalado en el pedido).

## Ramas IACT-ui (9) — ATENCIÓN: trabajo sin integrar

| Rama | Estado | Contenido único |
|---|---|---|
| feature/sanear-eslint-warnings-iact-ui | NO mergeada (3 commits) | eslint --fix (6→0 warnings) + fix webpack producción + override glob v10. **Superset** de las dos siguientes |
| feature/resolver-tests-fallidos-pytest-iact-api | NO mergeada (2 commits) | subconjunto de la anterior |
| feature/sanear-deuda-runtime-multirepo | NO mergeada (1 commit) | subconjunto de la anterior |
| feature/project-structure-analysis | NO mergeada (17 commits) | fix 37 test suites (97/97 passing), sync registry YMLs, cierres de WP — requiere revisión |
| feature/cerrar-uc-usr-07-ui-y-uc-auth-04 | mergeada | eliminable |
| claude/project-analysis-N9IkV | mergeada | eliminable |

Riesgo: iniciativas figuran "cerradas" en docs pero su código ui NO
está en develop. Integrar la punta (`sanear-eslint-warnings-iact-ui`)
absorbe 3 ramas; `project-structure-analysis` requiere decisión aparte.

## Ramas IACT-db (6) — trabajo sin integrar

| Rama | Estado | Contenido único |
|---|---|---|
| feature/resolver-tests-pipeline-residual-iact-api | NO mergeada (3 commits) | grants EXECUTE/DML/ROUTINE en ivr_legacy + test_ivr_legacy. **Superset** de las dos siguientes |
| feature/resolver-tests-dashboard-iact-api | NO mergeada (2) | subconjunto |
| feature/resolver-tests-fallidos-pytest-iact-api | NO mergeada (1) | subconjunto |
| feature/integrar-sp-rpt-resumen-abandono-rollup | mergeada | eliminable |

## Recomendaciones (decisión del ejecutor)

1. Mergear o cerrar los 5 PRs dependabot; si se mergean los de pip,
   regenerar `uv.lock` en el mismo PR.
2. ui: abrir PR `feature/sanear-eslint-warnings-iact-ui` → develop
   (absorbe 3 ramas); revisar `project-structure-analysis` por separado.
3. db: abrir PR `feature/resolver-tests-pipeline-residual-iact-api` →
   develop (absorbe 3 ramas).
4. api: eliminar las 17 `feature/*` contenidas (mismo criterio R-08).
5. Tras integrar, eliminar las ramas absorbidas en ui/db.
