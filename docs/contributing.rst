Contributing
============

This project is intended to be a small but high-quality helper around the
``uv init`` command.

Development workflow
--------------------

* Create a feature branch from ``main`` (e.g. ``dave-refactor``).
* Use ``uv`` to manage the virtual environment and dependencies.
* Run the test suite and type checker before opening a PR.

Useful commands
---------------

.. code-block:: bash

   # Create / update the virtual environment
   uv sync

   # Run the tests
   uv run pytest

   # Run the type checker (ty)
   uv run ty .

   # Build the documentation
   uv run sphinx-build -b html docs docs/_build/html

Code style
----------

* Type hints are required for public functions and methods.
* Ruff is used for linting and formatting; keep imports sorted and code clean.
* Prefer clarity over cleverness, especially in templates users will copy.

