#!/usr/bin/env python3
"""migrate-naming.py — STD_007 v2.0.0 universal kebab migration.

Idempotente: corre múltiples veces sin daño.

Uso:
    python migrate-naming.py --dry-run                  # preview completo
    python migrate-naming.py --dry-run --by-category    # agrupado por prefijo
    python migrate-naming.py --pilot <abs-or-rel-path>  # un solo archivo
    python migrate-naming.py --execute                  # aplicar (renames + refs)

Diseño:
    1. Recolecta renames: archivos y directorios que violan v2.0.0.
    2. Renombra archivos vía `git mv` (preserva historial).
    3. Renombra directorios bottom-up vía `git mv`.
    4. Actualiza :doc: y toctree entries en TODO el corpus .rst.

Excepciones (no renombradas):
    - index.rst
    - Directorios con prefijo `_` (Sphinx convention) — el prefijo se
      preserva, el resto se transforma a kebab.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
SOURCE = REPO_ROOT / "source"

PRESERVED_FILE_NAMES = {"index.rst"}


def transform_stem(stem: str) -> str:
    """Transforma stem (sin extensión) a kebab-lowercase."""
    new = stem.lower().replace("_", "-").replace(".", "-")
    new = re.sub(r"-+", "-", new)
    return new.strip("-")


def transform_filename(name: str) -> str:
    if name in PRESERVED_FILE_NAMES:
        return name
    if "." in name:
        stem, ext = name.rsplit(".", 1)
        return transform_stem(stem) + "." + ext
    return transform_stem(name)


def transform_dirname(name: str) -> str:
    if name.startswith("_"):
        return "_" + transform_stem(name[1:])
    return transform_stem(name)


def collect_file_renames():
    out = []
    for dirpath, _, filenames in os.walk(SOURCE):
        for fname in filenames:
            if not fname.endswith((".rst", ".puml")):
                continue
            new = transform_filename(fname)
            if new != fname:
                out.append((Path(dirpath) / fname, Path(dirpath) / new))
    return out


def collect_dir_renames():
    out = []
    for dirpath, dirnames, _ in os.walk(SOURCE):
        for d in dirnames:
            new = transform_dirname(d)
            if new != d:
                out.append((Path(dirpath) / d, Path(dirpath) / new))
    out.sort(key=lambda x: len(x[0].parts), reverse=True)
    return out


def categorize(name: str) -> str:
    """Clasifica el nombre por prefijo para agrupación."""
    upper = name.upper()
    for pref in ["UC_", "BR_", "BREQ_", "CNST_", "META_", "FND_", "SBVR_",
                 "MTM_", "TXM_", "GOB_", "STD_", "TPL_", "ADR-", "PROCED-",
                 "PROC-", "RNF-", "FR-"]:
        if upper.startswith(pref):
            return pref.rstrip("_-")
    return "(sin-prefijo)"


def build_doc_path_map(file_renames, dir_renames):
    """Mapping de paths relativos (sin .rst) viejos → nuevos.

    Para :doc: y toctree, las rutas son relativas a SOURCE y sin .rst.
    """
    mapping = {}
    # Build composite mapping: si un dir cambió, todos sus paths internos
    # quedan reflejados al renombrar primero los archivos y luego dirs.
    # Pero aquí construimos el mapping de paths FINALES.
    # Estrategia: simular renames secuencialmente.

    # Paso 1: archivos
    for old, new in file_renames:
        old_rel = old.relative_to(SOURCE).with_suffix("")
        new_rel = new.relative_to(SOURCE).with_suffix("")
        mapping[str(old_rel).replace(os.sep, "/")] = str(new_rel).replace(os.sep, "/")

    return mapping


def build_dir_segment_map(dir_renames):
    """Mapping de (path_dir_viejo) → (path_dir_nuevo) en formato POSIX."""
    out = {}
    for old, new in dir_renames:
        old_rel = old.relative_to(SOURCE)
        new_rel = new.relative_to(SOURCE)
        out[str(old_rel).replace(os.sep, "/")] = str(new_rel).replace(os.sep, "/")
    return out


# Refs target patterns
DOC_REF_RE = re.compile(r":doc:`([^`<>]*?<)?([^`<>]+?)(>?)`")


def update_refs_in_text(text, file_map, dir_map):
    """Actualiza :doc: refs, toctree entries, paths inline.

    Estrategia conservadora:
    - Reemplazo solo de paths conocidos (mapping completo).
    - Sin transformación heurística.
    """
    new_text = text

    # Sort by length desc para evitar prefix collisions
    file_items = sorted(file_map.items(), key=lambda x: -len(x[0]))
    dir_items = sorted(dir_map.items(), key=lambda x: -len(x[0]))

    # Update :doc:`...` refs
    def repl_doc(match):
        title = match.group(1) or ""
        path = match.group(2)
        closer = match.group(3) or ""
        # Try exact file match (with leading /)
        normalized = path.lstrip("/")
        for old, new in file_items:
            if normalized == old:
                replaced = "/" + new if path.startswith("/") else new
                return ":doc:`" + title + replaced + closer + "`"
        # Try with prefix /sphinx-style absolute path
        for old, new in file_items:
            if normalized == old or normalized.endswith("/" + old):
                replaced = path.replace(old, new, 1)
                return ":doc:`" + title + replaced + closer + "`"
        return match.group(0)

    new_text = DOC_REF_RE.sub(repl_doc, new_text)

    # Update toctree entries (lines inside .. toctree:: blocks)
    new_text = update_toctree_entries(new_text, file_map, dir_map)

    return new_text


def update_toctree_entries(text, file_map, dir_map):
    """Actualiza líneas de toctree replazando paths conocidos."""
    lines = text.split("\n")
    out = []
    in_toctree = False
    toctree_indent = ""

    for raw in lines:
        stripped_left = raw.lstrip()
        if stripped_left.startswith(".. toctree::"):
            in_toctree = True
            toctree_indent = raw[: len(raw) - len(stripped_left)]
            out.append(raw)
            continue

        if in_toctree:
            # Toctree termina cuando hay línea no indentada (o con menos indent)
            if raw.strip() == "":
                out.append(raw)
                continue
            current_indent = raw[: len(raw) - len(stripped_left)]
            if len(current_indent) <= len(toctree_indent):
                in_toctree = False
                out.append(raw)
                continue

            # Línea de opción :maxdepth: o :caption: etc — preservar
            if stripped_left.startswith(":"):
                out.append(raw)
                continue

            # Es un path o "Title <path>"
            content = stripped_left
            m = re.match(r"^(.*?<)([^>]+)(>.*)$", content)
            if m:
                prefix, path, suffix = m.group(1), m.group(2), m.group(3)
            else:
                prefix, path, suffix = "", content.rstrip(), ""

            # Reemplazo
            new_path = replace_path(path, file_map, dir_map)
            new_line = current_indent + prefix + new_path + suffix
            # Preserve trailing newline behavior
            out.append(new_line)
            continue

        out.append(raw)

    return "\n".join(out)


def replace_path(path, file_map, dir_map):
    """Reemplaza path viejo por nuevo si existe en mapping.

    Aplica primero file_map (más específico), luego dir_map.
    """
    cleaned = path.strip()
    if not cleaned:
        return path

    # Quitar leading /
    abs_marker = cleaned.startswith("/")
    norm = cleaned.lstrip("/")

    file_items = sorted(file_map.items(), key=lambda x: -len(x[0]))
    for old, new in file_items:
        if norm == old:
            return ("/" if abs_marker else "") + new

    # No exact file match — try dir prefix
    dir_items = sorted(dir_map.items(), key=lambda x: -len(x[0]))
    for old, new in dir_items:
        if norm == old or norm.startswith(old + "/"):
            replaced = norm.replace(old, new, 1)
            return ("/" if abs_marker else "") + replaced

    return path


def git_mv(src: Path, dst: Path):
    subprocess.run(
        ["git", "mv", str(src), str(dst)],
        check=True,
        cwd=REPO_ROOT,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--by-category", action="store_true")
    ap.add_argument("--pilot", help="Renombrar solo este path (relativo a source/)")
    ap.add_argument("--execute", action="store_true")
    args = ap.parse_args()

    if not (args.dry_run or args.execute or args.pilot):
        ap.error("Use --dry-run, --pilot, o --execute.")

    file_renames = collect_file_renames()
    dir_renames = collect_dir_renames()

    if args.pilot:
        target = (REPO_ROOT / args.pilot).resolve()
        file_renames = [(o, n) for o, n in file_renames if o.resolve() == target]
        dir_renames = []
        if not file_renames:
            print(f"PILOT: {target} no requiere rename o no existe.")
            return

    # Maps
    file_map = build_doc_path_map(file_renames, dir_renames)
    dir_map = build_dir_segment_map(dir_renames)

    print(f"==> {len(file_renames)} archivos a renombrar")
    print(f"==> {len(dir_renames)} directorios a renombrar")

    if args.by_category:
        cat_counts = defaultdict(int)
        for old, _ in file_renames:
            cat_counts[categorize(old.name)] += 1
        print("\nPor categoría:")
        for cat, n in sorted(cat_counts.items(), key=lambda x: -x[1]):
            print(f"  {cat:12s} {n:4d}")

    if args.dry_run:
        print("\n=== ARCHIVOS (primeros 30) ===")
        for old, new in file_renames[:30]:
            print(f"  {old.relative_to(REPO_ROOT)} -> {new.name}")
        if len(file_renames) > 30:
            print(f"  ... y {len(file_renames) - 30} más")

        print("\n=== DIRECTORIOS ===")
        for old, new in dir_renames:
            print(f"  {old.relative_to(REPO_ROOT)} -> {new.name}")

        # Count refs that would be updated
        refs_changed = 0
        for rst in SOURCE.rglob("*.rst"):
            text = rst.read_text()
            new_text = update_refs_in_text(text, file_map, dir_map)
            if new_text != text:
                refs_changed += 1
        print(f"\n==> {refs_changed} archivos .rst con refs/toctree a actualizar")
        return

    if args.execute or args.pilot:
        # 1. Renombrar archivos
        for old, new in file_renames:
            print(f"git mv {old.relative_to(REPO_ROOT)} -> {new.name}")
            git_mv(old, new)

        # 2. Renombrar directorios (bottom-up)
        for old, new in dir_renames:
            print(f"git mv {old.relative_to(REPO_ROOT)} -> {new.name}")
            git_mv(old, new)

        # 3. Actualizar refs en TODO el corpus
        # Recolectar después de los renames físicos
        rst_files = list(SOURCE.rglob("*.rst"))
        updated = 0
        for rst in rst_files:
            text = rst.read_text()
            new_text = update_refs_in_text(text, file_map, dir_map)
            if new_text != text:
                rst.write_text(new_text)
                updated += 1
        print(f"\n==> {updated} archivos .rst con refs actualizadas")


if __name__ == "__main__":
    main()
