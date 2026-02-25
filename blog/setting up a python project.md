## setting up a python project

When starting a software development project in python, the first thing to decide is how to set up a python environment and which package manager to use. Everyone agrees that there are currently too many options to do this. So questions to ask here is: where is my python coming from? where are my dependencies defined? How is my project set up and organised?
Python comes in many flavours: conda, home-brew, pyenv. If you look closely, you probably have more python versions on your computer than you care to know about. Additionally, you don’t want to use your main python installation for individual projects, but isolate them using virtual environments.
I will cut a long story short here and just lay out my setup that works well for me:
### Python Installation
When I began working with python, I quickly got into a mess with having many different versions of python installed on my mac, with conda, homebrew and pyenv. Now, I download python directly from python.org and have the main versions copied into my PATH in my shell config file, /.zshrc"  on a mac.
Now for most people (me included), that's already foreign territory, but if you want to have a productive environment you need to get to know this config file and make your self at home there!

> callout
Note! If you are on windows your shell config file depends on the terminal that you are using. For PowerShell you want to look for $PROFILE; and on Linux your config depends on the shell you are using, typically .bashrc or .zshrc. For Mac users, zsh is default, and you can generate a .zshrc file in your home directory. Going onto the finer details of shell commands etc is beyond the scope here but there are fine courses on youtube!

To have a clean vanilla version of python available, I have the following PATH configuration in my .zshrc file:

```bash

# Path to Python executables
export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"

```

I have three python distributions stored here and the default will be python 3.13. So in my terminal I can either evoke Python 3.13 by simply specifying python3, or specifically python 3.12 or 3.11 with python3.12 or python3.11.
For example, if I want to make sure that this works I can check with:

```bash
which python3
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3

```

> callout
> a nice little helper tool to keep your python versions up to date is [https://mopup.readthedocs.io/en/latest/index.html][1]

With uv you can actually get project specific python versions quickly and easily without worrying about updates and PATH configurations, but I still prefer having a defined system python version that I can call on in the terminal and that I keep up to date myself.

One last thing before we move on to uv: I still have a lot of legacy project with conda, so I have conda installed via the mini forge distribution but have it switched off by default. The trick here is to have the following line in the condarc file.

```bash
conda autoactivate = false
```

This means you can start a conda project by activating a conda environment, but it won't interfere with other projects that don’t use conda.



—
## Setting Up Your Python Environment

Before we get to uv, let me walk you through the foundation I built. It might look a bit finicky at first, but trust me—getting this right saves a lot of headaches later.

### Where Does Python Come From?

Here's the problem: Python comes in many flavours—conda, homebrew, pyenv—and if you look closely, you probably have more Python versions on your computer than you care to know about. On top of that, you definitely don't want to use your system Python installation for individual projects. You need isolation, which is where virtual environments come in. They let each project live in its own little bubble with its own dependencies.

So the questions become: Where is my Python coming from? How do I manage multiple versions? And how do I keep projects isolated?

Everyone agrees there are too many options to answer these questions. I'm going to cut a long story short and just lay out what works for me.

### My Python Setup

I download Python directly from python.org and keep multiple versions in my PATH. On macOS, that means editing my `.zshrc` file (the shell configuration file that runs every time you open a terminal). Yes, I know—that's already foreign territory if you're coming from Jupyter notebooks. But here's the thing: if you want a productive environment, you need to get to know this config file and make yourself at home there.

> **A note on platforms:** If you're on Windows, you'll be looking at `$PROFILE` in PowerShell instead. On Linux, it's typically `.bashrc` or `.zshrc` depending on your shell. The principle is the same—you're adding Python to your PATH so you can use it from anywhere. I'll focus on macOS here, but the concept translates.

Here's what my `.zshrc` looks like:
```bash
# Path to Python executables
export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:$PATH"
```

I have three Python distributions here, and the default is Python 3.13. So in my terminal, I can either invoke `python3` to get 3.13, or specifically `python3.12` or `python3.11` to pick a different version.

Want to check if this works? Try:
```bash
which python3
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3
```

If you see a path like that, you're good.

> **Keeping Python up to date:** A nice little helper tool for this is [MOPUp][2], which automates updating your Python installations.

### Why Vanilla Python?

You might wonder why I chose to download directly from python.org instead of using conda or pyenv. Honestly, it comes down to simplicity and reproducibility. I get the exact same Python binary on every machine I use, with no dependency on other package managers. And soon—when we get to uv—uv will actually handle version management for me anyway. This setup is just my baseline.

### What About Virtual Environments?

Virtual environments are isolated Python installations for individual projects. Think of them as sandboxes: each project has its own copy of Python and its own set of dependencies, so one project's package versions don't mess with another's. You'll always want to create a virtual environment for each project you work on. The good news? uv handles this automatically, so you won't need to think about it much.

### Managing Legacy Projects

I still have a lot of older projects that use conda, so I have it installed via miniforge. But here's the trick: I have it switched off by default with this line in my `.condarc` file:
```bash
conda autoactivate = false
```

This way, if I want to work on a conda project, I can activate a conda environment manually. But it won't interfere with everything else I'm doing. It's a nice way to keep things compartmentalized while you transition to other tools.

## Now, Let's Talk About uv

You've got a clean Python installation and you understand virtual environments. Now comes the part that actually simplifies everything: uv.

---























Charlie Marsh‘s Astral is on a mission to clear this up and to build a unified system called uv that is inspired by the way Rust is managed by cargo. Coming from data science, I am used to conda and mamba which is great for data analysis projects for example. But its not really cut out to support proper software development. So I decided to experiment with uv and use this as the basis for my project setup pipeline. I still have conda via the miniforge distribution on my machine but have it switched off by default. The trick here is to have the following line in the condarc file.

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
- Having said this, uv makes it easy to use scripts with dependencies, this could lead to a revival of small utiliuty scripts in python. See [here][3] for a comprehensive guide.
- --package (or --package --app) generate a more comprehensive project structure with a script entry point and a hatchling build system.
- --lib generates a similar structure but doesn't have the script entry point in pyproject.toml; so its the starting point for a pure library project.
- A really important feature is the way uv handles the python distribution. you can choose your python version using --python 3.13 etc.. if you have downloaded this from python.org and its installed in your system, uv will by default use this version. Otherwise it will pull python from https://github.com/astral-sh/python-build-standalone. In fact astral has recently taken over stewardship of this project. I personally prefer using vanilla python that I install from python.org and keep up to date using the wonderful [MOPUp][4] project.
- the initial uv init command does not setup a .venv yet. The virtual environment is only created once you add a dependency with uv add or you call uv sync which will also create a uv.lock file that ensures consistent package versions


### workspaces

If you are in a uv project directory and you call uv init again, you create a workspace. This is actually what I want for my main application: a mono-repo structure with several subprojects, each with its own pyproject.toml file. More about workspaces later...




Some more resources for details on uv:
[Charlie Marsh's recent talk about uv][5]
[A detaile iv blog on Saas Pegasus][6]
[talk python to me podcast with Charlie Marsh][7]

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
Python distribution and packaging
```

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
- Having said this, uv makes it easy to use scripts with dependencies, this could lead to a revival of small utiliuty scripts in python. See [here][8] for a comprehensive guide.
- --package (or --package --app) generate a more comprehensive project structure with a script entry point and a hatchling build system.
- --lib generates a similar structure but doesn't have the script entry point in pyproject.toml; so its the starting point for a pure library project.
- A really important feature is the way uv handles the python distribution. you can choose your python version using --python 3.13 etc.. if you have downloaded this from python.org and its installed in your system, uv will by default use this version. Otherwise it will pull python from https://github.com/astral-sh/python-build-standalone. In fact astral has recently taken over stewardship of this project. I personally prefer using vanilla python that I install from python.org and keep up to date using the wonderful [MOPUp][9] project.
- the initial uv init command does not setup a .venv yet. The virtual environment is only created once you add a dependency with uv add or you call uv sync which will also create a uv.lock file that ensures consistent package versions


### workspaces

If you are in a uv project directory and you call uv init again, you create a workspace. This is actually what I want for my main application: a mono-repo structure with several subprojects, each with its own pyproject.toml file. More about workspaces later...




Some more resources for details on uv:
[Charlie Marsh's recent talk about uv][10]
[A detaile iv blog on Saas Pegasus][11]
[talk python to me podcast with Charlie Marsh][12]

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

[1]:	https://mopup.readthedocs.io/en/latest/index.html
[2]:	https://mopup.readthedocs.io/en/latest/index.html
[3]:	https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/?featured_on=pythonbytes
[4]:	https://pypi.org/project/MOPUp/
[5]:	https://www.youtube.com/watch?v=gSKTfG1GXYQ%5C
[6]:	https://www.saaspegasus.com/guides/uv-deep-dive/
[7]:	https://talkpython.fm/episodes/show/476/unified-python-packaging-with-uv
[8]:	https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/?featured_on=pythonbytes
[9]:	https://pypi.org/project/MOPUp/
[10]:	https://www.youtube.com/watch?v=gSKTfG1GXYQ%5C
[11]:	https://www.saaspegasus.com/guides/uv-deep-dive/
[12]:	https://talkpython.fm/episodes/show/476/unified-python-packaging-with-uv
