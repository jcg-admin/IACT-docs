================================================================================
Git Workflow Documentation
================================================================================

This document standardizes Git workflows, branching strategies, and commit conventions for the IACT-docs repository.

.. contents:: Table of Contents
   :local:
   :depth: 2

---

1. Conventional Commits Format
================================================================================

The IACT-docs project follows the Conventional Commits specification to ensure clear, structured commit messages that can be automatically parsed and categorized.

1.1 Valid Commit Types
--------------------------------------------------------------------------------

Every commit must start with one of these seven types, followed by optional scope and description:

**feat**
  A new feature or capability added to the codebase.

  Example: ``feat(api): add user authentication endpoint``

**fix**
  A bug fix or correction to existing functionality.

  Example: ``fix(docs): correct markdown syntax error in requirements``

**docs**
  Changes to documentation, including README, guides, or inline code comments. No code functionality changes.

  Example: ``docs(git-workflow): add branch naming conventions``

**refactor**
  Code reorganization or restructuring that does NOT change behavior. Includes renaming, moving files, or improving code clarity without altering functionality.

  Example: ``refactor(config): reorganize sphinx configuration modules``

**test**
  Adding new tests, updating test suites, or improving test coverage. Includes test infrastructure changes.

  Example: ``test(api): add integration tests for authentication flow``

**perf**
  Performance improvements or optimizations to reduce execution time, memory usage, or resource consumption.

  Example: ``perf(build): optimize image processing in build pipeline``

**chore**
  Maintenance tasks, dependency updates, configuration changes, or tooling improvements that don't affect the build output or functionality. Includes version bumps, CI/CD configuration, and development environment setup.

  Example: ``chore(dependencies): update sphinx from 4.5 to 5.0``

1.2 Commit Message Structure
--------------------------------------------------------------------------------

Complete commit message format:

.. code-block:: text

   type(scope): description

   [optional body paragraphs]
   [optional footer lines]

- **type**: One of feat, fix, docs, refactor, test, perf, chore (required)
- **scope**: Optional but recommended — describes the area affected (e.g., api, docs, config, build)
- **description**: Concise explanation of what changed — present tense, imperative mood (e.g., "add" not "added" or "adds")

Example complete commit:

.. code-block:: text

   feat(github-actions): implement automated build verification

   Add GitHub Actions workflow to validate Sphinx RST syntax
   on every push to develop and main branches. Workflow runs
   build commands and reports failures to PR status checks.

   Closes #42
   Related to RFC-005

1.3 Examples by Type
--------------------------------------------------------------------------------

**feat: Adding a new documentation section**

.. code-block:: bash

   git commit -m "feat(docs): add security best practices guide"

**fix: Correcting a broken link**

.. code-block:: bash

   git commit -m "fix(docs): update broken reference to compliance matrix"

**docs: Updating user documentation**

.. code-block:: bash

   git commit -m "docs(handbook): clarify branch protection procedures"

**refactor: Reorganizing code modules**

.. code-block:: bash

   git commit -m "refactor(config): consolidate sphinx extensions into modules"

**test: Adding integration tests**

.. code-block:: bash

   git commit -m "test(api): add test suite for webhook validation"

**perf: Improving build speed**

.. code-block:: bash

   git commit -m "perf(build): parallelize sphinx documentation builds"

**chore: Updating dependencies**

.. code-block:: bash

   git commit -m "chore(deps): upgrade python-sphinx to 6.0.0"

1.4 Scope Rules (Detailed)
--------------------------------------------------------------------------------

When choosing a scope:

- Use **kebab-case** (lowercase with hyphens): ``git-workflow``, ``branch-protection``, ``config-management`` ✓
- **Do NOT use** PascalCase, snake_case, or spaces: ``GitWorkflow`` ✗, ``git_workflow`` ✗, ``git workflow`` ✗
- Scope is **recommended but optional** for clarity; however, including scope makes commit history much more searchable
- Scope should be **specific to the affected area**, not generic: ``docs`` is acceptable, ``docs(git-workflow)`` is better

Recommended scopes for IACT-docs:

- ``docs`` — Documentation changes (guides, READMEs)
- ``git-workflow`` — Git workflow procedures and branching documentation
- ``github-actions`` — CI/CD workflows and GitHub Actions configurations
- ``sphinx-config`` — Sphinx configuration and build settings
- ``requirements`` — Requirements specifications and analysis documents
- ``api`` — API design or implementation
- ``tests`` — Test suite and testing infrastructure
- ``build`` — Build tooling and compilation
- ``deps`` — Dependency updates and package management

1.5 Scope Rules — Valid and Invalid Examples
--------------------------------------------------------------------------------

The scope must follow these rules for consistency across the project:

+-----------------------------------+---------------------+-------------------------------------------+
| Characteristic                    | Valid Examples      | Invalid Examples                          |
+===================================+=====================+===========================================+
| Case                              | kebab-case          | ``GitWorkflow``, ``git_workflow``,        |
|                                   |                     | ``Git Workflow``, ``GITWORKFLOW``         |
+-----------------------------------+---------------------+-------------------------------------------+
| Length                            | Concise (1-3 words) | ``git-workflow-feature-documentation``,   |
|                                   | separated by hyphens| overly long scopes reduce readability     |
+-----------------------------------+---------------------+-------------------------------------------+
| Content                           | Domain-specific     | Generic: ``misc``, ``stuff``,             |
|                                   | names               | ``change``, ``update``                    |
+-----------------------------------+---------------------+-------------------------------------------+
| Spaces / Special chars            | Hyphens only        | ``git_workflow``, ``git.workflow``,       |
|                                   |                     | ``git/workflow``, ``git workflow``        |
+-----------------------------------+---------------------+-------------------------------------------+

**Valid Scope Examples:**

- ``feat(github-actions): ...`` ✓
- ``fix(sphinx-config): ...`` ✓
- ``docs(api): ...`` ✓
- ``refactor(build): ...`` ✓
- ``test(validation): ...`` ✓
- ``chore(deps): ...`` ✓
- ``feat(docs): ...`` ✓ (simple, single-word scopes are acceptable)

**Invalid Scope Examples:**

- ``feat(GitHub-Actions): ...`` ✗ (PascalCase, not kebab-case)
- ``fix(sphinx_config): ...`` ✗ (snake_case, not kebab-case)
- ``docs(Sphinx Config): ...`` ✗ (spaces and capitals)
- ``refactor(BUILDTOOL): ...`` ✗ (UPPERCASE, not kebab-case)
- ``feat(): ...`` ✗ (empty scope — use no scope instead of empty parens)
- ``feat(git-workflow-update-system): ...`` ✗ (unnecessarily long)

1.6 Body Format — Multi-Paragraph Structure
--------------------------------------------------------------------------------

The commit body is optional but **highly recommended** for non-trivial changes. It provides context about why the change was necessary and any design decisions:

**Formatting Rules:**

- Separate body from subject line with **exactly one blank line**
- Each paragraph should be logically distinct and wrapped at **72 characters**
- Use clear, concise language explaining the **why**, not the **what** (the diff shows the what)
- Structure body in 2–3 paragraphs:

  1. **Problem statement** — What issue or gap does this commit address?
  2. **Solution description** — How does this change solve the problem?
  3. **Additional context** — Design decisions, trade-offs, or considerations for reviewers

**Example: Multi-Paragraph Body**

.. code-block:: text

   feat(github-actions): automate Sphinx build validation on PRs

   The documentation build was only validated after merge to main,
   meaning syntax errors were caught too late. Contributors often
   didn't catch RST formatting issues until CI failed.

   This commit adds a GitHub Actions workflow that runs Sphinx
   build on every push to develop and main branches. Build failures
   are reported as PR status checks, blocking merge if the
   documentation won't compile.

   The workflow runs in parallel with other checks and takes ~2
   minutes, so it doesn't significantly impact CI time. The build
   output is stored as artifacts for 30 days for debugging.

   Closes #42

1.7 Issue References and RFC Citations
--------------------------------------------------------------------------------

Commit messages can link to related issues and documentation by using standard keywords in the footer section (after the body).

**Issue Reference Keywords:**

Use these keywords to link commits to GitHub issues:

- ``Closes #NNN`` — Closes the issue when the PR is merged (preferred for bug fixes and feature implementations)
- ``Fixes #NNN`` — Synonym for Closes (both work identically)
- ``Resolves #NNN`` — Synonym for Closes
- ``Relates to #NNN`` — Links to an issue without automatically closing it (use for partial solutions or related work)
- ``References #NNN`` — Synonym for Relates to

**RFC (Request for Comments) Citations:**

For significant changes, reference any RFC or design document that drove the decision:

- ``Related to RFC-NNN`` — References a design RFC document
- ``Implements RFC-security-framework`` — Indicates the commit fulfills a documented requirement
- ``Updates RFC-api-v2`` — Shows the commit modifies a previous RFC

**Examples with Issue References:**

.. code-block:: text

   fix(docs): correct broken internal link in requirements

   The link to the API specification was using an outdated path.
   Updated to reference the new documentation structure.

   Closes #156

.. code-block:: text

   feat(git-workflow): implement feature branch naming convention

   Standardize branch names to follow feature/* pattern with
   kebab-case project identifiers. This allows automated tooling
   to categorize and track feature progress.

   Relates to #89
   Related to RFC-version-control-standards

.. code-block:: text

   refactor(sphinx-config): modularize extension configuration

   Split monolithic conf.py into separate modules by extension
   category. Improves maintainability and allows selective loading
   of extensions based on environment.

   This refactor aligns with RFC-configuration-management and
   resolves the technical debt tracked in #201.

   References #89
   Related to RFC-configuration-management

1.8 Complete Commit Example with All Elements
--------------------------------------------------------------------------------

Here is a complete, production-ready commit message with subject, body, and footer:

.. code-block:: text

   feat(github-actions): implement automated build verification for docs

   The Sphinx documentation build was only validated after merge,
   meaning contributors didn't catch syntax errors until the build
   failed. This delays feedback and creates rework.

   This commit adds a GitHub Actions workflow that automatically
   runs Sphinx build on every push to develop and main branches.
   Failures are reported as PR status checks, blocking merge if
   documentation doesn't compile.

   The workflow:
   - Runs in ~2 minutes (parallelized)
   - Stores build logs as CI artifacts for debugging
   - Integrates with GitHub branch protection rules
   - Provides immediate feedback to authors

   Closes #42
   Related to RFC-documentation-quality-gates

1.9 Merge Commit Format
--------------------------------------------------------------------------------

When merging a feature branch to develop or main, a merge commit is created with a standardized message that documents the PR and preserved history.

**Why Merge Commits?**

The IACT-docs project uses merge commits (``--no-ff`` flag) instead of squashing commits because:

- **Full history preservation** — Every commit remains visible in the main branch history
- **Traceability** — You can see which commits belong to which feature by following the merge commit
- **Blame accuracy** — ``git blame`` shows the original commit author, not the merger
- **Revert capability** — You can easily revert entire features with ``git revert -m 1 MERGE_COMMIT_SHA``
- **Release notes** — Commit history clearly shows what features were included in each release

**Merge Commit Message Format:**

When GitHub creates a merge commit, it generates a message automatically:

.. code-block:: text

   Merge pull request #PR_NUMBER from feature/feature-name

   Description of the feature or fix included in this PR.
   Multiple paragraphs may follow.

The merge message includes:

- **Merge pull request #NNN** — The PR number (automatic)
- **from feature/branch-name** — The source branch name (automatic)
- **Description** — The PR description, which should follow commit conventions (manual input)

**Guidelines for Merge Commits:**

1. **PR description (the body) must explain the PR contents**, not just the branch name
2. **Include what changed and why** — Same principles as commit bodies
3. **Mention any related issues or RFCs** in the merge message body
4. **Keep the description concise** — 1–3 paragraphs maximum

**Example Merge Commit Message:**

.. code-block:: text

   Merge pull request #156 from feature/github-actions-validation

   Implement automated Sphinx build validation for all PRs.

   This PR adds GitHub Actions workflows that run Sphinx build on
   every push to develop and main branches. Build failures are
   reported as PR status checks, preventing merge of documentation
   that won't compile.

   - Adds .github/workflows/sphinx-build.yml
   - Validates RST syntax before merge
   - Stores build logs as CI artifacts
   - Integrates with branch protection rules

   Closes #42
   Related to RFC-documentation-quality-gates

**Additional Context for Merge Commits:**

The actual merge command (detailed in section 2) will look like:

.. code-block:: bash

   git merge --no-ff feature/github-actions-validation \
     -m "Merge pull request #156 from feature/github-actions-validation

   [PR description here]"

This preserves the entire feature branch history while creating a single merge commit on the develop/main branch.

