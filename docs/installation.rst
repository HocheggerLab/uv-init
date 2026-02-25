Installation
============

Prerequisites
-------------

- **Python 3.13+** (not tested on earlier versions)
- **uv** — the fast Python package manager
  (`install uv <https://docs.astral.sh/uv/getting-started/installation/>`_)
- **gh** — the GitHub CLI, only needed if you use the ``--github`` flag
  (`install gh <https://cli.github.com/>`_)

Clone and install
-----------------

.. code-block:: bash

   git clone https://github.com/Helfrid/uv-init.git
   cd uv-init
   uv sync

Author configuration
--------------------

Configure your author details so they are injected into every project
you generate. Run this once after installing:

.. code-block:: bash

   uv-init --config "Jane Doe" "jane@example.com"

This saves your name and email to ``~/.config/uv-init/config.toml``.

If you skip this step, uv-init falls back to your ``git config``
(``user.name`` / ``user.email``). If neither is set, placeholder
values are used.

GitHub authentication
---------------------

If you plan to use the ``--github`` flag, authenticate the ``gh`` CLI first:

.. code-block:: bash

   gh auth login

No token needs to be stored in ``.env``. If ``GH_TOKEN`` or
``GITHUB_TOKEN`` is already set in your shell, ``gh`` will pick it up
automatically.

Shell alias (recommended)
-------------------------

Because uv-init is not published on PyPI, you need to tell ``uv run``
where the project lives. A shell alias hides this detail:

.. code-block:: bash

   # Add to ~/.zshrc or ~/.bashrc
   uv_init() {
     UV_ORIGINAL_CWD="$PWD" uv run --directory /path/to/uv-init uv-init "$@"
   }
   alias uv-init='uv_init'

After restarting your shell you can run ``uv-init`` from any directory:

.. code-block:: bash

   cd ~/projects
   uv-init my-new-project -t package -g
