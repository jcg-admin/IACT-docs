# Troubleshooting Sphinx Builds

## "Unknown directive" or "Unknown role"

**Cause:** Directive/role not registered

**Solution:**
1. Check if extension is in `conf.py` extensions list
2. Verify extension is importable: `python -c "import myext"`
3. Check directive name matches `app.add_directive()`
4. Run `make clean html` to clear cache

## Broken Cross-References (`:ref:`, `:doc:`)

**Cause:** Label doesn't exist or is misnamed

**Solution:**
```rst
.. _my-section-label:

My Section
==========

Reference it as: :ref:`my-section-label`
```

## Build Takes Too Long

**Cause:** Processing all files or slow extensions

**Solution:**
- Use parallel: `make html -j 4`
- Run `make clean` first
- Check slow extensions: `sphinx-build -v ...`

## PDF Generation Fails

**Cause:** LaTeX not installed

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install texlive-latex-full

# macOS
brew install basictex

# Windows
# Install MiKTeX from https://miktex.org/
```

## Theme Not Applying

**Cause:** Theme not installed or wrong name

**Solution:**
```python
# conf.py
html_theme = 'sphinx_rtd_theme'
# Then: pip install sphinx-rtd-theme
```

## Autodoc Not Finding Module

**Cause:** Module not in Python path

**Solution:**
```python
# conf.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))
```

## "toctree node doesn't match any files"

**Cause:** Document referenced in toctree doesn't exist

**Solution:**
- Check spelling of filenames
- Make sure files are in same directory or use correct paths
- Check extension: `.rst` or `.md`
