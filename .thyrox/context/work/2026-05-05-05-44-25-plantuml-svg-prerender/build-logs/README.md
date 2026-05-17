```yml
created_at: 2026-05-05 05:55:00
project: IACT-docs
work_package: 2026-05-05-05-44-25-plantuml-svg-prerender
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Build logs — registro de invocaciones make/sphinx-build

## Regla del proyecto

> **Toda invocación de `make` o `sphinx-build` durante el WP
> debe registrarse aquí con timestamp ISO 8601.**

## Convención

Filename: `YYYY-MM-DDTHH-MM-SS-{nombre-corto}.log`

Ejemplos:

- `2026-05-05T05-55-00-build-cache-only-5svgs.log`
- `2026-05-05T06-30-00-prerender-1007-diagrams.log`
- `2026-05-05T07-15-00-build-full-cached.log`

## Contenido mínimo de cada log

```
=== BUILD LOG — {nombre} ===
Timestamp ISO:  2026-05-05T05:55:00Z
Comando:        make clean && sphinx-build -b html -d build/doctrees source build/html
Working dir:    /home/user/IACT-docs
Sphinx version: 8.2.3
Python:         3.11
Branch:         claude/wp-merge-pr-review
HEAD:           {sha}

--- STDOUT ---
{output}

--- STDERR ---
{output}

--- RESULTADO ---
Exit code:      {N}
Wall clock:     {tiempo}
Warnings:       {cuenta}
Errors:         {cuenta}

--- NOTAS ---
{contexto: por qué se corrió, qué se esperaba, qué pasó}
```

## Helper script

Ver `scripts/build-with-log.sh` (creado en T-018, fuera del
plan original).
