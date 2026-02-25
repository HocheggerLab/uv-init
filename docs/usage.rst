Usage
=====

Basic command
-------------

.. code-block:: bash

   uv-init <project-name> [options]

The project name must not contain spaces or underscores.

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``-t, --type [lib|package]``
     - Project type to create. **lib** (default) creates a simple library
       with a ``src/`` layout. **package** creates an installable package
       with an entry-point script.
   * - ``-p, --python [3.13|3.12|3.11|3.10]``
     - Python version for the new project (default: **3.13**).
   * - ``-w, --workspace``
     - Create a `uv workspace <https://docs.astral.sh/uv/concepts/projects/workspaces/>`_
       (monorepo). You will be prompted to add a shared utilities library
       and additional sub-projects.
   * - ``-g, --github``
     - Initialise a Git repository **and** create a GitHub remote.
       Sets up CI/CD workflows automatically.
   * - ``--private``
     - Make the GitHub repository private. Requires ``--github``.

Examples
--------

Create a library (default)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   uv-init my-lib

Creates a ``my-lib/`` directory with a ``src/my_lib/`` package, test
directory, and all dev-tool configuration.

Create an installable package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   uv-init my-cli -t package

Same as a library but also registers a console script entry-point so the
package can be run from the command line.

Specify a Python version
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   uv-init my-project -p 3.12

Target Python 3.12 instead of the default 3.13.

Create a project with a GitHub repo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   uv-init my-project -g

Initialises a local Git repo, creates a **public** GitHub remote, pushes
an initial commit, and sets up CI workflows.

.. code-block:: bash

   uv-init my-project -g --private

Same as above but the GitHub repository is **private**.

Create a workspace (monorepo)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   uv-init my-workspace -w

Sets up a uv workspace. You will be interactively prompted to:

1. Add a ``common-utils`` shared library
2. Add additional sub-projects to the workspace

Combine workspace and GitHub:

.. code-block:: bash

   uv-init my-workspace -w -g

Generated project structure
---------------------------

Standard project
^^^^^^^^^^^^^^^^

.. code-block:: text

   project-name/
   ├── src/
   │   └── project_name/
   │       └── __init__.py
   ├── tests/
   ├── pyproject.toml
   ├── README.md
   ├── LICENSE
   └── .pre-commit-config.yaml

Workspace
^^^^^^^^^

.. code-block:: text

   workspace-name/
   ├── packages/
   │   ├── package1/
   │   └── package2/
   ├── pyproject.toml
   ├── README.md
   └── .pre-commit-config.yaml

Development tools configured
-----------------------------

Every generated project comes with:

- **Ruff** — linter and formatter (line length 79, flake8 + isort rules)
- **Ty** — static type checker (checks ``src/`` and ``tests/``)
- **pytest** — test framework with automatic discovery in ``tests/``
- **commitizen** — conventional commits, automatic version bumping, and
  changelog generation
- **pre-commit** — Git hooks that run linting, formatting, and type
  checking before each commit

GitHub CI/CD workflows
----------------------

When ``--github`` is used, two GitHub Actions workflows are created:

**CI pipeline** — runs on every push and pull request:

- Ruff linting and format checking
- Ty type checking
- pytest test suite

**Release pipeline** — runs on pushes to ``main``:

- Automatic version bumping based on conventional commits
- GitHub release creation with changelog
