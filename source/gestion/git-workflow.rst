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

---

2. Feature Branch Workflow
================================================================================

This section describes how to create a feature branch, make changes, and prepare for merge to develop.

2.1 Create Feature Branch — Step-by-Step
--------------------------------------------------------------------------------

**Prerequisites:** You have git installed, your local repository is cloned, and you are on the develop branch.

**Step 1: Ensure your local develop branch is up to date**

Fetch the latest changes from the remote repository:

.. code-block:: bash

   git fetch origin
   git checkout develop
   git pull origin develop

This ensures you're starting from the latest code. Your local develop should match origin/develop.

**Step 2: Create a new feature branch from develop**

Use the ``git checkout -b`` command to create and switch to a new branch:

.. code-block:: bash

   git checkout -b feature/your-feature-name

**Important:** Create branches from ``develop``, NOT from ``main``. The ``main`` branch is for releases only.

Branch naming must follow the pattern ``feature/kebab-case-description``. Examples:
- ``feature/github-actions-setup``
- ``feature/fix-broken-links``
- ``feature/sphinx-config-refactor``

**Step 3: Make your changes**

Edit files in your working directory. Track changes:

.. code-block:: bash

   # See what changed
   git status

   # See the diff
   git diff

**Step 4: Commit your changes with Conventional Commits**

Stage your changes and commit with the format ``type(scope): description``:

.. code-block:: bash

   git add source/gestion/git-workflow.rst
   git commit -m "docs(git-workflow): add feature branch workflow section"

If your changes span multiple logical units, create multiple commits:

.. code-block:: bash

   git add source/gestion/feature-branch-guide.rst
   git commit -m "docs(guides): add feature branch creation guide"

   git add source/gestion/git-workflow.rst
   git commit -m "docs(git-workflow): document branch naming conventions"

Each commit should be atomic — it should make sense on its own and pass all tests independently.

**Step 5: Push your feature branch to remote with tracking**

Push your branch to the remote repository using ``git push -u``:

.. code-block:: bash

   git push -u origin feature/your-feature-name

The ``-u`` flag sets up tracking, so future ``git push`` commands (without branch name) will know where to push. The output confirms:

.. code-block:: text

   branch 'feature/your-feature-name' set up to track 'origin/feature/your-feature-name'.

**Summary of Commands:**

.. code-block:: bash

   # All steps combined
   git fetch origin && git checkout develop && git pull origin develop
   git checkout -b feature/your-feature-name
   # [make changes]
   git add .
   git commit -m "type(scope): description"
   git push -u origin feature/your-feature-name

2.2 Feature Branch Examples — Real Scenarios
--------------------------------------------------------------------------------

**Scenario 1: Simple Typo Fix**

A contributor notices a typo in the documentation and wants to fix it quickly.

.. code-block:: bash

   # Start from develop
   git fetch origin
   git checkout develop && git pull origin develop

   # Create feature branch for typo fix
   git checkout -b feature/fix-spelling-error

   # Edit the file and fix the typo
   # (open source/requisitos/index.rst and fix "thier" → "their")

   # Commit the fix
   git add source/requisitos/index.rst
   git commit -m "fix(docs): correct spelling error in requirements overview"

   # Push to remote
   git push -u origin feature/fix-spelling-error

   # GitHub will automatically show "Create Pull Request" button
   # Create PR, wait for review and merge

**Scenario 2: Medium Feature — GitHub Actions Workflow**

A developer wants to add automated build validation using GitHub Actions.

.. code-block:: bash

   # Create feature branch
   git fetch origin && git checkout develop && git pull origin develop
   git checkout -b feature/github-actions-build-validation

   # Create workflow file and configuration
   # (create .github/workflows/build-validation.yml)
   git add .github/workflows/build-validation.yml
   git commit -m "feat(github-actions): add Sphinx build validation workflow"

   # Add documentation for the workflow
   # (edit source/gestion/ci-cd-guide.rst)
   git add source/gestion/ci-cd-guide.rst
   git commit -m "docs(ci-cd): document build validation workflow setup"

   # Add tests for the workflow
   # (create tests/test_build_validation.py)
   git add tests/test_build_validation.py
   git commit -m "test(ci-cd): add integration tests for build workflow"

   # Push all commits
   git push -u origin feature/github-actions-build-validation

   # Create PR, reviewers examine commits, discuss in PR thread
   # Iterate if needed, then merge

**Scenario 3: Large Feature — Architecture Refactor**

A team wants to refactor Sphinx configuration for maintainability.

.. code-block:: bash

   # Create feature branch
   git fetch origin && git checkout develop && git pull origin develop
   git checkout -b feature/sphinx-config-modularization

   # Refactor: split conf.py into modules
   # (create source/_config/extensions.py)
   git add source/_config/extensions.py
   git commit -m "refactor(sphinx): extract extension configuration to module"

   # Create another module
   # (create source/_config/build-options.py)
   git add source/_config/build-options.py
   git commit -m "refactor(sphinx): extract build options to module"

   # Update main conf.py to import modules
   # (edit source/conf.py)
   git add source/conf.py
   git commit -m "refactor(sphinx): consolidate configuration imports"

   # Add documentation
   # (create source/gestion/sphinx-configuration-guide.rst)
   git add source/gestion/sphinx-configuration-guide.rst
   git commit -m "docs(sphinx): add configuration module guide"

   # Add tests
   # (create tests/test_sphinx_config.py)
   git add tests/test_sphinx_config.py
   git commit -m "test(sphinx): add configuration module tests"

   # Push entire feature branch with all commits preserved
   git push -u origin feature/sphinx-config-modularization

   # Create PR, reviewers see all commits and understand refactoring progression
   # Team discusses, makes suggestions, contributor iterates
   # After approval, merge with --no-ff to preserve history

2.3 Branch Naming Conventions
--------------------------------------------------------------------------------

All feature branches must follow these naming rules for consistency and automation:

**Pattern:** ``feature/kebab-case-description``

**Rules:**

- **Prefix**: Always start with ``feature/`` (not ``feat/``, not ``feature-``)
- **Case**: Use **kebab-case** (lowercase with hyphens)
- **Descriptive**: Branch name should describe the feature, not be overly generic
- **Source**: Create from ``develop`` branch, NEVER from ``main``

**Valid Branch Names:**

- ``feature/github-actions-setup`` ✓
- ``feature/fix-broken-links`` ✓
- ``feature/sphinx-config-modularization`` ✓
- ``feature/api-authentication`` ✓
- ``feature/user-guide-rewrite`` ✓

**Invalid Branch Names:**

- ``feature/GitHub-Actions-Setup`` ✗ (PascalCase, not kebab-case)
- ``feature/github_actions_setup`` ✗ (snake_case, not kebab-case)
- ``feature/feature-1`` ✗ (not descriptive)
- ``new-feature`` ✗ (missing ``feature/`` prefix)
- ``GitHub-Actions`` ✗ (missing ``feature/`` prefix, PascalCase)
- ``main`` ✗ (don't create features from main)

**Why These Rules?**

- **Consistency**: Teams can scan branch lists and immediately understand what each branch contains
- **Automation**: CI/CD tools can detect feature branches by prefix and apply automatic checks
- **Prevent mistakes**: The ``feature/`` prefix prevents accidental pushes to main
- **Searchability**: ``git branch -l feature/*`` finds all active features

**Example — List all feature branches:**

.. code-block:: bash

   git branch -l feature/*

   # Output:
   # feature/github-actions-setup
   # feature/sphinx-config-modularization
   # feature/api-authentication

