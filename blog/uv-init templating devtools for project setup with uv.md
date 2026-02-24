I'm not a software developer, I am a scientist who develops tools for image analysis and bioinformatics. This means that I am used to Jupyter notebooks and writing scripts in Python. Recently I have been working on a larger research application that is now running more or less non stop in my lab. This means transitioning into a very different style of working with code. Especially since I am starting to work on this with a small team of developers. I have to admit this transition doesn't come easy. Its like moving to a different country! Code style, typing, versioning, logging, pre-commit hooks, continuous integration that's a hell of a lot of new concepts to become familiar with.
I like learning by doing so I decided to build a small application that automates the project set up. This let me catch two birds with one stone: I familiarise myself with some fundamental tools that support modern python software development, and I generated a little package that helps me quickly get started with new projects. So what's not to like...

This blog is my documentation of this process. I will summarise the different steps of building the project and refer to more detailed documentation as I go along. Going into depth for each of the tools is beyond the scope of this text. What I hope to achieve here is to give a practical overview of setting up a modern python project that is ready to go with state of the art tools for productive software development.
# TODO Discuss the professional cookie cutter projectsa
## Python distribution and packaging

### UV

When starting a software development project in python, the first thing to decide is how to set up a python environment and which package manager to use. Everyone agrees that there are currently too many options to do this. Charlie Marsh‘s Astral is on a mission to clear this up and to build a unified system called uv that is inspired by the way Rust is managed by cargo. I have been experimenting with Rust in the last year and I have to say it does feel a lot easier and more organised. Coming from data science, I am used to conda and mamba which is great for data analysis projects for example. But its not really cut out to support proper software development. So I decided to experiment with uv and use this as the basis for my project setup pipeline. I still have conda via the miniforge distribution on my machine but have it switched off by default. The trick here is to have the following line in the condarc file.

```bash
conda autoactivate = false
```

Astral‘s uv has recently stepped up from an incredibly fast pip alternative to a full fledged packaging manager. This is handled via:

```bash
uv init project-name [options]
```


which is the starting point of setting up a project. There are quite a few choices, —lib, —package, —app and also the option to build a workspace with several packages integrated in a mono-repo.
uv init is modelled after cargo new, setting up a ready to go development environment, with a pyproject.toml file, git initiated and a src with a module folder.

A few points here:

- the default uv init generates the --app option. I find this somewhat impractical since it doesn't generate a complete distributable project structure but a minimal rump.
- Having said this, uv makes it easy to use scripts with dependencies, this could lead to a revival of small utiliuty scripts in python. See [here][1] for a comprehensive guide.
- --package (or --package --app) generate a more comprehensive project structure with a script entry point and a hatchling build system.
- --lib generates a similar structure but doesn't have the script entry point in pyproject.toml; so its the starting point for a pure library project.
- A really important feature is the way uv handles the python distribution. you can choose your python version using --python 3.13 etc.. if you have downloaded this from python.org and its installed in your system, uv will by default use this version. Otherwise it will pull python from https://github.com/astral-sh/python-build-standalone. In fact astral has recently taken over stewardship of this project. I personally prefer using vanilla python that I install from python.org and keep up to date using the wonderful [MOPUp][2] project.
- the initial uv init command does not setup a .venv yet. The virtual environment is only created once you add a dependency with uv add or you call uv sync which will also create a uv.lock file that ensures consistent package versions


### workspaces

If you are in a uv project directory and you call uv init again, you create a workspace. This is actually what I want for my main application: a mono-repo structure with several subprojects, each with its own pyproject.toml file. More about workspaces later...




Some more resources for details on uv:
[Charlie Marsh's recent talk about uv][3]
[A detaile iv blog on Saas Pegasus][4]
[talk python to me podcast with Charlie Marsh][5]

### Parsing uv commands for project initialisation

To get started I am letting uv build the project setup capturing the commands via argparse in a
cli.py module. There are many other options to do this but I am used to argparse and it serves me
well here. There aren't too many commands to handle.
This is the overview you get via uv-init --help
```
Description:                                                                                │
│   Initialize a new Python project with uv                                                   │
│                                                                                             │
│ Usage:                                                                                      │
│   uv-init project_name [-t lib|package|app] [-p 3.13|3.12|3.11|3.10] [-w] [-g] [--private]  │
│                                                                                             │
│ Arguments:                                                                                  │
│   project_name The name of the project (no spaces or under-scores allowed)                  │
│                                                                                             │
│ Options:                                                                                    │
│   -t, --type  The type of project to create (default: lib)                                  │
│   -p, --python [3.13|3.12|3.11|3.10] The python version to use (default: 3.12)              │
│   -w, --workspace Create a workspace                                                        │
│   -g, --github Create and initialize a GitHub repository                                    │
│   --private Create a private GitHub repository (requires --github)
```
At this stage I haven't done anything yet except capturing uv commands to handle the project setup.
The type argument sets the project as either a library or package. By default python 3.12 is used, except
otherwise specified. -w sets a loop ina ction to generate workspace packages. uv automatically adds an empty README file and initialises git. I enhanced this a little by using a generic README template, a .gitignore file suited for python projects, a MIT licence and a tests directory with a dummy test\_init.py file. I use a .env file that stored environment variable for AUTHOR\_NAME and AUTHOR\_EMAIL that I use to populate these template files. There is also an option to set up a remote github repo with the -g flag, but this requires a valid GITHUB-TOKEN environment variable in the .env file.
So the project structure will now look like this for a simple my-app project (I'll discuss workspaces in more detail below):

```bash
├── .gitignore
├── .python-version
├── LICENSE
├── README.md
├── pyproject.toml
├── src
│   └── my_app
│       ├── __init__.py
│       └── py.typed
├── tests
│   └── test_init.py
└── uv.lock
```

## development tools install.

Having initialised the project I now want to set up various tools that support a consistent development workflow. This is done via uv add --dev to install the following dev dependencies: ruff, mypy, pytest, commitizen and pre-commit, I am also installing python-dotenv to deal with .env files. This will be required for my logger set up. For each of these I have specific configurations that I generally use, so I have config templates that are added to the pyproject.toml file. I'll discuss these separately in the next sections

### ruff
Ruff takes care of formatting your code, detecting syntax errors and enforcing style rules. As uv its written in Rust, blazingly fast and maintained by Astral. Specific linting rules can be configured in a section of the pyproject.toml file. I use this configuration template:

```toml
# ===========================
# Ruff Configuration Section
# ===========================

[tool.ruff]
line-length = 79
lint.select = [
    "E", "F", "W", #flake8
    "UP", # pyupgrade
    "I", # isort
    "BLE", # flake8-blind-exception
    "B", # flake8-bugbear
    "A", # flake8-builtins
    "C4", # flake8-comprehensions
    "ISC", # flake8-implicit-str-concat
    "G", # flake8-logging-format
    "PIE", # flake8-pie
    "SIM", # flake8-simplify
]
lint.ignore = [
    "E501", # line too long. let black handle this
    "UP006", "UP007", # type annotation. As using magicgui require runtime type annotation then we disable this.
    "SIM117", # flake8-simplify - some of merged with statements are not looking great with black, incompatible with Python < 3.10
    "ISC001", # string concatenation conflicts with formatter
]

exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".mypy_cache",
    ".pants.d",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "venv",
    "*vendored*",
    "*_vendor*",
]

fix = true

```

This includes a broad range of rules from Flake8 and its extensions, such as E, F, W (core Flake8), UP (pyupgrade), I (isort), and various specialized plugins like flake8-bugbear, flake8-comprehensions, and more. It also has a set of specific ignored rules and excluded paths that I find useful.
This is copied into the pyproject.toml file during the setup.

You can find more info on Ruff in the [documentation][6]. There are lots of blogs and webinars out there.
Here is one from pycharm with Charlie Marsh: [ruff webinar][7]

### mypy
This is my tool of choice for type checking. Static typing in Python is not something you do much when you work on code snippest and data analysis in jupyter notebooks. But it becomes really useful when you are developing a larger code base. It helps eliminating bugs, replaces the need for length docstrings and makes code more readable and maintainable.
Again, the specific workings of mypy can be adapted using a config section in pyproject.toml. Here is my template:

```toml
# ===========================
# Mypy Configuration Section
# ===========================

[tool.mypy]
strict = true
python_version = {python_version}
exclude = [
    "tests/.*",
    ".venv/.*",
    "venv/.*",
    "env/.*",
    "build/.*",
    "dist/.*",
    "migrations/.*",
]

incremental = true
cache_dir = ".mypy_cache"
ignore_missing_imports = false
follow_imports = "silent"
pretty = true
warn_unused_configs = true

["tool.mypy.some_untyped_package.*"]
ignore_missing_imports = true

["tool.mypy.another_untyped_package.*"]
ignore_missing_imports = true

```

- strict = true to true enforces 100% type accuracy. This can become cumbersome and decided to exclude tests for that reason. However, my aim is to have consistent type checking and strict = True is enforcing this.
-  {python\_version} allows to add the version dynamically as the project setup is underway
- incremental - true optimises performance allowing mypy to cache type checking results and only recheck files that have changed since the last run.
- ignore\_missing\_imports = false  mypy will report errors for any imports that it cannot find type information for, ensuring that all dependencies are properly typed or stubbed.
- follow\_imports = "silent" tells mypy to follow imports normally but suppress error messages related to missing type hints in those imports.
- pretty = true Enables pretty-printed output
- warn\_unused\_configs = true issue warnings about configuration options that are set but not used
- ["tool.mypy.some\_untyped\_package"] placeholders that should be replaced by project specific depedncies that do not have type hints available.

### Commitizen
This is a command line tool that is designed to standardise commit messages, support automated versioning based on conventional commits and maintain a consistent changelog for project development. I always get into a mess with version numbers and my commit messages usually are a waste of time. This tool made me rethink my strategy and helps me keep a clear and streamlined development process that is well documented.
The main point of action is the commit message that will be the decision point for the change in version number and the record kept in the changelog. This is done via conventional commits - a standardized specification for writing clear and consistent commit messages.
Their basic format is:
```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```
Common types include:

- feat: A new feature
- fix: A bug fix
- docs: Documentation changes
- style: Changes that don't affect code functionality (formatting, etc.)
- refactor: Code changes that neither fix bugs nor add features
- test: Adding or correcting tests
- chore: Changes to the build process or auxiliary tools

Different commit types can trigger different version increments:

- fix commits trigger PATCH releases (1.0.0 → 1.0.1)
- feat commits trigger MINOR releases (1.0.0 → 1.1.0)
- Commits with BREAKING CHANGE in the footer trigger MAJOR releases (1.0.0 → 2.0.0)

This is really useful during development to understand what changes were made and why by scanning commit messages.
Also, commitizen enables  automatic changelog generation and release notes.

In the uv-init project I use the following commitizen configuration in a separate template toml file that
will be added to pyproject.toml files during project setup.

```toml
# ===========================
# Commitizen Configuration Section
# ===========================

[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
tag_format = "v$version"
version_files = [
    "src/{module_name}/__init__.py:__version__",
    "pyproject.toml:version",
    "README.md:version-[0-9]+\\.[0-9]+\\.[0-9]+"
]
version_provider = "commitizen"
major_version_zero = true
bump_message = "bump: version $current_version → $new_version"
update_changelog_on_bump = true
annotated_tag = true
```
Key aspects here are:

- Commit Standard: Using the Conventional Commits format (cz\_conventional\_commits)
- Current Version: Starting at version 0.1.0
- Automated Changelog: Updates CHANGELOG.md when bumping versions
- Annotated Tags: Creates detailed Git tags with commit information in the format v0.1.0
- Custom Bump Message: Uses template "bump: version $current\_version → $new\_version"

The configuration tracks version information in the following files:

- Python module's \_\_init\_\_.py file
- pyproject.toml
- README.md

This is applied to the different packages in monorepo projects with multiple pyproject.toml, README and
__init__.py files.

To trigger a commitizen commit you need to use
```bash
cz commit
```
And this will then guide you through a formal commit message.
If your commit is fix, feat or BREAKING CHANGe, you can trigger a bump with

```bash
cz bump
```
The change will then applied to the version info in README, pyproject.toml and __init__.py.

It gets a bit complicated with mono-repos where there are multiple packages with individual
pyproject.toml files. My setup at the moment automatically adds the specific commitizen configs
to each package.
When you trigger a commit and want to bump the version of a specific package you need to
cd into that directory. So standard commits and bumps from root will only bump the root package,
while commits and bumps from within a package directory will bump the specific package.
This is a bit clumsy but it avoids a much more complex setup and it generally works for me.

A common way to automate this is to set up pre-commit hooks or continuous integration with GitHub Actions to handle version bumping. I'll expand on this in detail below, but my preferred approach is to integrate versioning within a continuous integration pipeline using GitHub Actions. I deliberately don't enforce version bumping in pre-commit hooks, as I prefer to handle testing with GitHub Actions and only bump versions after all tests have passed successfully.

Without GitHub integration, my setup requires manual version bumps, which can be a bit clunky, but I rarely use it without setting up a GitHub repository upstream and configuring CI with proper testing. This approach ensures that version numbers only increase when code is fully validated.

I'll cover more about this workflow in the Pre-commit Hooks and CI/CD sections below.

Here is the link to the commitizen documentation: https://commitizen-tools.github.io/commitizen/

There lots of youtube videos etc. Version bumping is a topic that is quite important and can
get complex and messy pretty quickly. I haven't found a lot of discussion of this on the main
python podcasts and online learning resources compared to other developer tooling issues.


### testing
ok, this is another subject that could fill quite a few pages here.
When you start working with data and python as you do in science, testing is the last thing
you think about. But when you develop code for other people to use slowly but surly it becomes
probably the most important topic to consider during development. My aim is to have a codebase
that will outlast me, or at least that I myself can come back to regularly and have confidence that
a small change won't break the entire thing. Currently for my image analysis project
I probably spend as much time on planning my testing strategy than actually developing the application.
I am using the pytest framework, which is the standard tool, and generally I try to keep
a healthy balance between unit and integration testing, although personally I find integration tests
more trustworthy. When I run the entire code and I get the correct data out, I can be assured that all works.
Having said that, testing individual functions and logic is important and useful during development.
I find myself more and more in the test driven development camp, where designing the tests precedes or at least
happens in parallel to developing functions.

With uv-init I am creating new Python projects that automatically set up a comprehensive testing infrastructure.
I use a template with a come a pre-configured pytest setup added to the pyproject.toml file in the new repository:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q"
testpaths = ["tests"]
python_files = ["test_*.py"]
```
This configuration:

- Requires Pytest 6.0 or higher
- Uses compact output (-q) but shows test summaries for all except passed tests (-ra)
- Automatically finds tests in the tests directory
- Recognizes files that start with test\_ as test files

The testing framework follows a conventional structure:

```text
project_name/
├── src/
│   └── project_name/
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Shared fixtures and configuration
│   └── test_*.py        # Test modules
```

When the GitHub integration flag (-g) is used, uv-init also sets up a CI workflow
that runs your tests automatically. More about CI later.

## Logging

When I started writing code I mainly used print statements to the console to feedback information
about the dataflow and execution steps. This quickly ends in a mess with a mix of debug information
and true feedback from the program to the user littering the screen as the code executes.
There comes a point where this becomes unsustainable and you start moving towards proper debugging and
logging. I won't discuss debugging here but if you are interested in the topic here is an excellent
[debugging talk][8]
Now to logging: For me this is the main solution to separate deeper information of
code progression and debugging and user feedback. For the latter I try to use clear
and well formatted messages using the [rich][9]package using different colors to convey seoerate levels of information,
for example red for errors, green for progress reports etc..
But while I develop and also when something goes wrong in real life scenarios, I want more information
about what is going on with my code. So at critical checkpoints along the way, I add log statements
that come at different levels, error, warning, info, debug.
If you never heard used logging before and are interested, there are planty of tutorials online
but actually the [python documentation][10] does a great job
at getting you started.

My problem with this was that now the log statements are littering the terminal as the program
runs and I haven't really solved the separation of cleab user interface and informative developer
experience. One way to deal with this is to set the log level to debug in development and warning
in deployment, but then you miss information if you want to check what went wrong when an error occurs.
Another way to deal with this is to switch between showing the logs on the console or saving them to a file.
So for a decent logging setup you want to be able to control the behaviour of the logger and
switch quickly between different outputs and log levels.

### ENV variables

Im using environment variables for this: uv-init comes with a config.py file that contains to key functions: set\_env\_vars() and get\_logger()

The set\_env\_vars function loads environment variables from configuration files (.env files).
For this uv-init install the [dotenv][11] package as a dependency.

The function first checks if an ENV environment variable has been set in your system. If no ENV variable is found, it defaults to "development". Then it looks for a specific configuration file matching that environment (for example, .env.development if ENV is set to development). If it finds that environment-specific file, it loads the variables from that file and completes its task. If the environment-specific file isn't found, the function falls back to looking for a general .env file in your project's root directory. It loads from this file if it exists.
My default .env file has all the parameters for my logger and looks like this:

```text
# Logging Configuration

LOG_LEVEL=INFO

ENABLE_CONSOLE_LOGGING=true

ENABLE_FILE_LOGGING=true

LOG_FILE_PATH=logs/app.log

LOG_MAX_BYTES=1048576

LOG_BACKUP_COUNT=5

LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s

```
By setting up various .env files (eg .env.dev and .env.prod) and setting an ENV variable
you can switch between the different styles of logging. This is useful for example when you
want to test the user experience in a program and switch quickly between dev and prod mode.

The ENV variable can be set in a terminal session with
```bash
export ENV="DEV"
```
or in python via
```python
import os
os.environ["ENV"] = "DEV"
```
The function is executed in the __init__.py file to make the configuration available to the program.
You can use the .env files for other configurations, like srever addresses and passwords.
Its a good idea to exclude this from git!

### logging factory




[1]:	https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/?featured_on=pythonbytes
[2]:	https://pypi.org/project/MOPUp/
[3]:	https://www.youtube.com/watch?v=gSKTfG1GXYQ%5C
[4]:	https://www.saaspegasus.com/guides/uv-deep-dive/
[5]:	https://talkpython.fm/episodes/show/476/unified-python-packaging-with-uv
[6]:	https://astral.sh/ruff
[7]:	https://duckduckgo.com/?q=Ruff+linter&iax=videos&ia=videos&iai=https://www.youtube.com/watch?v%3DjeoL4qsSLbE
[8]:	https://duckduckgo.com/?q=Nina+Zakharenko+debugging&iax=videos&ia=videos&iai=https://www.youtube.com/watch?v%3DMPuRWFr5tks
[9]:	https://rich.readthedocs.io/en/stable/introduction.html
[10]:	https://docs.python.org/3/library/logging.html
[11]:	https://pypi.org/project/python-dotenv/
