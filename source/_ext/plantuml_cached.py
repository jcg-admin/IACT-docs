"""plantuml_cached — Sphinx extension that overrides the ``uml`` directive
to short-circuit Java/PlantUML rendering when a pre-rendered SVG exists.

Decisions implemented (WP plantuml-svg-prerender):
    D-04 preserve :caption:, :alt:, :align:, :name: options
    D-05 fallback to sphinxcontrib.plantuml when cache misses

Hash function MUST stay aligned with scripts/prerender-plantuml.py:
    sha256(plantuml_styles + "\\n" + normalized_uml_block)[:16]
"""

import hashlib
from pathlib import Path
from typing import List

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList
from sphinx.util import logging

logger = logging.getLogger(__name__)

CACHE_DIR_NAME = "_generated_diagrams"
STYLES_RELATIVE = ("_static", "plantuml-styles.puml")


def _normalize_block(uml_block: str) -> str:
    """Strip common leading whitespace from a multi-line UML block."""
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


def _diagram_hash(uml_block: str, styles: str) -> str:
    normalized = _normalize_block(uml_block).strip()
    full = (styles or "") + "\n" + normalized
    return hashlib.sha256(full.encode("utf-8")).hexdigest()[:16]


class CachedUmlDirective(Directive):
    """Override of sphinxcontrib.plantuml's ``uml`` directive.

    On cache hit (SVG file exists in source/_generated_diagrams/):
        - Emit an ``image`` (or ``figure`` if :caption:) node referencing
          the SVG. Sphinx copies the SVG into the build output.

    On cache miss:
        - Delegate to ``sphinxcontrib.plantuml.UmlDirective`` to perform
          the standard Java-based render.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "caption": directives.unchanged,
        "alt": directives.unchanged,
        "align": directives.unchanged_required,
        "name": directives.unchanged,
        "scale": directives.percentage,
        "width": directives.length_or_percentage_or_unitless,
        "height": directives.length_or_unitless,
    }

    def _styles_text(self, srcdir: Path) -> str:
        styles_path = srcdir.joinpath(*STYLES_RELATIVE)
        if styles_path.exists():
            try:
                return styles_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                # A-06: a silent "" alters the diagram hash for EVERY
                # diagram, invalidating the whole cache and bringing
                # back the OOM via mass miss. Warn loudly instead of
                # failing silently.
                logger.warning(
                    "plantuml_cached: styles file unreadable (%s): %s. "
                    "Diagram hashes will change and the cache will be "
                    "fully invalidated.",
                    styles_path, exc,
                )
                return ""
        # A-06: missing styles file is also a silent cache-wide
        # invalidation; surface it as a warning.
        logger.warning(
            "plantuml_cached: styles file not found at %s. Diagram "
            "hashes will change and the cache will be fully "
            "invalidated.",
            styles_path,
        )
        return ""

    def _build_image_node(self, uri: str) -> nodes.image:
        atts = {"uri": uri}
        for opt in ("alt", "align", "name", "scale", "width", "height"):
            if opt in self.options:
                atts[opt] = self.options[opt]
        return nodes.image(**atts)

    def _delegate_to_plantuml(self) -> List[nodes.Node]:
        try:
            from sphinxcontrib.plantuml import UmlDirective  # type: ignore
        except ImportError:
            logger.error(
                "plantuml_cached: cache miss but sphinxcontrib.plantuml "
                "not available for fallback"
            )
            return [
                nodes.error(
                    "",
                    nodes.paragraph(
                        text=(
                            "PlantUML cache miss and sphinxcontrib.plantuml "
                            "not installed (fallback unavailable)."
                        )
                    ),
                )
            ]
        original = UmlDirective(
            self.name,
            self.arguments,
            self.options,
            self.content,
            self.lineno,
            self.content_offset,
            self.block_text,
            self.state,
            self.state_machine,
        )
        return original.run()

    def run(self) -> List[nodes.Node]:
        env = self.state.document.settings.env
        srcdir = Path(env.srcdir)
        cache_dir = srcdir / CACHE_DIR_NAME

        # Reconstruct the @startuml..@enduml block from directive content.
        body = "\n".join(self.content)
        if not body.strip():
            return self._delegate_to_plantuml()

        styles = self._styles_text(srcdir)
        h = _diagram_hash(body, styles)
        svg_path = cache_dir / f"{h}.svg"

        if not svg_path.exists():
            logger.info(
                "plantuml_cached: miss hash=%s docname=%s",
                h, env.docname,
            )
            return self._delegate_to_plantuml()

        # Cache hit — emit image (or figure with caption) node.
        # URI is relative to the source dir so Sphinx resolves it via _static-style.
        # A-02: log the hit so hit/miss ratio is observable. Without
        # this, only misses were logged and cache degradation (e.g.
        # mass invalidation) was undetectable until an OOM appeared.
        logger.info(
            "plantuml_cached: hit hash=%s docname=%s",
            h, env.docname,
        )
        uri = "/" + CACHE_DIR_NAME + "/" + h + ".svg"
        image_node = self._build_image_node(uri)

        caption = self.options.get("caption")
        if not caption:
            return [image_node]

        figure_node = nodes.figure("", image_node)
        if "align" in self.options:
            figure_node["align"] = self.options["align"]
        # Parse caption as inline RST so cross-references and emphasis work.
        caption_node = nodes.caption()
        caption_lines = StringList(
            [caption], source=env.docname
        )
        self.state.nested_parse(
            caption_lines, self.content_offset, caption_node
        )
        figure_node += caption_node
        return [figure_node]


def setup(app):
    """Sphinx extension entry point.

    Registers ``CachedUmlDirective`` overriding any prior ``uml`` directive.
    Must be loaded BEFORE sphinxcontrib.plantuml in the extensions list,
    or after — both work because directive registration is idempotent
    on the docutils registry (last registration wins). We use
    override=True to be explicit.
    """
    app.add_directive("uml", CachedUmlDirective, override=True)
    return {
        "version": "1.1.0",
        "parallel_read_safe": True,
        # A-01: el fallback de cache miss delega en
        # sphinxcontrib.plantuml, que lanza un proceso Java por
        # render. Declarar parallel_write_safe: True era falso y
        # contribuia al OOM bajo -j auto (multiples JVM
        # concurrentes). Se declara False: Sphinx serializa la
        # escritura, eliminando esa causa raiz.
        "parallel_write_safe": False,
    }
