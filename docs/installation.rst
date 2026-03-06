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

   git clone https://github.com/Helfrid/uv-start.git
   cd uv-start
   uv sync

Author configuration
--------------------

Configure your author details so they are injected into every project
you generate. Run this once after installing:

.. code-block:: bash

   uv-start --config "Jane Doe" "jane@example.com"

This saves your name and email to ``~/.config/uv-start/config.toml``.

If you skip this step, uv-start falls back to your ``git config``
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

Because uv-start is not published on PyPI, you need to tell ``uv run``
where the project lives. A shell alias hides this detail:

.. code-block:: bash

   # Add to ~/.zshrc or ~/.bashrc
   uv_start() {
     UV_ORIGINAL_CWD="$PWD" uv run --directory /path/to/uv-start uv-start "$@"
   }
   alias uv-start='uv_start'

After restarting your shell you can run ``uv-start`` from any directory:

.. code-block:: bash

   cd ~/projects
   uv-start my-new-project -t package -g
