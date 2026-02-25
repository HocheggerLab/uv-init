## uv
When uv first came out it was designed as a new tool to pull Python packages, working very much like pip, but much faster. The speed comes from its Rust core, extensive optimisation, and lots of caching. From the start, the idea was to extend uv into a fully fledged Python project management system, much like poetry but equipped with a hyperdrive. So in parallel to the classic `uv pip install` type of commands that shadow the pip way of doing things, the `uv init, uv add, uv sync'` api was soon released that offered a more complete eco-system for working with python projects.
Both types of commands are still in use and also somewhat interchangeable but I decided to build my project around the `uv init [option]` api which is the starting point of setting up a project. There are quite a few choices available to specific the type of project you want using optional command: ` —lib, —package, —app` and also the option to build a workspace with several packages integrated in a mono-repo.
uv init is modelled after cargo new, setting up a ready to go development environment, with a pyproject.toml file, git initiated and a src with a module folder.

A few points here:

- the default uv init generates the --app option. I find this somewhat impractical since it doesn’t generate a complete distributable project structure but a minimal rump.
- Having said this, uv makes it easy to use scripts with dependencies, this could lead to a revival of small utiliuty scripts in python. See [here][1] for a comprehensive guide.
- --package (or --package --app) generate a more comprehensive project structure with a script entry point and a hatchling build system.
- --lib generates a similar structure but doesn't have the script entry point in pyproject.toml; so its the starting point for a pure library project.
- A really important feature is the way uv handles the python distribution. You can choose your Python version using —python 3.13, etc, if you have downloaded this from python.org and it’s installed in your system, uv will by default use this version. Otherwise it will pull python from https://github.com/astral-sh/python-build-standalone. In fact astral has recently taken over stewardship of this project. I personally prefer using vanilla python that I install from python.org and keep up to date using the wonderful [MOPUp][2] project.
- the initial uv init command does not setup a .venv yet. The virtual environment is only created once you add a dependency with uv add or you call uv sync which will also create a uv.lock file that ensures consistent package versions
- If you are in a uv project directory and you call uv init again, you create a workspace. This is actually what I want for my main application: a mono-repo structure with several subprojects, each with its own pyproject.toml file. More about workspaces later...




Some more resources for details on uv:
[Charlie Marsh's recent talk about uv][3]
[A detaile iv blog on Saas Pegasus][4]
[talk python to me podcast with Charlie Marsh][5]

—

## Understanding uv

When uv first appeared, it was designed as a replacement for pip—faster, built in Rust, heavily optimized. But that was just the beginning. The real power came with the expanded toolset: `uv init`, `uv add`, `uv sync`. Suddenly, you had a full project management system that felt less like pip-with-a-speedboost and more like cargo reimagined for Python.

Here's what matters: uv handles everything you need to create, manage, and run a Python project. You don't have to think about multiple tools or worry about incompatibilities. It's all in one place.

### Choosing Your Project Type

The first decision you'll make with uv is what kind of project you're building. When you run `uv init`, you'll specify a type using `--lib`, `--package`, or `--app`. Here's the practical difference:

**`--lib`** is for pure library code—something you'll use as a dependency in other projects. No executable, just reusable functions and classes. If you're writing image analysis utilities that others (or future you) will import, this is your choice.

**`--package --app`** is for distributable applications. You get a proper project structure with a script entry point and a build system. This is what you want if your code needs to be run by end users, not just imported by developers. It's the middle ground between pure library and standalone script.

**`--app`** alone creates a minimal application structure. Honestly, I find this somewhat impractical for actual projects—it doesn't give you enough structure to scale. But it's useful if you're building simple utility scripts with dependencies. uv makes that pattern surprisingly convenient.

For my uv-init tool, I use `--package --app` because it needs to be installed and run as a command-line tool. But for a pure analysis library, I'd go with `--lib`.

### Python Versions and Virtual Environments

Here's something uv gets right: Python version management. When you run `uv init`, you can specify which Python version you want:
```bash
uv init my-project --python 3.13
```

If you've installed Python 3.13 from python.org (like we did earlier), uv will use that. If you don't have it, uv will automatically pull Python from the official build-standalone distribution maintained by Astral. This is nice because you don't have to worry about where Python comes from—uv just handles it.

One thing to know: `uv init` doesn't create a virtual environment yet. That happens the first time you add a dependency with `uv add` or run `uv sync`. At that point, uv creates a `.venv` directory and generates a `uv.lock` file. That lock file is important—it pins exact versions of every dependency, so anyone else running your project gets the exact same environment. Reproducibility. That's the whole point.

### What About Workspaces?

If you're building a larger application with multiple interconnected packages, uv supports workspaces—basically a monorepo structure. If you're in a uv project directory and run `uv init` again, you create a workspace. Each subproject gets its own `pyproject.toml` file, but they all share a single `uv.lock` file at the root.

I use workspaces for my main image analysis project, and I'll show you how that works when we build out the full uv-init workflow at the end of this series. For now, just know it exists and that uv handles it smoothly.

### Resources

If you want to dive deeper into uv, these are solid:

- [Charlie Marsh's talk on uv][6]
- [A detailed deep dive from SaaS Pegasus][7]
- [Talk Python to Me podcast episode with Charlie Marsh][8]

---

## Setting Up Your First Project

Now that you understand what uv does and what project type to choose, let's actually create something...

[1]:	https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/?featured_on=pythonbytes
[2]:	https://pypi.org/project/MOPUp/
[3]:	https://www.youtube.com/watch?v=gSKTfG1GXYQ%5C
[4]:	https://www.saaspegasus.com/guides/uv-deep-dive/
[5]:	https://talkpython.fm/episodes/show/476/unified-python-packaging-with-uv
[6]:	https://www.youtube.com/watch?v=gSKTfG1GXYQ
[7]:	https://www.saaspegasus.com/guides/uv-deep-dive/
[8]:	https://talkpython.fm/episodes/show/476/unified-python-packaging-with-uv
