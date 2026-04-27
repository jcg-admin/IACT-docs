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

---

---

3. Feature → Develop Merge Workflow
================================================================================

This section describes how to create a pull request from a feature branch to develop, handle code review feedback, resolve conflicts, and merge using GitHub.

3.1 Create a Pull Request — Step-by-Step
--------------------------------------------------------------------------------

**Prerequisites:**
- You have pushed your feature branch to remote (from Section 2)
- Branch protection is configured on develop (from Section 3)
- Your feature branch has commits following Conventional Commits format

**Step 1: Go to the GitHub repository**

Navigate to: https://github.com/jcg-admin/IACT-docs

**Step 2: Click "Compare & pull request"**

GitHub automatically detects your recently pushed feature branch and shows a banner:

.. code-block:: text

   feature/github-actions-validation had recent pushes
   [Compare & pull request] [Dismiss]

Click the green **"Compare & pull request"** button.

If the banner is gone, use the alternative:
1. Click **Pull requests** tab
2. Click **New pull request**
3. Select your feature branch in "compare" dropdown

**Step 3: Verify the merge direction**

Confirm the merge direction is correct:

.. code-block:: text

   base: develop  ← target branch (where you're merging INTO)
   compare: feature/your-feature-name  ← source branch (what you're merging FROM)

**DO NOT merge into main** — only merge feature branches to develop first.

**Step 4: Fill in the PR description**

Enter a clear title and description:

**Title:** Use Conventional Commits format (already introduced in Section 1):

.. code-block:: text

   feat(github-actions): implement build validation workflow

**Description:** Write a concise explanation of what the PR accomplishes:

.. code-block:: text

   ## What This PR Does

   Adds GitHub Actions workflow to validate Sphinx documentation
   build on every push to develop and main branches. Build failures
   are reported as PR status checks.

   ## Changes

   - Adds .github/workflows/sphinx-build.yml
   - Validates RST syntax before merge
   - Stores build logs as CI artifacts
   - Integrates with branch protection rules

   ## Testing

   Tested locally:
   - make html (successful)
   - Verified workflow syntax with `gh workflow validate`
   - Triggered workflow on test push (passed)

   Closes #42
   Related to RFC-documentation-quality-gates

The PR description should include:
- What problem does this solve?
- What changes were made?
- How was it tested?
- Any related issues (using keywords from Section 1.7)

**Step 5: Review and Create the PR**

1. Review the "Files changed" tab to verify you're committing what you intended
2. Check that "All checks have passed" (if CI is configured) or wait for checks to complete
3. Click **Create pull request**

GitHub will now:
- Trigger CI/CD checks (Sphinx build, tests, linting)
- Notify reviewers (if configured)
- Apply branch protection rules (PR approval required, status checks must pass)

3.2 Respond to Code Review
--------------------------------------------------------------------------------

After creating the PR, reviewers will examine your commits and leave feedback. Here's how to respond:

**Scenario: Reviewer requests changes**

Reviewer leaves a comment:

.. code-block:: text

   "The commit message should be more specific about what changed.
    Can you update it to mention the workflow file specifically?"

**How to respond:**

1. **Don't force-push or rebase** — Keep the original commits visible in PR history
2. **Make changes locally** on your feature branch
3. **Commit the changes** with a new Conventional Commits message:

   .. code-block:: bash

      # Edit the files based on reviewer feedback
      nano source/gestion/git-workflow.rst

      # Commit the changes
      git add source/gestion/git-workflow.rst
      git commit -m "fix(git-workflow): clarify branch protection configuration"

4. **Push the new commit** to your feature branch:

   .. code-block:: bash

      git push origin feature/your-feature-name

GitHub will automatically update the PR with your new commit. The reviewer can see:
- The original commits
- The new fix commit
- How you addressed their feedback

**Advantages of this approach:**

- Full history is preserved — you can see the conversation and evolution of changes
- Merge commit will show all commits, including the fix (Section 4.4 explains this)
- No rewriting history, no force-pushes needed
- Clear audit trail of review feedback and responses

**When review is approved:**

Once all reviewers approve and CI checks pass:
1. You see a green **"Merge pull request"** button
2. Proceed to Section 3.4 for merging

3.3 Handling Merge Conflicts
--------------------------------------------------------------------------------

**What causes conflicts?**

If someone merged changes to develop while you were working on your feature, your feature branch may be out of date. GitHub will show:

.. code-block:: text

   This branch has conflicts that must be resolved

**Option 1: Resolve conflicts locally (recommended)**

This keeps your history clean and avoids unnecessary merge commits.

**Step 1: Update your local develop branch**

.. code-block:: bash

   git fetch origin
   git checkout develop
   git pull origin develop

**Step 2: Merge develop into your feature branch**

.. code-block:: bash

   git checkout feature/your-feature-name
   git merge develop

Git will report conflicts:

.. code-block:: text

   CONFLICT (content): Merge conflict in source/gestion/git-workflow.rst
   Automatic merge failed; fix conflicts and then commit the result.

**Step 3: Resolve the conflicts**

Open the conflicted file and look for conflict markers:

.. code-block:: text

   <<<<<<< HEAD
   Your changes from your feature branch
   =======
   Changes from develop that conflict
   >>>>>>> develop

Edit the file to keep the correct version (or combine both if both are needed):

.. code-block:: text

   # Remove the markers and keep the correct content
   Final version that incorporates both changes

**Step 4: Commit the merge**

.. code-block:: bash

   git add source/gestion/git-workflow.rst
   git commit -m "merge: resolve conflicts with develop"

**Step 5: Push the updated feature branch**

.. code-block:: bash

   git push origin feature/your-feature-name

GitHub will automatically detect that conflicts are resolved and enable the **Merge** button.

**Option 2: Resolve conflicts on GitHub (simpler but less preferred)**

If you don't want to resolve locally, GitHub offers a UI resolver:
1. Go to the PR
2. Click **Resolve conflicts**
3. Edit the conflicted sections in the browser
4. Click **Mark as resolved**
5. Commit the merge

3.4 Merge to Develop with --no-ff
--------------------------------------------------------------------------------

Once all CI checks pass and reviewers approve, you can merge the PR to develop.

**Why --no-ff (no fast-forward)?**

A merge commit preserves the entire feature branch history as a unit, making it easy to:
- Revert the entire feature with one ``git revert`` command
- See which commits belonged to which feature
- Generate accurate release notes

GitHub's merge process uses ``--no-ff`` by default when you select "Create a merge commit".

**Step 1: Choose the merge strategy**

On the PR page, click the **Merge pull request** dropdown:

.. code-block:: text

   [Merge pull request ▼]
     • Create a merge commit (recommended)
     • Squash and merge
     • Rebase and merge

**IMPORTANT: Select "Create a merge commit"**

This uses the ``--no-ff`` flag, preserving all commits from the feature branch.

**DO NOT use "Squash and merge"** — This collapses all commits into one and loses history.

**Step 2: Confirm the merge commit message**

GitHub will show a default merge message:

.. code-block:: text

   Merge pull request #156 from feature/github-actions-validation

Edit to add more context if needed:

.. code-block:: text

   Merge pull request #156 from feature/github-actions-validation

   Implement automated Sphinx build validation for all PRs.

   This PR adds GitHub Actions workflows that run Sphinx build on
   every push to develop and main branches. Build failures are
   reported as PR status checks, preventing merge of documentation
   that won't compile.

   Closes #42
   Related to RFC-documentation-quality-gates

**Step 3: Click "Confirm merge"**

GitHub will merge the PR using:

.. code-block:: bash

   git merge --no-ff feature/your-feature-name \
     -m "Merge pull request #156..."

The feature branch remains as a complete unit in the develop history.

**Step 4: Optional — Delete the feature branch**

After merging, GitHub offers to delete the remote feature branch:

.. code-block:: text

   [Delete branch]

You can click this to clean up. Locally, delete it with:

.. code-block:: bash

   git branch -d feature/your-feature-name

3.5 Final Verification — Tracking and History
--------------------------------------------------------------------------------

After merge, verify the merge was successful and understand the tracking:

**Check branch tracking:**

.. code-block:: bash

   git branch -vv

Output shows your local branches and their remote tracking status:

.. code-block:: text

   feature/your-feature-name  7f2e4d9 [origin/feature/your-feature-name] commit message
   develop                    a1b2c3d [origin/develop: ahead 1] Merge pull request #156

The ``[origin/develop: ahead 1]`` means your local develop is 1 commit ahead of remote (or behind if it shows "behind 1").

**Update local develop to match remote:**

After the merge happened on GitHub, your local develop is outdated:

.. code-block:: bash

   git fetch origin
   git checkout develop
   git pull origin develop

Now your local develop has the merge commit.

**View the merge commit in history:**

.. code-block:: bash

   git log --oneline develop

Output:

.. code-block:: text

   a1b2c3d (HEAD -> develop, origin/develop) Merge pull request #156 from feature/github-actions-validation
   7f2e4d9 feat(github-actions): implement build validation workflow
   abc1234 docs(github-actions): add workflow configuration guide
   def5678 previous commit on develop

You can see:
- The merge commit (a1b2c3d) at the top
- All the feature branch commits preserved below it (7f2e4d9, abc1234)
- Original develop history (def5678)

**View just the feature branch commits:**

.. code-block:: bash

   git log --oneline --graph develop

This shows a visual tree of the merge, making it clear which commits belonged to the feature:

.. code-block:: text

   * a1b2c3d (HEAD -> develop, origin/develop) Merge pull request #156
   |\
   | * 7f2e4d9 feat(github-actions): implement build validation workflow
   | * abc1234 docs(github-actions): add workflow configuration guide
   |/
   * def5678 previous commit on develop

---

---

4. Develop → Main Release Workflow
================================================================================

This section describes how to prepare a release, create a release PR to main, tag the release, generate release notes, and handle rollbacks if needed.

4.1 Release Procedure — Pre-Release QA Checklist
--------------------------------------------------------------------------------

Before creating a release PR, complete this checklist to ensure quality:

**Step 1: Update documentation**

- [ ] Update CHANGELOG.md with release notes (features, fixes, breaking changes)
- [ ] Update version number in pyproject.toml or setup.py
- [ ] Update README.rst with any new features or changes
- [ ] Update CONTRIBUTING.md if process changed
- [ ] Verify all documentation links are correct

**Step 2: Run local build**

.. code-block:: bash

   # Clean previous builds
   make clean

   # Build documentation
   make html

   # Expected output: build/html/index.html exists, no errors

   # If using Python package, build package
   python -m build

**Step 3: Run tests**

.. code-block:: bash

   # Run all tests
   pytest

   # Run specific test suite if applicable
   pytest tests/test_sphinx_config.py

   # Expected: All tests pass

**Step 4: Verify code quality**

.. code-block:: bash

   # Check for lint issues
   flake8 source/

   # Type checking (if applicable)
   mypy source/

   # Expected: No errors or warnings

**Step 5: Create a test build artifact**

.. code-block:: bash

   # Build for distribution (if applicable)
   pip install build
   python -m build

   # Verify artifact exists and is valid
   ls -lh dist/

**Step 6: Tag verification (for pre-release check)**

.. code-block:: bash

   # Check existing tags
   git tag -l

   # Verify new tag version follows semver (v1.2.3)
   # and is higher than the latest tag

**Release Checklist Summary:**

Only proceed to release PR if:
- ✓ Documentation updated and reviewed
- ✓ Build succeeds (make html, make clean, no warnings)
- ✓ All tests pass
- ✓ Code quality checks pass (flake8, mypy, etc.)
- ✓ Test build artifacts are valid
- ✓ Version numbering follows Semantic Versioning 2.0.0

If any check fails, **DO NOT proceed** — fix issues before release.

4.2 Create Release PR — Develop to Main
--------------------------------------------------------------------------------

Once pre-release QA passes, create a PR to merge develop→main:

**Step 1: Ensure develop branch is up to date**

.. code-block:: bash

   git fetch origin
   git checkout develop
   git pull origin develop

**Step 2: Create a release branch**

Use a temporary branch for the release PR (optional but recommended):

.. code-block:: bash

   git checkout -b release/v1.2.3

**Step 3: Open the Release PR on GitHub**

1. Go to https://github.com/jcg-admin/IACT-docs
2. Click **Pull requests**
3. Click **New pull request**
4. Set base to ``main`` and compare to ``develop`` (or ``release/vX.Y.Z`` if using release branch)
5. Use this PR title:

   .. code-block:: text

      Release v1.2.3 — Merge develop to main

6. Use this PR description:

   .. code-block:: text

      ## Release: v1.2.3

      This PR merges develop to main for production release.

      ### Release Summary

      - [List key features added in this release]
      - [List critical fixes]
      - [Any breaking changes]

      ### Release Artifacts

      - Build: ✓ make html successful
      - Tests: ✓ all tests pass
      - Quality: ✓ no lint/type errors
      - Documentation: ✓ CHANGELOG.md updated

      ### Deployment

      After merge, proceed to section 5.3 for tagging and release.

7. Click **Create pull request**

**Step 4: Release PR Review**

The release PR requires **2 approvals** (enforced by branch protection) before merge:

- Release manager (you or designated owner)
- Code owner or project maintainer

Provide context in PR comments:
- Link to build artifacts
- Link to release notes (CHANGELOG.md)
- Any special deployment instructions

**Step 5: Merge the Release PR**

Once 2 approvals received and CI checks pass:

1. Click **Merge pull request**
2. Select **Create a merge commit** (--no-ff)
3. Update merge message:

   .. code-block:: text

      Merge pull request #156 from develop

      Release v1.2.3

      Key features:
      - [Feature 1]
      - [Feature 2]

      Fixes:
      - [Fix 1]
      - [Fix 2]

4. Click **Confirm merge**

4.3 Tagging Strategy — Annotated Tags
--------------------------------------------------------------------------------

After merge to main, create an annotated tag to mark the release:

**Why Annotated Tags?**

Annotated tags are recommended because they:
- Store metadata (tagger name, date, message)
- Can be signed with GPG for security
- Show up in release history
- Are distinct from lightweight tags

Lightweight tags are just pointers to commits and don't have metadata.

**Step 1: Fetch the latest main**

.. code-block:: bash

   git fetch origin
   git checkout main
   git pull origin main

The merge commit from section 5.2 is now on main.

**Step 2: Create an annotated tag**

.. code-block:: bash

   git tag -a v1.2.3 -m "Release v1.2.3

   Features:
   - Feature 1
   - Feature 2

   Fixes:
   - Fix 1
   - Fix 2

   Documentation: https://docs.example.com"

Replace v1.2.3 with the actual version number.

**Tagging Rules:**

- **Version format**: ``vMAJOR.MINOR.PATCH`` (e.g., v1.2.3, v2.0.0)
- **Follow Semantic Versioning 2.0.0**:
  - MAJOR: Breaking changes
  - MINOR: New features, backward compatible
  - PATCH: Bug fixes, backward compatible
- **Never use leading zeros**: v1.2.3 not v1.02.003
- **Annotated tags only**: Use ``git tag -a``, not ``git tag``

**Step 3: Verify the tag**

.. code-block:: bash

   git tag -l v1.2.3
   git show v1.2.3

Output should show:
- Tag name
- Tagger name and email
- Tag date
- Tag message (the release notes)
- Commit hash it points to

**Step 4: Push the tag to remote**

.. code-block:: bash

   git push origin v1.2.3

This makes the tag available on GitHub for release artifacts.

**Verify the tag on GitHub:**

1. Go to https://github.com/jcg-admin/IACT-docs/releases
2. You should see the new tag listed
3. You can create a GitHub Release from the tag if desired

4.4 Release Notes Generation
--------------------------------------------------------------------------------

Generate release notes automatically from commit history:

**Method 1: Using git log (recommended)**

.. code-block:: bash

   # Get all commits between last release and current
   git log v1.1.0..v1.2.3 --oneline --format="%h %s"

   # Output:
   # a1b2c3d feat(docs): add release workflow documentation
   # b2c3d4e fix(sphinx): correct configuration error
   # c3d4e5f docs(guides): update contribution guidelines

**Method 2: Git log with grouping**

.. code-block:: bash

   # Group by type (feat, fix, docs, etc.)
   git log v1.1.0..v1.2.3 --pretty=format:"%h %s" | \
     awk '{
       type = substr($0, index($0, "(") + 1);
       type = substr(type, 1, index(type, ")") - 1);
       if (type ~ /feat/) group="Features";
       else if (type ~ /fix/) group="Bug Fixes";
       else if (type ~ /docs/) group="Documentation";
       else group="Other";
       print group ": " $0
     }' | sort | uniq

**Method 3: Manual release notes**

For each commit type, list the relevant commits:

.. code-block:: markdown

   # Release Notes v1.2.3

   ## Features

   - docs(git-workflow): add release workflow documentation (#123)
   - feat(github-actions): implement build validation (#156)

   ## Bug Fixes

   - fix(sphinx): correct configuration error (#145)
   - fix(docs): update broken internal links (#167)

   ## Documentation

   - docs(guides): update contribution guidelines (#178)

   ## Other

   - chore(deps): upgrade sphinx to 5.0 (#189)

**Add release notes to the CHANGELOG.md:**

.. code-block:: markdown

   # Changelog

   ## [1.2.3] - 2026-04-27

   ### Added

   - Release workflow documentation with tagging strategy
   - GitHub Actions build validation workflow
   - Branch protection enforcement

   ### Fixed

   - Sphinx configuration error preventing builds
   - Broken internal documentation links

   ### Documentation

   - Updated contribution guidelines
   - Added release procedure checklist

4.5 Rollback Procedure
--------------------------------------------------------------------------------

If a release has a critical issue and must be reverted:

**Step 1: Identify the merge commit to revert**

.. code-block:: bash

   git log main --oneline | head -5

   # Output:
   # a1b2c3d (HEAD -> main) Merge pull request #156 from develop
   # b2c3d4e Some previous commit
   # c3d4e5f Another previous commit

The merge commit is a1b2c3d.

**Step 2: Revert the merge commit**

Use ``git revert -m 1`` to revert a merge without losing history:

.. code-block:: bash

   git revert -m 1 a1b2c3d

The ``-m 1`` flag tells git to keep the first parent (the main branch) and revert the changes from the second parent (the develop branch).

Git will create a new commit with the revert:

.. code-block:: bash

   git commit -m "revert(release): rollback v1.2.3 due to critical bug"

**Step 3: Push the revert commit**

.. code-block:: bash

   git push origin main

**Step 4: Create a rollback tag**

Create a new tag to mark the rollback point:

.. code-block:: bash

   git tag -a v1.2.3-rollback -m "Rollback from v1.2.3

   Reason: Critical bug in feature X
   Reverted to: [previous stable version]
   See: [link to issue]"

   git push origin v1.2.3-rollback

**Step 5: Notify stakeholders**

- Create a GitHub Release for the rollback tag
- Post to project channels (Slack, email, etc.)
- Document reason and next steps

**Rollback Example in Practice:**

.. code-block:: bash

   # Release goes out as v1.2.3
   git tag v1.2.3

   # Critical bug found, rollback needed
   git revert -m 1 a1b2c3d
   git push origin main

   # Tag the rollback point
   git tag -a v1.2.3-rollback -m "Rollback from v1.2.3 due to critical bug in X"
   git push origin v1.2.3-rollback

   # History preserved:
   # a1b2c3d (tag: v1.2.3) Merge pull request #156 from develop
   # e1f2g3h (tag: v1.2.3-rollback) revert(release): rollback v1.2.3
   # Previous stable version

**Why This Approach?**

- History is preserved (no force-push or hard reset)
- You can track why a release was rolled back
- The original merge commit remains in history for audit
- Future releases can reference the rollback decision
- No loss of data or commit history

5. GitHub Branch Protection
================================================================================

Branch protection rules enforce quality gates on the ``develop`` and ``main`` branches, preventing accidental or unauthorized changes. This section documents how to configure these rules.

5.1 Branch Protection Overview
--------------------------------------------------------------------------------

**Why Branch Protection?**

Branch protection rules prevent:

- Direct pushes to critical branches (all changes must go through pull requests)
- Merging code that doesn't pass CI checks
- Merging without required code review approvals
- Deleting protected branches accidentally
- Force-pushing to rewrite history

**Protected Branches in IACT-docs:**

- **develop** — Moderate protection: PR review required, CI must pass
- **main** — Strict protection: 2 PR approvals required, admin-only push, CI must pass

5.2 GitHub UI Setup — Step-by-Step
--------------------------------------------------------------------------------

**Access Branch Protection Settings:**

1. Go to your repository on GitHub: https://github.com/jcg-admin/IACT-docs
2. Click **Settings** (top right, gear icon)
3. In the left sidebar, click **Branches**
4. Under "Branch protection rules", click **Add rule**

**Configuring Protection for 'develop' Branch:**

Enter the branch name pattern:

.. code-block:: text

   develop

Then configure these settings:

1. **Require a pull request before merging** — ✓ Check this box
   - ``Require approvals`` — Check this box
   - ``Required number of approvals before merging`` — Set to **1** (minimum review)
   - ``Require approval from code owners`` — Optional (check if you have CODEOWNERS file)

2. **Require status checks to pass before merging** — ✓ Check this box
   - ``Require branches to be up to date before merging`` — ✓ Check this box
   - ``Search for status checks that run in this repository...`` — Select:
     - ``build`` (Sphinx build validation)
     - ``tests`` (any test suites)
   - Add any other CI workflows relevant to your project

3. **Require code review before merging** — Covered in step 1 above

4. **Require conversation resolution before merging** — ✓ Check this box
   (Ensures all review comments are addressed)

5. **Require commits to be signed** — Optional
   (Only if you enforce GPG signing for compliance)

6. **Restrict who can push to matching branches** — ✓ Check this box
   - ``Restrict who can push to matching branches`` — Add your team or leave for all maintainers

7. **Allow force pushes** — ✓ **Do NOT check** (prevent rewriting history)

8. **Allow deletions** — ✓ **Do NOT check** (prevent accidental branch deletion)

9. **Require linear history** — Optional but recommended
   (Ensures commits can't have multiple parents)

**Click "Create" to save the rule for develop**

**Configuring Protection for 'main' Branch (Stricter):**

Repeat the process but enter:

.. code-block:: text

   main

Configure with **stricter** settings:

1. **Require a pull request before merging** — ✓ Check this box
   - ``Require approvals`` — Check this box
   - ``Required number of approvals before merging`` — Set to **2** (higher bar for main)
   - ``Require approval from code owners`` — ✓ Check this box (if available)
   - ``Dismiss stale pull request approvals when new commits are pushed`` — ✓ Check this box
   - ``Require review from Code Owners`` — ✓ Check this box (if CODEOWNERS exists)

2. **Require status checks to pass before merging** — ✓ Check this box
   - ``Require branches to be up to date before merging`` — ✓ Check this box
   - Select the same status checks as develop (build, tests, etc.)

3. **Require conversation resolution before merging** — ✓ Check this box

4. **Restrict who can push to matching branches** — ✓ Check this box
   - Add **only administrators** (repository owners)

5. **Allow force pushes** — ✓ **Do NOT check**

6. **Allow deletions** — ✓ **Do NOT check**

7. **Require linear history** — ✓ Check this box

8. **Require branches to be up to date before merging** — ✓ Check this box

**Click "Create" to save the rule for main**

**Summary Table — develop vs main:**

+-------------------------------------------+-----------+---------+
| Rule                                      | develop   | main    |
+===========================================+===========+=========+
| Require PR before merge                   | ✓         | ✓       |
+-------------------------------------------+-----------+---------+
| Required approvals                        | 1         | 2       |
+-------------------------------------------+-----------+---------+
| Require code owner approval               | Optional  | ✓       |
+-------------------------------------------+-----------+---------+
| Require status checks (CI)                | ✓         | ✓       |
+-------------------------------------------+-----------+---------+
| Require linear history                    | Optional  | ✓       |
+-------------------------------------------+-----------+---------+
| Restrict push to admins only              | No        | ✓       |
+-------------------------------------------+-----------+---------+
| Allow force push                          | ✗         | ✗       |
+-------------------------------------------+-----------+---------+
| Allow deletion                            | ✗         | ✗       |
+-------------------------------------------+-----------+---------+

5.3 API Configuration — GitHub REST API
--------------------------------------------------------------------------------

If you prefer to configure branch protection programmatically (e.g., in infrastructure-as-code), use the GitHub API:

**Endpoint:** ``PUT /repos/{owner}/{repo}/branches/{branch}/protection``

**Example: Protect 'develop' branch with curl**

.. code-block:: bash

   curl -X PUT \
     -H "Authorization: token YOUR_GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/repos/jcg-admin/IACT-docs/branches/develop/protection \
     -d '{
       "required_status_checks": {
         "strict": true,
         "contexts": ["build", "tests"]
       },
       "enforce_admins": false,
       "required_pull_request_reviews": {
         "dismiss_stale_reviews": false,
         "require_code_owner_reviews": false,
         "required_approving_review_count": 1
       },
       "restrictions": null,
       "allow_force_pushes": false,
       "allow_deletions": false,
       "require_linear_history": false,
       "required_conversation_resolution": true
     }'

**Example: Protect 'main' branch with curl (stricter)**

.. code-block:: bash

   curl -X PUT \
     -H "Authorization: token YOUR_GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/repos/jcg-admin/IACT-docs/branches/main/protection \
     -d '{
       "required_status_checks": {
         "strict": true,
         "contexts": ["build", "tests"]
       },
       "enforce_admins": true,
       "required_pull_request_reviews": {
         "dismiss_stale_reviews": true,
         "require_code_owner_reviews": true,
         "required_approving_review_count": 2
       },
       "restrictions": null,
       "allow_force_pushes": false,
       "allow_deletions": false,
       "require_linear_history": true,
       "required_conversation_resolution": true
     }'

**Key API fields:**

- ``strict`` — Require branch to be up-to-date before merge
- ``enforce_admins`` — Restrict push to admins only
- ``require_code_owner_reviews`` — Code owners must approve
- ``required_approving_review_count`` — Number of approvals needed
- ``allow_force_pushes`` — Allow rewriting history (should be false)
- ``allow_deletions`` — Allow branch deletion (should be false)
- ``require_linear_history`` — Prevent merge commits that create multiple parents

**Getting a GitHub Token:**

1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Give it a descriptive name: "Branch Protection API"
4. Select scopes: ``repo`` (full control of private repositories)
5. Click "Generate token" and **save it securely**
6. Use the token in the curl command: ``Authorization: token YOUR_TOKEN``

5.4 Verification — Confirm Protection is Active
--------------------------------------------------------------------------------

**Via GitHub UI:**

1. Go to Settings > Branches
2. Verify both ``develop`` and ``main`` appear in "Branch protection rules"
3. Click each rule to review settings

**Via GitHub CLI:**

If you have the GitHub CLI installed (``gh``):

.. code-block:: bash

   # List all branch protection rules
   gh api repos/jcg-admin/IACT-docs/branches/develop/protection

   # Should return JSON with protection configuration
   {
     "url": "https://api.github.com/repos/jcg-admin/IACT-docs/branches/develop/protection",
     "required_status_checks": {
       "url": "...",
       "strict": true,
       "contexts": ["build", "tests"]
     },
     "required_pull_request_reviews": {
       "url": "...",
       "required_approving_review_count": 1
     }
   }

**Testing Branch Protection:**

1. Try to push directly to ``develop`` or ``main``:

   .. code-block:: bash

      git push origin feature/test-protection:develop

   Expected result: **REJECTED** with message:

   .. code-block:: text

      remote: error: The develop branch is protected from force pushes
      ! [remote rejected] feature/test-protection -> develop (protected branch hook declined)

2. Try to create a PR without approval:

   Create a PR and try to merge without waiting for approval. Expected: **Merge button is disabled** with message:

   .. code-block:: text

      "Merging blocked — 1 approval required"

3. Create a valid PR, get approval, and merge:

   Expected: **Merge succeeds** and branch protection rules are satisfied.

