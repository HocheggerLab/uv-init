#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Set the templates directory to the script's location
TEMPLATES_DIR="$(cd "$(dirname "$0")" && pwd)/template"

# Function to display usage information
usage() {
cat <<EOF
Usage: $0 [OPTIONS] <project_name> [other_package_name]

Initialize a new Python project using uv.

Options:
  --app              Initialize the project as an application. (Default: library)
  --lib              Initialize the project as a library. (Default)
  --python <version> Specify the Python version to use (e.g., 3.12). (Default: 3.12)
  --workspace        Initialize the project as a workspace. (Default: false)
  -h, --help         Display this help message and exit.

Examples:
  $0 my-library
  $0 --app my-app
  $0 --workspace my-app other-service
EOF
}

# Function to check if a command exists
check_command() {
  if ! command -v "$1" &> /dev/null; then
    echo "Error: '$1' is not installed. Please install it and try again."
    exit 1
  fi
}

# Function to copy files safely (skips if destination exists)
safe_copy() {
  SRC="$1"
  DEST="$2"

  if [[ -f "$DEST" ]]; then
    echo "Warning: '$DEST' already exists. Skipping copy."
  else
    cp "$SRC" "$DEST"
    echo "Copied '$SRC' to '$DEST'."
  fi
}

# Function to overwrite files (always copies, replacing existing files)
overwrite_copy() {
  SRC="$1"
  DEST="$2"

  cp "$SRC" "$DEST"
  echo "Overwritten '$DEST' with '$SRC'."
}

# Function for in-place file replacement compatible with both GNU sed and BSD sed
replace_placeholder_in_file() {
  local file="$1"
  local placeholder="$2"
  local replacement="$3"
  local pattern="$4"

  if [[ "$(uname)" == "Darwin" ]]; then
    # macOS/BSD sed
    sed -i '' "/$pattern/ s|$placeholder|$replacement|g" "$file"
  else
    # GNU sed
    sed -i "/$pattern/ s|$placeholder|$replacement|g" "$file"
  fi
}

# Default values
PROJECT_TYPE="lib"
PYTHON_VERSION="3.12"
IS_WORKSPACE=false

# Parse command-line arguments
PROJECT_NAME=""
OTHER_SERVICE_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --app)
      PROJECT_TYPE="app"
      shift
      ;;
    --lib)
      PROJECT_TYPE="lib"
      shift
      ;;
    --python)
      if [[ -n "$2" && ! "$2" =~ ^-- ]]; then
        PYTHON_VERSION="$2"
        shift 2
      else
        echo "Error: --python requires a version number (e.g., --python 3.11)"
        exit 1
      fi
      ;;
    --workspace)
      IS_WORKSPACE=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Error: Unknown option: $1"
      usage
      exit 1
      ;;
    *)
      if [[ -z "$PROJECT_NAME" ]]; then
        PROJECT_NAME="$1"
      elif [[ -z "$OTHER_SERVICE_NAME" ]]; then
        OTHER_SERVICE_NAME="$1"
      else
        echo "Error: Too many arguments provided"
        usage
        exit 1
      fi
      shift
      ;;
  esac
done

# Check if project name is provided
if [[ -z "$PROJECT_NAME" ]]; then
  echo "Error: Project name is required."
  usage
  exit 1
fi

# If workspace is enabled, check for second argument
if [[ "$IS_WORKSPACE" == "true" && -z "$OTHER_SERVICE_NAME" ]]; then
  echo "Error: When using --workspace, you must provide a second package name."
  usage
  exit 1
fi

# Create a valid Python package name by replacing hyphens with underscores and converting to lowercase
PYTHON_PACKAGE_NAME="$(echo "$PROJECT_NAME" | tr '-' '_' | tr '[:upper:]' '[:lower:]')"

# Check for required commands
check_command "uv"
check_command "git"
check_command "cp"
check_command "mkdir"

# Check if the project directory already exists
if [[ -d "$PROJECT_NAME" ]]; then
  echo "Error: Directory '$PROJECT_NAME' already exists."
  exit 1
fi

echo "Initializing a new Python $PROJECT_TYPE project with uv..."

# Step 1: Initialize the project with uv
if [[ "$PROJECT_TYPE" == "lib" ]]; then
  if uv init --lib --python "$PYTHON_VERSION" "$PROJECT_NAME"; then
    echo "Project '$PROJECT_NAME' initialized successfully."
  else
    echo "Error: Failed to initialize project with uv."
    exit 1
  fi
elif [[ "$PROJECT_TYPE" == "app" ]]; then
  if uv init --app --package --python "$PYTHON_VERSION" "$PROJECT_NAME"; then
    echo "Project '$PROJECT_NAME' initialized successfully."
  else
    echo "Error: Failed to initialize project with uv."
    exit 1
  fi
fi

# Navigate into the project directory
cd "$PROJECT_NAME"

# Step 2: Add development dependencies
if uv add --dev ruff pytest mypy commitizen; then
  echo "Development dependencies added successfully."
else
  echo "Error: Failed to add development dependencies."
  exit 1
fi

# Check if the templates directory exists
if [[ ! -d "$TEMPLATES_DIR" ]]; then
  echo "Error: Templates directory '$TEMPLATES_DIR' does not exist."
  exit 1
fi

# Step 3: Copy template files
# Overwrite README.md for main project
if [[ "$IS_WORKSPACE" == "true" ]]; then
    # Force project type to be an app with package structure
    PROJECT_TYPE="app"
    
    # Create packages directory and initialize workspace members
    mkdir -p packages
    cd packages || exit 1
    
    # Initialize shared utils library
    if uv init --lib --python "$PYTHON_VERSION" "shared-utils"; then
        echo "Shared utilities package initialized."
        # Add version to shared-utils __init__.py
        echo '__version__ = "0.1.0"' > "shared-utils/src/shared_utils/__init__.py"
        # Copy package README
        if [[ -f "$TEMPLATES_DIR/README-package.md" ]]; then
            overwrite_copy "$TEMPLATES_DIR/README-package.md" "shared-utils/README.md"
            replace_placeholder_in_file "shared-utils/README.md" "{project_name}" "shared-utils" "."
            replace_placeholder_in_file "shared-utils/README.md" "{root_project}" "$PROJECT_NAME" "."
        fi
    fi
    
    # Initialize other service as a package
    if uv init --app --package --python "$PYTHON_VERSION" "$OTHER_SERVICE_NAME"; then
        echo "Other service '$OTHER_SERVICE_NAME' initialized."
        # Convert other service name to Python package name
        OTHER_SERVICE_PACKAGE_NAME="${OTHER_SERVICE_NAME//-/_}"
        # Add version to other service __init__.py
        echo '__version__ = "0.1.0"' > "$OTHER_SERVICE_NAME/src/$OTHER_SERVICE_PACKAGE_NAME/__init__.py"
        # Copy package README
        if [[ -f "$TEMPLATES_DIR/README-package.md" ]]; then
            overwrite_copy "$TEMPLATES_DIR/README-package.md" "$OTHER_SERVICE_NAME/README.md"
            replace_placeholder_in_file "$OTHER_SERVICE_NAME/README.md" "{project_name}" "$OTHER_SERVICE_NAME" "."
            replace_placeholder_in_file "$OTHER_SERVICE_NAME/README.md" "{root_project}" "$PROJECT_NAME" "."
        fi
    fi
    
    cd .. || exit 1  # Back to project root
    
    # Copy workspace README
    if [[ -f "$TEMPLATES_DIR/README-workspace.md" ]]; then
        overwrite_copy "$TEMPLATES_DIR/README-workspace.md" ./README.md
        replace_placeholder_in_file "./README.md" "{project_name}" "$PROJECT_NAME" "."
        replace_placeholder_in_file "./README.md" "{other_service_name}" "$OTHER_SERVICE_NAME" "."
    fi
fi

# Copy README for non-workspace projects
if [[ "$IS_WORKSPACE" != "true" ]]; then
    if [[ -f "$TEMPLATES_DIR/README.md" ]]; then
        overwrite_copy "$TEMPLATES_DIR/README.md" ./README.md
        replace_placeholder_in_file "./README.md" "{project_name}" "$PROJECT_NAME" "."
        replace_placeholder_in_file "./README.md" "{author}" "HocheggerLab" "."
        replace_placeholder_in_file "./README.md" "{email}" "hh65@sussex.ac.uk" "."
    fi
fi

# Overwrite .gitignore
if [[ -f "$TEMPLATES_DIR/.gitignore" ]]; then
  overwrite_copy "$TEMPLATES_DIR/.gitignore" ./.gitignore
else
  echo "Warning: '.gitignore' not found in templates directory. Skipping copy."
fi

# Copy LICENSE safely
if [[ -f "$TEMPLATES_DIR/LICENSE" ]]; then
  safe_copy "$TEMPLATES_DIR/LICENSE" ./LICENSE
else
  echo "Warning: 'LICENSE' not found in templates directory. Skipping copy."
fi

# Step 4: Append Ruff configuration
if [[ -f "$TEMPLATES_DIR/ruff-config.toml" ]]; then
  cat "$TEMPLATES_DIR/ruff-config.toml" >> ./pyproject.toml
  echo "Appended 'ruff-config.toml' to 'pyproject.toml'."
else
  echo "Warning: 'ruff-config.toml' not found in templates directory. Skipping append."
fi

# Step 5: Append Pytest configuration
if [[ -f "$TEMPLATES_DIR/pytest-config.toml" ]]; then
  cat "$TEMPLATES_DIR/pytest-config.toml" >> ./pyproject.toml
  echo "Appended 'pytest-config.toml' to 'pyproject.toml'."
else
  echo "Warning: 'pytest-config.toml' not found in templates directory. Skipping append."
fi

# Step 6: Append Commitizen configuration
if [[ -f "$TEMPLATES_DIR/commitizen-config.toml" ]]; then
    printf "\n" >> ./pyproject.toml
    
    if [[ "$IS_WORKSPACE" == "true" ]]; then
        # Use workspace config
        if [[ -f "$TEMPLATES_DIR/commitizen-workspace-config.toml" ]]; then
            cat "$TEMPLATES_DIR/commitizen-workspace-config.toml" >> ./pyproject.toml
            # Replace placeholders in both version_files and projects sections
            replace_placeholder_in_file "./pyproject.toml" "{package_name}" "${PYTHON_PACKAGE_NAME}" "."
            replace_placeholder_in_file "./pyproject.toml" "{other_service_name}" "${OTHER_SERVICE_NAME}" "."
            # Replace the package name with underscore version for __init__.py path
            OTHER_SERVICE_PACKAGE_NAME="${OTHER_SERVICE_NAME//-/_}"
            replace_placeholder_in_file "./pyproject.toml" "{other_service_package_name}" "${OTHER_SERVICE_PACKAGE_NAME}" "."
            echo "Appended workspace commitizen configuration to 'pyproject.toml'."
        else
            echo "Warning: 'commitizen-workspace-config.toml' not found in templates directory."
        fi
    else
        # Single package configuration
        cat "$TEMPLATES_DIR/commitizen-config.toml" >> ./pyproject.toml
        replace_placeholder_in_file "./pyproject.toml" "{package_name}" "${PYTHON_PACKAGE_NAME}" "."
    fi
fi

# Step 7: Append Mypy configuration
if [[ -f "$TEMPLATES_DIR/mypy-config.toml" ]]; then
  # Ensure there is a newline before appending
  printf "\n" >> ./pyproject.toml
  cat "$TEMPLATES_DIR/mypy-config.toml" >> ./pyproject.toml
  echo "Appended 'mypy-config.toml' to 'pyproject.toml'."
else
  echo "Warning: 'mypy-config.toml' not found in templates directory. Skipping append."
fi

# Step 8: Edit src/PYTHON_PACKAGE_NAME/__init__.py
INIT_FILE="src/$PYTHON_PACKAGE_NAME/__init__.py"
if [[ -f "$INIT_FILE" ]]; then
  # Insert __version__ line at the top of the file with double quotes
  echo '__version__ = "0.1.0"' | cat - "$INIT_FILE" > temp && mv temp "$INIT_FILE"
  echo "Added version line to the top of '$INIT_FILE'."
else
  echo "Warning: '$INIT_FILE' not found. Skipping version line addition."
fi

# Step 9: Create an empty tests directory
if [[ -d "tests" ]]; then
  echo "Warning: 'tests' directory already exists. Skipping creation."
else
  mkdir tests
  echo "Created empty 'tests' directory."
fi

# Step 10: Initialize Git
if git init; then
  echo "Git repository initialized successfully."
else
  echo "Error: Failed to initialize Git repository."
  exit 1
fi

echo "Project '$PROJECT_NAME' setup complete."