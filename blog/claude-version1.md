# From Jupyter Notebooks to Professional Python: A Scientist's Guide to Modern Project Setup

I'm not a software developer — I'm a scientist who writes code for image analysis and bioinformatics. I taught myself Python during lockdown, starting the way most scientists do: Jupyter notebooks, one cell at a time. That approach works fine for exploratory analysis, but once I tried to reuse code across projects and collaborate with others, things started to fall apart quickly. I realised I needed .py files, modules, proper structure, and something resembling actual software development practices.

So just when I started being comfortable with Python I realised that there is yet another steep learning hill to climb. Moving from "how do I write a for-loop?" to "how do I set up a professional Python project?" felt like relocating to a foreign country. Suddenly I needed to understand virtual environments, package managers, git workflows, type hints, code formatting, testing, logging, pre-commit hooks, continuous integration — the list kept growing. Each tool solved a real problem, but figuring out which ones to use and how they fit together was overwhelming.

For years, I fumbled with conda and various setups, never quite satisfied. Then I started learning Rust out of curiosity, and discovered cargo — its native package manager. The elegance of that workflow was revelatory. Around the same time, [uv](https://docs.astral.sh/uv/) appeared on the horizon, a new Python package manager that borrowed cargo's philosophy. Suddenly, things clicked into place.

By then, my projects had grown substantially and I was collaborating with others. Yet, I kept wrestling with the same setup problems on every new project. Rather than use an existing cookiecutter tool, I decided to build one tailored to my needs. This served two purposes: I'd learn modern Python development practices by actually using them, and I'd create something genuinely useful for my own work.

This post documents what I learned. I'm not trying to compete with professional tools or become a Python packaging expert — far from it. If you're a researcher struggling with Python tooling, a data scientist moving toward maintainable code, or someone who keeps Googling "how to set up a Python project properly" every time you start something new — hopefully you'll find something useful here.

---

## What uv-init Does

[uv-init](https://github.com/TODO-your-repo-here) is a small CLI tool that wraps around `uv` to create Python projects that are ready to go from the first commit. You run one command and get a complete project with development tools configured, testing set up, and optionally a GitHub repository with CI.

```
uv-init my-project -t lib -p 3.13 -g
```

That's it. Here's what you get:

```
my-project/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Tests on every push
│       └── release.yml         # Version bumps on merge to main
├── .vscode/
│   ├── launch.json             # Debug configuration
│   └── settings.json           # Editor settings
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── config.py           # Logging and env variable setup
│       └── py.typed
├── tests/
│   └── test_init.py
├── .env                        # Logging configuration
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── LICENSE
├── README.md
├── pyproject.toml              # All tool configs in one place
└── uv.lock
```

The `pyproject.toml` comes pre-loaded with configurations for all the development tools. Let me walk through what's in there and why.

---

## The Toolchain: What and Why

When I started down this path, I spent ages figuring out which tools to use and how to configure them. There are plenty of tutorials on each tool individually, but surprisingly little on how they all fit together into a coherent workflow. Here's the stack I settled on and why.

### uv — Package Management

When starting a Python project, the first thing to decide is how to set up your environment and which package manager to use. Everyone agrees there are currently too many options. Charlie Marsh's [Astral](https://astral.sh/) is on a mission to clear this up with uv — a unified system inspired by the way Rust manages projects with cargo.

Coming from data science, I was used to conda and mamba, which are great for analysis but not really cut out for proper software development. uv changed that. It handles Python versions, virtual environments, dependency resolution, and project scaffolding — all in one tool, and it's fast because it's written in Rust.

The key commands you need to know:
- `uv init project-name --lib` or `--package` — creates the project structure
- `uv add package-name` — adds a dependency (and creates the `.venv` if it doesn't exist yet)
- `uv sync` — installs everything and generates a lock file for reproducibility
- `uv run` — runs commands within the project's virtual environment

If you're in a uv project directory and run `uv init` again, you create a workspace — a monorepo structure with multiple packages sharing a single lock file. I use this for my main image analysis project where I have several interconnected packages.

One thing I really appreciate: you can specify your Python version with `--python 3.13` and uv will either use your system installation or pull one automatically. No more pyenv confusion.

**Resources:** [Charlie Marsh's talk on uv](https://www.youtube.com/watch?v=gSKTfG1GXYQ) | [SaaS Pegasus deep dive](https://www.saaspegasus.com/guides/uv-deep-dive/) | [Talk Python episode](https://talkpython.fm/episodes/show/476/unified-python-packaging-with-uv)

### Ruff — Formatting and Linting

[Ruff](https://astral.sh/ruff) takes care of formatting your code, detecting syntax errors, and enforcing style rules. Like uv, it's written in Rust and maintained by Astral. It replaces what used to be a handful of separate tools — black, isort, flake8, and several flake8 plugins — with a single, fast command.

I use a fairly comprehensive set of linting rules covering pyupgrade, bugbear, comprehension checks, and more. The [full configuration is in the repo](https://github.com/TODO-your-repo-here) if you want to see the details, but the point is: uv-init sets all of this up for you so you don't have to think about it.

### Type Checking

Static typing in Python is not something you do much when writing scripts and notebooks. But it becomes really useful when you're developing a larger codebase. It eliminates entire categories of bugs, reduces the need for lengthy docstrings, and makes code more readable and maintainable.

I started with [mypy](https://mypy-lang.org/) in strict mode and have recently been experimenting with [ty](https://github.com/astral-sh/ty), Astral's new type checker (also written in Rust, sensing a pattern here). uv-init sets up whichever you prefer with sensible defaults.

### pytest — Testing

OK, this is a subject that could fill quite a few pages. When you start working with data and Python in science, testing is the last thing you think about. But when you develop code for other people to use, slowly but surely it becomes probably the most important topic to consider during development. My aim is to have a codebase that will outlast me, or at least that I can come back to regularly and have confidence that a small change won't break the entire thing.

I use the [pytest](https://docs.pytest.org/) framework with a straightforward configuration. uv-init creates a `tests/` directory with a starter test file and configures pytest in `pyproject.toml`. When you enable GitHub integration, CI runs your tests automatically on every push. Nothing revolutionary, but it's the kind of thing that's easy to skip when you're setting up by hand and then never get around to adding later.

I find myself more and more in the test-driven development camp, where designing the tests precedes or at least happens in parallel to developing functions. Having the infrastructure ready from day one makes that much easier.

### Commitizen — Versioning That Makes Sense

[Commitizen](https://commitizen-tools.github.io/commitizen/) standardises commit messages and handles automated versioning. I always used to get into a mess with version numbers and my commit messages were usually a waste of time. This tool made me rethink my strategy.

The idea is simple: you use `cz commit` instead of `git commit`, and it guides you through writing a structured message. Different commit types trigger different version increments — a `fix` bumps the patch version, a `feat` bumps the minor version. When you're ready to release, `cz bump` updates the version everywhere it needs to be: `__init__.py`, `pyproject.toml`, `README.md`.

I deliberately don't enforce version bumping in pre-commit hooks. My preferred approach is to handle this in CI — versions only bump after all tests have passed. This way version numbers only increase when code is fully validated.

### Pre-commit — The Safety Net

[Pre-commit](https://pre-commit.com/) ties everything together. Before each commit, it automatically runs ruff for formatting and linting, checks your types, and catches common mistakes like accidentally committing large files or leaving merge conflict markers in your code.

The beauty of this is that you set it up once and then forget about it. Your code gets checked every time you commit, and problems get caught before they make it into the repository. uv-init installs a `.pre-commit-config.yaml` with all of these hooks configured and ready to go.

### GitHub Actions — CI That Just Works

When you use the `-g` flag, uv-init creates a GitHub repository and sets up two workflows:

- **CI** (`ci.yml`): Runs on every push. Installs dependencies, runs ruff, runs the type checker, runs pytest. If any of these fail, you know immediately.
- **Release** (`release.yml`): Runs when you merge to main. Handles version bumping with commitizen based on your commit messages.

This is the complete loop: you write code, pre-commit checks it locally, you push, CI checks it again, and when you merge, versioning happens automatically.

---

## Things I Wish Someone Had Told Me

Building this tool taught me as much as using it. Here are a few hard-won lessons.

**Keep conda around but switch it off.** If you have legacy conda projects, you don't have to nuke everything. Just add `conda autoactivate = false` to your `.condarc` file. Conda will be there when you need it but won't interfere with everything else.

**Separate your logging from your user interface.** When I started writing code I mainly used print statements to the console. This quickly ends in a mess with debug information and actual user feedback all littered across the screen. The solution I landed on uses environment variables to control logging behaviour — different `.env` files for development and production, with switches for console vs. file logging, log levels, and formatting. uv-init ships a `config.py` that sets this up using [python-dotenv](https://pypi.org/project/python-dotenv/). It's the kind of infrastructure that's boring to set up but transforms your debugging experience once it's there.

**Use vanilla Python.** I download Python directly from [python.org](https://python.org) and add it to my PATH. No conda, no pyenv, no homebrew. uv handles the rest. There's a nice little tool called [MOPUp](https://mopup.readthedocs.io/) that keeps your installations up to date. Simple, predictable, and one less thing to debug when something goes wrong.

**Don't skip type hints.** I know, I know — it feels like extra work when you're writing a quick analysis script. But once your codebase grows beyond a few files, type hints become the documentation that actually stays up to date. Start strict from day one; it's much harder to retrofit later.

**Workspaces are worth the learning curve.** If you're building something that naturally splits into multiple packages — say, a core library and a CLI that uses it — uv workspaces handle this elegantly. Each package gets its own `pyproject.toml` but they share a single lock file. I use this for my main image analysis project and it keeps things much more organised than the alternative of juggling multiple repositories.

---

## Try It

If any of this sounds useful, grab the repo and try it:

```bash
uvx uv-init my-project -t lib -p 3.13 -g
```

The [source code is on GitHub](https://github.com/TODO-your-repo-here). It's not a polished product — it's a learning project that happens to be useful. Feel free to fork it, adapt it, or just browse the template files to see how the different tools are configured.

My main sources for a lot of the topics covered here were the [Talk Python](https://talkpython.fm/) and [Real Python](https://realpython.com/) podcasts and courses. These led me to other people's blogs and resources, so in the end I learned a lot from other people's efforts to teach and share knowledge. In return, perhaps a few people will find something helpful here.

If you're a researcher who's been meaning to level up your Python workflow, or you just want to stop spending the first hour of every new project configuring the same tools — give it a go. And if you have suggestions for how to improve it, I'd genuinely love to hear them.
