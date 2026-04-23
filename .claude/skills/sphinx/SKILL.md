---
name: sphinx
description: "Build, configure, and extend professional documentation with Sphinx"
version: "1.0.0"
author: "Claude Code"
status: "active"
metadata:
  triggers:
    - command: "/sphinx"
    - pattern: "*.rst"
    - pattern: "conf.py"
    - pattern: "Makefile"
  capabilities:
    - "build-documentation"
    - "validate-rst-syntax"
    - "configure-sphinx"
    - "create-extensions"
    - "manage-themes"
    - "integrate-builders"
    - "troubleshoot-builds"
  dependencies:
    - "sphinx>=5.0"
  context:
    file_types: [".rst", ".md", "conf.py"]
    domains: ["documentation", "build-systems", "content"]
    complexity: "intermediate"
---

# Sphinx Documentation Builder Skill

## Overview

**Sphinx** is a professional documentation engine that transforms plain-text source files (reStructuredText or Markdown) into beautifully formatted documentation in multiple output formats (HTML, PDF, ePub, man pages, etc.).

This skill provides:
- Understanding of Sphinx's architecture and build pipeline
- Guidance for creating and configuring documentation projects
- Patterns for extending Sphinx with custom directives and roles
- Troubleshooting strategies for common build issues
- Integration strategies for modern documentation workflows

**Core value:** Sphinx enables **single-source documentation** that can be published to web, PDF, and other formats automatically.

---

## Quick Start

### 1. Create a New Documentation Project

```bash
# Initialize Sphinx project
sphinx-quickstart docs/

# Follow prompts:
# - Project name: Your Project
# - Author name: Your Name
# - Release: 1.0.0
# - Language: en
```

### 2. Create Your First Document

**File: `docs/source/index.rst`**
```rst
Welcome to My Project
======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

### 3. Build Documentation

```bash
# Build HTML documentation
cd docs/
make html

# Output in docs/build/html/index.html
# Open in browser to preview
```

### 4. Configure Theme (Optional)

**Edit `docs/source/conf.py`:**
```python
html_theme = 'pydata_sphinx_theme'  # Modern, responsive theme
extensions = [
    'sphinx.ext.autodoc',           # Auto-document Python code
    'myst_parser',                  # Support Markdown (.md) files
    'sphinx_rtd_theme',             # Alternative: Read the Docs theme
]
```

### 5. Rebuild

```bash
make clean html
# Open docs/build/html/index.html
```

---

## Core Concepts

### 1. Directives (Content Blocks)

Directives are extensions to reStructuredText that create structured content blocks.

**Syntax:**
```rst
.. directive-name:: argument
   :option-key: option-value
   
   Content block
```

**Common directives:**

| Directive | Purpose | Example |
|-----------|---------|---------|
| `code-block` | Code with syntax highlighting | `.. code-block:: python` |
| `image` | Embed images | `.. image:: /path/to/img.png` |
| `toctree` | Table of contents tree | `.. toctree:: :maxdepth: 2` |
| `admonition` | Note, warning, tip boxes | `.. note::`, `.. warning::` |
| `literalinclude` | Include code from files | `.. literalinclude:: main.py` |
| `autodoc` | Generate docs from docstrings | `.. automodule:: mypackage` |

**Example - Code block with language highlighting:**
```rst
.. code-block:: python
   :linenos:
   :emphasize-lines: 2, 3
   
   def hello(name):
       """Greet someone."""
       return f"Hello, {name}!"
```

### 2. Roles (Inline Markup)

Roles apply inline styling or create references within text.

**Syntax:**
```rst
:role:`content`
```

**Common roles:**

| Role | Purpose | Example |
|------|---------|---------|
| `:code:` | Inline code | `:code:`import sphinx`` |
| `:ref:` | Cross-reference | `:ref:`section-label`` |
| `:doc:` | Link to document | `:doc:`/guide/installation`` |
| `:py:func:` | Python function ref | `:py:func:`os.path.join`` |
| `:py:class:` | Python class ref | `:py:class:`list`` |
| `:py:mod:` | Python module ref | `:py:mod:`sphinx`` |
| `:kbd:` | Keyboard input | `:kbd:`Ctrl+C`` |

**Example - Cross-reference:**
```rst
See :ref:`installation-guide` for setup instructions.

.. _installation-guide:

Installation Guide
==================
```

### 3. Domains (Language-Specific Documentation)

Domains provide language-specific directives for documenting APIs.

**Python domain:**
```rst
.. py:function:: read_config(path: str) -> dict
   
   Read configuration from file.
   
   :param path: Path to config file
   :return: Configuration dictionary
   :raises FileNotFoundError: If file doesn't exist
```

**Supported domains:**
- `py` - Python
- `c` - C/C++
- `cpp` - C++
- `js` - JavaScript
- `go` - Go
- `rust` - Rust
- And 10+ more

### 4. Extensions (Customization)

Extensions add functionality to Sphinx.

**Built-in extensions:**
```python
extensions = [
    'sphinx.ext.autodoc',          # Auto-generate from docstrings
    'sphinx.ext.intersphinx',      # Link to other Sphinx docs
    'sphinx.ext.todo',             # TODO markup support
    'sphinx.ext.viewcode',         # Add links to source code
    'sphinx.ext.imgmath',          # Render LaTeX math as images
    'myst_parser',                 # Markdown support
    'sphinxcontrib.plantuml',      # PlantUML diagrams
    'sphinx_rtd_theme',            # Read the Docs theme
]
```

### 5. Builders (Output Formats)

Builders convert the parsed documentation into output formats.

**Common builders:**

| Builder | Output | Command |
|---------|--------|---------|
| `html` | Static HTML website | `make html` |
| `dirhtml` | Directory-based HTML | `make dirhtml` |
| `singlehtml` | Single-file HTML | `make singlehtml` |
| `latex` | LaTeX source | `make latex` |
| `pdf` | PDF (via LaTeX) | `make pdf` |
| `epub` | ePub format | `make epub` |
| `man` | Man pages | `make man` |
| `linkcheck` | Validate all links | `make linkcheck` |

---

## Architecture

### Build Pipeline

```
┌─────────────────────────────────────────────────────────┐
│ Source Files (RST, Markdown, Python code)              │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│ 1. PARSE - Read source files & apply directives        │
│    (sphinx/environment.py)                             │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│ 2. BUILD DOCTREE - Create AST (Abstract Syntax Tree)   │
│    (docutils parsing + Sphinx transforms)              │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│ 3. RESOLVE - Cross-references, domains, indices        │
│    (sphinx/environment/collect_metadata.py)            │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│ 4. TRANSFORM - Apply extensions, event hooks           │
│    (app.connect('doctree-resolved') events)            │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│ 5. GENERATE - Write output format (HTML, PDF, etc.)    │
│    (builders/html, builders/latex, etc.)               │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│ Output (HTML files, PDF, ePub, etc.)                    │
└─────────────────────────────────────────────────────────┘
```

### Extension System

Sphinx's extensibility is based on **event-driven architecture**:

```python
# Extension structure (always a setup() function):

def setup(app: Sphinx) -> ExtensionMetadata:
    """Setup custom extension."""
    
    # Register event handlers
    app.connect('config-inited', on_config)
    app.connect('doctree-resolved', on_doctree)
    
    # Register custom directives
    app.add_directive('custom', CustomDirective)
    
    # Register custom roles
    app.add_role('custom', custom_role)
    
    # Register custom domain
    app.add_domain(CustomDomain)
    
    # Return metadata
    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

**Key events (24+ available):**

| Event | Trigger | Use Case |
|-------|---------|----------|
| `config-inited` | After config loaded | Validate/modify settings |
| `env-before-read-docs` | Before processing | Setup caches, temporary state |
| `env-get-outdated` | Determine changed files | Custom change detection |
| `doctree-read` | After parsing RST | Transform raw doctree |
| `doctree-resolved` | After cross-refs | Final transformations |
| `build-finished` | After all output written | Post-processing, cleanup |
| `object-description-transform` | Before rendering | Customize API docs |

---

## Common Tasks

### Task 1: Build HTML Documentation

**Goal:** Generate static HTML website from RST sources

**Steps:**

1. **Ensure Sphinx is installed:**
   ```bash
   pip install sphinx sphinx-rtd-theme myst-parser
   ```

2. **Navigate to docs directory:**
   ```bash
   cd docs/
   ```

3. **Build HTML:**
   ```bash
   make clean html
   ```

4. **View result:**
   ```bash
   # On Linux/Mac
   open build/html/index.html
   
   # On Windows
   start build/html/index.html
   ```

5. **Configure output (optional):**
   Edit `source/conf.py`:
   ```python
   html_theme = 'pydata_sphinx_theme'
   html_theme_options = {
       'navbar_align': 'left',
       'show_nav_depth': 2,
   }
   ```

### Task 2: Create a Custom Directive

**Goal:** Add a reusable content block (e.g., highlight important information)

**Steps:**

1. **Create extension file: `source/ext/highlight_directive.py`**
   ```python
   from docutils import nodes
   from docutils.parsers.rst import Directive
   
   class HighlightDirective(Directive):
       """Custom directive for highlighted content."""
       
       has_content = True
       required_arguments = 0
       option_spec = {'color': str}
       
       def run(self):
           color = self.options.get('color', 'yellow')
           content_node = nodes.emphasis()
           self.state.nested_parse(self.content, 0, content_node)
           return [content_node]
   
   def setup(app):
       app.add_directive('highlight', HighlightDirective)
       return {'version': '1.0.0', 'parallel_read_safe': True}
   ```

2. **Register in `source/conf.py`:**
   ```python
   import sys
   from pathlib import Path
   
   sys.path.insert(0, str(Path(__file__).parent / 'ext'))
   
   extensions = [
       'sphinx.ext.autodoc',
       'highlight_directive',  # Add custom extension
   ]
   ```

3. **Use in RST document:**
   ```rst
   .. highlight:: This is important!
      :color: red
   ```

4. **Build and test:**
   ```bash
   make clean html
   ```

### Task 3: Document Python Code with Autodoc

**Goal:** Auto-generate API documentation from Python docstrings

**Steps:**

1. **Enable autodoc in `conf.py`:**
   ```python
   extensions = [
       'sphinx.ext.autodoc',
       'sphinx.ext.viewcode',  # Link to source code
   ]
   
   # Configure autodoc
   autodoc_default_options = {
       'members': True,
       'inherited-members': True,
       'show-inheritance': True,
   }
   ```

2. **Create API documentation file: `source/api.rst`**
   ```rst
   API Reference
   =============
   
   .. automodule:: mypackage
      :members:
      :undoc-members:
      :show-inheritance:
   ```

3. **Build and verify:**
   ```bash
   make html
   ```

### Task 4: Use Markdown Instead of reStructuredText

**Goal:** Write documentation in Markdown (.md) files

**Steps:**

1. **Install MyST parser:**
   ```bash
   pip install myst-parser
   ```

2. **Enable in `conf.py`:**
   ```python
   extensions = [
       'myst_parser',
   ]
   
   source_suffix = {
       '.rst': 'restructuredtext',
       '.md': 'markdown',
   }
   ```

3. **Create Markdown file: `source/guide.md`**
   ```markdown
   # My Guide
   
   This is a **Markdown** document.
   
   ```python
   print("Hello, World!")
   ```
   ```

4. **Reference in toctree: `source/index.rst`**
   ```rst
   .. toctree::
      
      guide
   ```

5. **Build:**
   ```bash
   make html
   ```

### Task 5: Generate PDF Documentation

**Goal:** Create PDF from RST sources

**Steps:**

1. **Install LaTeX:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install texlive-latex-base texlive-latex-extra
   
   # Mac (with Homebrew)
   brew install basictex
   
   # Windows: Install MiKTeX
   ```

2. **Build LaTeX source:**
   ```bash
   make latex
   ```

3. **Build PDF:**
   ```bash
   make latexpdf
   # or
   cd build/latex
   pdflatex -interaction=nonstopmode MyProject.tex
   ```

4. **Verify output:**
   ```bash
   open build/latex/MyProject.pdf  # Mac
   # or
   start build/latex/MyProject.pdf  # Windows
   ```

### Task 6: Validate Documentation Build

**Goal:** Catch errors during development

**Steps:**

1. **Use warnings-as-errors flag:**
   ```bash
   make clean
   make html SPHINXOPTS="-W --keep-going"
   ```

2. **Check for broken links:**
   ```bash
   make linkcheck
   # Output in build/linkcheck/output.txt
   ```

3. **Validate cross-references:**
   ```bash
   sphinx-build -b html -W source build
   ```

---

## API Reference

### Configuration Options (`conf.py`)

**Core project metadata:**
```python
project = 'My Project'
author = 'Your Name'
release = '1.0.0'
```

**Theme and output:**
```python
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_logo = 'logo.png'
```

**Extensions:**
```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'myst_parser',
]
```

**Language and encoding:**
```python
language = 'en'
source_encoding = 'utf-8'
```

### Extension Interface

**Setup function signature:**
```python
def setup(app: Sphinx) -> ExtensionMetadata:
    """Required setup function for all extensions."""
    
    # app methods
    app.add_directive(name, directive_class)
    app.add_role(name, role_function)
    app.add_config_value(name, default, rebuild)
    app.add_event(name)
    app.connect(event, callback, priority=500)
    
    # Return metadata
    return {
        'version': '1.0.0',
        'parallel_read_safe': bool,
        'parallel_write_safe': bool,
    }
```

### Available Directives

```
RST Content Blocks:
- code-block
- image
- figure
- table
- note / warning / tip / important / caution
- literalinclude
- include
- raw
- toctree
- contents (local table of contents)
- index
- centered
- highlight
- container
```

### Available Roles

```
Inline Markup:
- :code:`...` - inline code
- :ref:`label` - cross-reference
- :doc:`path` - document link
- :download:`path` - downloadable file link
- :kbd:`key` - keyboard input
- :file:`path` - file path
- :envvar:`VAR` - environment variable
- :py:func:, :py:class:, :py:mod: - Python domain
- :c:func:, :c:type: - C domain
- :js:func:, :js:class: - JavaScript domain
```

---

## Advanced Patterns

### Pattern 1: Custom Domain (Language-Specific)

**Use case:** Document custom language or DSL

```python
from sphinx.domains import Domain, Index
from sphinx.roles import XRefRole
from sphinx.directives import Directive

class CustomDomain(Domain):
    """Domain for custom language."""
    
    name = 'custom'
    label = 'Custom'
    roles = {
        'func': XRefRole(),
        'class': XRefRole(),
    }
    directives = {
        'function': CustomFunctionDirective,
        'class': CustomClassDirective,
    }
    
    def resolve_xref(self, env, from_doc, builder,
                     typ, target, node, contnode):
        """Resolve cross-references."""
        return None

def setup(app):
    app.add_domain(CustomDomain)
    return {'version': '1.0.0'}
```

### Pattern 2: Multi-Version Documentation

**Use case:** Document multiple versions simultaneously

**Directory structure:**
```
docs/
├── v1.0/
│   ├── source/
│   └── conf.py
├── v2.0/
│   ├── source/
│   └── conf.py
└── latest/ → symlink to v2.0
```

**Build script:**
```bash
#!/bin/bash
for version in v1.0 v2.0; do
    cd $version
    make clean html
    cd ..
done
```

### Pattern 3: Parallel Build Optimization

**Use case:** Faster builds for large projects

```bash
# Use multiple cores
make html -j4

# Or programmatically
sphinx-build -b html -j 4 source build
```

**Key:** Extensions must declare `parallel_read_safe` and `parallel_write_safe` in metadata.

### Pattern 4: Conditional Content

**Use case:** Build different docs for different audiences

**In `conf.py`:**
```python
tags.add('internal')  # or tags.add('public')
```

**In RST:**
```rst
.. only:: internal

   This is only visible in internal builds.

.. only:: public

   This is only in public builds.
```

**Build:**
```bash
make -e SPHINXOPTS="-t internal" html
```

---

## Troubleshooting

### Problem: "Unknown directive" error

**Cause:** Directive not registered

**Solution:**
1. Check `conf.py` for `extensions` list
2. Ensure extension module is importable: `import myext`
3. Verify directive name matches in `add_directive()`
4. Rebuild with `make clean html`

### Problem: Broken cross-references (`:ref:` role)

**Cause:** Label not defined or misnamed

**Solution:**
```rst
.. _my-section-label:

My Section
==========
```

Then reference as `:ref:`my-section-label`

### Problem: Build takes too long

**Cause:** Processing too many files or slow extensions

**Solution:**
1. Enable parallel builds: `make html -j 4`
2. Check for slow extensions: `sphinx-build -v ...`
3. Exclude unnecessary files: Edit `.gitignore`
4. Cache third-party docs with `intersphinx`

### Problem: PDF generation fails

**Cause:** LaTeX not installed or incompatible characters

**Solution:**
1. Install LaTeX: `apt-get install texlive-latex-full`
2. Check for Unicode issues in conf.py:
   ```python
   latex_elements = {
       'inputenc': '\\usepackage[utf-8]{inputenc}',
   }
   ```
3. Build LaTeX first to see errors: `make latex`

### Problem: Theme not applying

**Cause:** Theme not installed or wrong name

**Solution:**
```python
# In conf.py
html_theme = 'sphinx_rtd_theme'  # Check correct name
# Then install:
# pip install sphinx-rtd-theme
```

### Problem: Autodoc not finding module

**Cause:** Module not in Python path

**Solution:**
```python
# In conf.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))
```

---

## Examples

### Example 1: Simple Directive Implementation

**File: `source/ext/note_directive.py`**
```python
from docutils import nodes
from docutils.parsers.rst import Directive

class NoteDirective(Directive):
    """Custom note directive with title."""
    
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    option_spec = {}
    
    def run(self):
        title = self.arguments[0] if self.arguments else 'Note'
        
        # Create container with styling
        container = nodes.container()
        container['classes'].append('custom-note')
        
        # Add title
        title_node = nodes.title(text=title)
        container += title_node
        
        # Add content
        self.state.nested_parse(
            self.content,
            self.content_offset,
            container
        )
        
        return [container]

def setup(app):
    app.add_directive('note', NoteDirective)
    return {'version': '1.0.0', 'parallel_read_safe': True}
```

### Example 2: Complete conf.py Configuration

```python
"""Sphinx configuration file."""

import sys
from pathlib import Path

# Add extensions
sys.path.insert(0, str(Path(__file__).parent / 'ext'))

project = 'My Project'
author = 'Your Name'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinxcontrib.plantuml',
    'custom_directives',  # Your custom extension
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    'navbar_align': 'left',
    'show_version': True,
}

# PlantUML configuration
plantuml = 'java -jar /usr/share/plantuml/plantuml.jar'

# Autodoc configuration
autodoc_default_options = {
    'members': True,
    'inherited-members': True,
    'show-inheritance': True,
    'private-members': False,
}

# Intersphinx (link to other Sphinx projects)
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# Warnings
warnings_suppressed = ['toc.circular']
```

---

## References

- **Official Sphinx Documentation:** https://www.sphinx-doc.org/
- **Sphinx Extensions:** https://www.sphinx-doc.org/en/master/usage/extensions/index.html
- **reStructuredText Specification:** https://docutils.sourceforge.io/rst.html
- **docutils (RST parser):** https://docutils.sourceforge.io/
- **Common Sphinx Themes:**
  - PyData Sphinx Theme: https://pydata-sphinx-theme.readthedocs.io/
  - Read the Docs Theme: https://sphinx-rtd-theme.readthedocs.io/
  - Furo: https://pradyunsg.me/furo/
- **MyST Parser (Markdown support):** https://myst-parser.readthedocs.io/

---

## Summary

Sphinx provides:
1. **Powerful documentation engine** - Convert RST/Markdown to multiple formats
2. **Extensibility** - Event-driven system for customization
3. **Automated APIs** - Autodoc generates docs from Python docstrings
4. **Ecosystem** - 100+ extensions for themes, builders, content types

**Next steps:**
- Run `sphinx-quickstart` to start your project
- Read the official documentation for deep dives
- Contribute extensions back to the community
