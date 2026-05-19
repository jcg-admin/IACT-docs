#!/usr/bin/env python3
"""prerender-plantuml.py — Pre-render PlantUML diagrams to SVG cache.

Walks all .rst files under ``source/``, extracts ``@startuml..@enduml``
blocks from ``.. uml::`` directives, hashes content with the global
plantuml-styles.puml, and renders missing SVGs to
``source/_generated_diagrams/{hash}.svg``.

Idempotent: re-running with no source changes is a no-op (only checks
file existence by hash).

Usage:
    python3 scripts/prerender-plantuml.py [--dry-run] [--source DIR] [--limit N]

Decisions implemented (WP plantuml-svg-prerender):
    D-01 hash = sha256(styles + uml_block)[:16]
    D-02 SVG output format
    D-03 path source/_generated_diagrams/ (persists make clean)
    D-08 plantuml CLI invocation (no -cfgfile — see WP plantuml-cache-prerender-update)
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterator, Tuple

# Paths relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "source"
CACHE_DIR = SOURCE_DIR / "_generated_diagrams"
STYLES_FILE = SOURCE_DIR / "_static" / "plantuml-styles.puml"
PLANTUML_BIN = REPO_ROOT / "tools" / "bin" / "plantuml"

# Match @startuml..@enduml blocks. They live inside `.. uml::`
# directives in RST so they typically have leading whitespace; we allow
# any indentation level.
UML_BLOCK_RE = re.compile(
    r"^[ \t]*@startuml\b.*?^[ \t]*@enduml\b",
    re.MULTILINE | re.DOTALL,
)

# Paths excluded from pre-render: working/backup areas that are also
# excluded from the Sphinx build via exclude_patterns in conf.py.
# Pre-render must match that exclusion or it reports phantom errors
# on RST content that is not part of the published corpus.
EXCLUDED_PATH_PARTS = (
    "wp-tmp",
    "temp-backup",
    "temp-holding",
    "_build",
    ".venv",
)

# Directives whose content is *example text*, not real UML. @startuml
# blocks appearing inside these directives must be skipped — they
# are syntax examples shown to readers, not diagrams to render.
CODE_DIRECTIVE_RE = re.compile(
    r"^(?P<indent>[ \t]*)\.\. (?:code-block|code|sourcecode|highlight|literalinclude)::",
)
UML_DIRECTIVE_RE = re.compile(
    r"^(?P<indent>[ \t]*)\.\. uml::",
)


def is_excluded_path(rst_path: Path) -> bool:
    """Return True if the RST file lives under an excluded directory."""
    parts = set(rst_path.parts)
    return any(p in parts for p in EXCLUDED_PATH_PARTS)


def find_rst_files(source: Path) -> Iterator[Path]:
    """Yield all .rst files under source/, sorted for determinism.

    Files under EXCLUDED_PATH_PARTS (e.g. wp-tmp/) are skipped because
    they are also excluded from the Sphinx build.
    """
    for path in sorted(source.rglob("*.rst")):
        if is_excluded_path(path):
            continue
        yield path


def _block_is_in_code_directive(text: str, start_pos: int) -> bool:
    """True if the @startuml block at ``start_pos`` is inside a code-like
    directive (``.. code-block::``, ``.. code::``, ``literalinclude``, etc.)
    at *any* nesting depth. Such blocks are example text, not diagrams.

    Strategy: walk backwards collecting every directive at strictly
    decreasing indent level (each one is an ancestor of the block).
    If any ancestor is a code-like directive, return True — even if a
    closer ``.. uml::`` ancestor exists, because that ``.. uml::`` is
    itself rendered as literal text inside the outer code-block.
    """
    line_start = text.rfind("\n", 0, start_pos) + 1
    line_end = text.find("\n", line_start)
    if line_end == -1:
        line_end = len(text)
    block_line = text[line_start:line_end]
    block_indent = len(block_line) - len(block_line.lstrip())

    pos = line_start - 1
    current_max_indent = block_indent
    while pos > 0:
        prev_line_start = text.rfind("\n", 0, pos) + 1
        line = text[prev_line_start:pos]
        stripped = line.strip()
        if stripped:
            indent = len(line) - len(line.lstrip())
            if indent < current_max_indent:
                # Candidate ancestor directive (or content) at outer
                # indent level.
                if CODE_DIRECTIVE_RE.match(line):
                    return True
                # Keep walking to find still-outer ancestors. The
                # `.. uml::` ancestor alone is not conclusive — it may
                # itself be inside a code-block.
                current_max_indent = indent
                if current_max_indent == 0:
                    # Cannot find a more-outer directive than column 0.
                    break
        pos = prev_line_start - 1
    return False


def extract_uml_blocks(rst_path: Path) -> list[str]:
    """Extract real @startuml..@enduml blocks from a single RST file.

    Skips blocks that appear inside code-like directives (those are
    syntax examples, not diagrams to render).

    Returns the raw text of each block (including @startuml/@enduml).
    """
    try:
        text = rst_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    out: list[str] = []
    for m in UML_BLOCK_RE.finditer(text):
        if _block_is_in_code_directive(text, m.start()):
            continue
        out.append(m.group(0))
    return out


def normalize_block(uml_block: str) -> str:
    """Normalize indentation so the same diagram in different RST files
    produces the same hash regardless of leading whitespace.

    Strategy: find the minimum leading whitespace common to all non-empty
    lines and strip it.
    """
    lines = uml_block.splitlines()
    non_empty = [ln for ln in lines if ln.strip()]
    if not non_empty:
        return uml_block
    indent = min(len(ln) - len(ln.lstrip()) for ln in non_empty)
    if indent == 0:
        return uml_block
    return "\n".join(
        ln[indent:] if len(ln) >= indent else ln for ln in lines
    )


def diagram_hash(uml_block: str, styles: str) -> str:
    """sha256(styles + "\n" + normalized_uml_block)[:16] hex."""
    normalized = normalize_block(uml_block).strip()
    full = (styles or "") + "\n" + normalized
    return hashlib.sha256(full.encode("utf-8")).hexdigest()[:16]


def render_to_svg(uml_block: str, svg_path: Path) -> Tuple[bool, str]:
    """Render a single PlantUML block to SVG.

    Returns (success, error_message).
    """
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    # Write the block to a temp .puml in the cache dir to leverage local paths.
    # Strip "@startuml NAME" → "@startuml" so PlantUML writes the SVG to
    # {hash}.svg (stem of the .puml file) instead of NAME.svg. The hash is
    # computed from the original block, so runtime cache lookup still
    # matches. Without this strip, named diagrams produce SVGs at the wrong
    # path and the script reports "no output" while NAME.svg leaks into
    # the cache dir overwriting unrelated legacy files.
    normalized = normalize_block(uml_block)
    normalized = re.sub(
        r"^([ \t]*)@startuml\b[^\n]*",
        r"\1@startuml",
        normalized,
        count=1,
        flags=re.MULTILINE,
    )
    puml_path = svg_path.with_suffix(".puml")
    puml_path.write_text(normalized, encoding="utf-8")
    try:
        # Note: do NOT use -cfgfile with plantuml-styles.puml. That file is
        # designed to be `!include`d from inside @startuml blocks, not used
        # as a CLI cfgfile. Passing it as -cfgfile causes PlantUML to write
        # a "Syntax Error" SVG (line 1 of input file). The styles content
        # still affects the cache hash (so changes invalidate the cache),
        # but PlantUML rendering uses only what is inside the diagram block.
        cmd = [
            str(PLANTUML_BIN),
            "-tsvg",
            "-o", str(svg_path.parent),
            str(puml_path),
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        # Validate: SVG exists, non-empty, and does not contain the
        # PlantUML "Syntax Error" placeholder text (defensive check
        # against future regressions of the kind cfgfile produced).
        if svg_path.exists() and svg_path.stat().st_size > 0:
            try:
                svg_text = svg_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                svg_text = ""
            if "Syntax Error" in svg_text:
                svg_path.unlink(missing_ok=True)
                msg = (result.stderr or result.stdout).strip()
                return False, msg or "plantuml produced Syntax Error SVG"
            return True, ""
        msg = (result.stderr or result.stdout).strip()
        return False, msg or f"plantuml exit {result.returncode}, no output"
    except subprocess.TimeoutExpired:
        return False, "plantuml timeout (60s)"
    except FileNotFoundError:
        return False, f"plantuml binary not found at {PLANTUML_BIN}"
    finally:
        if puml_path.exists():
            puml_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-render PlantUML diagrams to SVG cache"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be rendered without invoking plantuml",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=SOURCE_DIR,
        help=f"Source directory (default: {SOURCE_DIR})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Render at most N missing diagrams (0 = no limit)",
    )
    parser.add_argument(
        "--only",
        type=str,
        default="",
        help="Only process RST files whose path contains this substring",
    )
    args = parser.parse_args()

    if not args.source.exists():
        print(f"ERROR: source directory not found: {args.source}",
              file=sys.stderr)
        return 2

    styles = STYLES_FILE.read_text(encoding="utf-8") if STYLES_FILE.exists() else ""
    if not styles:
        print(f"WARN: styles file not found at {STYLES_FILE}; proceeding",
              file=sys.stderr)

    if not args.dry_run:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    total_blocks = 0
    cached = 0
    rendered = 0
    errors: list[Tuple[Path, int, str]] = []
    rendered_now = 0

    for rst_path in find_rst_files(args.source):
        if args.only and args.only not in str(rst_path):
            continue
        blocks = extract_uml_blocks(rst_path)
        for idx, block in enumerate(blocks, start=1):
            total_blocks += 1
            h = diagram_hash(block, styles)
            svg_path = CACHE_DIR / f"{h}.svg"
            if svg_path.exists():
                cached += 1
                continue
            if args.dry_run:
                rendered += 1
                continue
            if args.limit and rendered_now >= args.limit:
                continue
            ok, err = render_to_svg(block, svg_path)
            if ok:
                rendered += 1
                rendered_now += 1
            else:
                errors.append((rst_path, idx, err))

    print(f"PlantUML pre-render summary:")
    print(f"  Total diagrams found: {total_blocks}")
    print(f"  Cached (skipped):     {cached}")
    print(f"  Rendered (this run):  {rendered}")
    if args.dry_run:
        print("  Mode: DRY RUN")
    if errors:
        print(f"\n  ERRORS ({len(errors)}):")
        for rst_path, idx, err in errors[:20]:
            rel = rst_path.relative_to(REPO_ROOT) if rst_path.is_relative_to(REPO_ROOT) else rst_path
            print(f"    {rel} #{idx}: {err[:200]}")
        if len(errors) > 20:
            print(f"    ... and {len(errors) - 20} more")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
