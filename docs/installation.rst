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

If you plan to use the ``--github`` flag, authenticate the ``gh`` CLI
first using OAuth:

.. code-block:: bash

   gh auth login

Follow the interactive prompts to authenticate via your browser. This
stores credentials securely in the ``gh`` keychain — no tokens need to
be stored in any file.

.. note::

   If ``GH_TOKEN`` or ``GITHUB_TOKEN`` is already exported in your shell,
   ``gh`` will use it automatically. However, OAuth via ``gh auth login``
   is the recommended approach.

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
