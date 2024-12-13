# UV Init

A command-line tool for initializing Python projects usng the new uv project management tool:
https://docs.astral.sh/uv/
This package integrates uv commands with a template for development configs, commitizen versionin,precommit hooks and CI

## Status

Version: ![version](https://img.shields.io/badge/version-0.3.5-blue)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Development state of the program
This project is in active development. Current version: 0.3.5
Features and APIs may change. Please report issues on GitHub.

## Versioning

This project uses [Semantic Versioning](https://semver.org/) and [Conventional Commits](https://www.conventionalcommits.org/).


## Authors

Helfrid Hochegger

### Dependencies

- Requires Python 3.13 (not tested on other versions)
- UV package manager installed (https://github.com/astral-sh/uv)
- GitHub account and personal access token (if using GitHub features)


## Contact

Created by Helfrid Hochegger
Email: hh65@sussex.ac.uk
GitHub Issues: https://github.com/Helfrid/uv-init/issues

## License

This project is licensed under the MIT Licencse

## Features

- Create Python libraries, packages, or applications
- Workspace support for monorepo setups
- Automatic setup of development tools:
  - Ruff for linting and formatting
  - MyPy for type checking
  - Pytest for testing
  - Commitizen for conventional commits
  - Pre-commit hooks
- GitHub repository initialization with CI/CD workflows
- Semantic versioning support
- Python 3.10+ support for project initialisation

## Installation

Not deployed on Pypi, to use clone this repo and install using pip install or uv pip install or uv add.
Requires a .env file at the root of the project with:

AUTHOR_NAME='John Doe'
AUTHOR_EMAIL='johndoe@email.com'
GITHUB_TOKEN='insert github token'

## Usage

Basic usage to install a repo with pre-configured Ruff, Mypy, Commitizen and Pre-Commit Hooks settings, optional setup of github repo and basic CI pipeline including version bumps on conventional commit messages.

bash
```
uv-init project-name [options]
```

Options:
- `-t, --type [lib|package]`: The type of project to create (default: lib, alternative: package)
- `-p, --python [3.3.12|3.11|3.10]`: Python version to use (default: 3.12)
- `-w, --workspace`: Create a workspace (monorepo setup)
- `-g, --github`: Create and initialize a GitHub repository
- `--private`: Create a private GitHub repository (requires --github)


### Examples

Create a basic library:
bash
```
uv-init my-package -t package -p 3.13
```

Create a workspace with GitHub repository:

bash
```
uv-init my-workspace -w -g
```
creates an upstream main branch on giyhub (default public, use --private for private repos)

bash
```
uv-init my-workspace -w -g
```
This will generate a uv workspcae (see: https://docs.astral.sh/uv/concepts/projects/workspaces/)
The user will be prompted to add a common-utils library and an additional project.

## Project Structure

The generated project follows this structure:

project_name/
├── src/
│ └── project_name/
│ └── init.py
├── tests/
├── pyproject.toml
├── README.md
├── LICENSE
└── .pre-commit-config.yaml

Fro workspaces:

workspace_name/
├── packages/
│ ├── package1/
│ └── package2/
├── pyproject.toml
├── README.md
└── .pre-commit-config.yaml

# Development Tools

UV Init sets up the following development tools:

- **Ruff**: Modern Python linter and formatter
- **MyPy**: Static type checker
- **Pytest**: Testing framework
- **Commitizen**: Conventional commit tooling
- **Pre-commit**: Git hooks manager

## GitHub Integration

When using the `-g` flag, UV Init:
1. Initializes a Git repository
2. Creates a GitHub repository
3. Sets up GitHub Actions workflows for:
   - CI (linting, type checking, testing)
   - Automated releases using conventional commits

additional --private flag for optional private repos

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using conventional commits (`cz commit`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Tools Configuration

### Ruff
- Line length: 79 characters
- Selected rules: flake8, pyupgrade, isort, and more
- Automatic fixes enabled

### MyPy
- Strict mode enabled
- Configured for Python 3.12+
- Excludes tests and build directories

### Commitizen
- Uses conventional commits
- Automatic version bumping
- Changelog generation
- Version tracking in multiple files

## Workspace Features

When creating a workspace (`-w` flag), UV Init:
- Sets up a monorepo structure
- Offers to create a common utilities package
- Supports adding multiple projects
- Configures dependencies between workspace packages

## GitHub Workflows

### CI Pipeline
- Runs on Python 3.13
- Performs:
  - Code linting with Ruff
  - Type checking with MyPy
  - Unit tests with Pytest
  - Format checking

### Release Pipeline
- Automatic version bumping on main branch
- Creates releases based on conventional commits
- Generates changelogs
