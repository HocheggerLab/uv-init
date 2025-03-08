# Comprehensive Logging Setup for Python Projects

In this blog post, I'll describe the logging system I've implemented in my project. This setup provides flexible, configurable logging that adapts to different environments while remaining easy to use throughout the codebase.

## Core Design Philosophy

My logging system follows these key principles:
- **Environment-based configuration**: Different environments (development, production, etc.) can have different logging settings
- **Multiple output targets**: Support for both console and file logging
- **Sensible defaults**: Works out-of-the-box with reasonable settings
- **Centralized configuration**: One place to manage all logging settings
- **Simple developer experience**: Easy to use in any module

## Environment Configuration

The logging system uses environment variables loaded from `.env` files to control its behavior. This allows flexible configuration without code changes:

```python
# Load environment variables based on the ENV variable
def set_env_vars() -> None:
    # Set default environment variables if .env doesn't exist
    os.environ.setdefault("LOG_LEVEL", "INFO")
    os.environ.setdefault("LOG_FILE_PATH", "logs/app.log")
    os.environ.setdefault("ENABLE_CONSOLE_LOGGING", "True")
    os.environ.setdefault("ENABLE_FILE_LOGGING", "True")

    # First load the minimal .env to get the ENV variable
    minimal_env_path = project_root / ".env"
    if minimal_env_path.exists():
        load_dotenv(minimal_env_path)

    # Then load environment-specific settings (e.g., .env.development)
    ENV = os.getenv("ENV", "development").lower()
    env_specific_path = project_root / f".env.{ENV}"
    if env_specific_path.exists():
        load_dotenv(env_specific_path, override=True)
```

This pattern allows for a layered configuration approach:
1. Default values if nothing else is specified
2. Base configuration in `.env`
3. Environment-specific overrides in `.env.<environment>`

## The Logger Factory

The heart of the system is the `get_logger` function, which acts as a factory for properly configured loggers:

```python
def get_logger(name: str) -> logging.Logger:
    # Intelligent handling of __main__ and module paths
    if name == "__main__":
        # Logic to determine correct module name
        # ...

    # Get or create the logger
    logger = logging.getLogger(name)

    # Configure root logger if not already done
    root_logger = logging.getLogger("{module_name}")
    if not root_logger.handlers:
        # Configure based on environment variables
        # ...

    return logger
```

This approach ensures:
1. Loggers use the correct module name for better traceability
2. Root configuration happens only once
3. All loggers inherit the same base configuration

## Output Handlers

The system supports both console and file logging, controlled by environment variables:

```python
# Console Handler
if ENABLE_CONSOLE_LOGGING:
    ch = logging.StreamHandler()
    configure_log_handler(ch, LOG_LEVEL, formatter, root_logger)

# File Handler with rotation
if ENABLE_FILE_LOGGING:
    log_path = Path(LOG_FILE_PATH)
    if log_dir := log_path.parent:
        log_dir.mkdir(parents=True, exist_ok=True)

    fh = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
    )
    configure_log_handler(fh, LOG_LEVEL, formatter, root_logger)
```

The `RotatingFileHandler` provides log rotation capabilities, preventing log files from growing too large and managing archival automatically.

## Using the Logger

Using this logger in any module is straightforward:

```python
# In any module of your project
from template.config import get_logger

# Get a logger for this module
logger = get_logger(__name__)

def some_function():
    logger.debug("Starting function execution")
    try:
        # Do something
        logger.info("Operation completed successfully")
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        raise
```

## Key Features and Benefits

1. **Smart Module Names**: Even when running a file directly (`__main__`), the logger attempts to determine the proper module path.

2. **Automatic Directory Creation**: If logging to a file, the system ensures the log directory exists.

3. **Configurable Formatting**: The log format is configurable through environment variables.

4. **Log Rotation**: Prevents log files from consuming too much disk space.

5. **Environment Adaptability**: Easily switch between development (verbose console logging) and production (critical issues to files) configurations.

6. **Centralized Configuration**: All logging settings in one place, making it easy to maintain and update.

## Configurable Parameters

Some key parameters that can be set via environment variables:

- `LOG_LEVEL`: Controls verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FORMAT`: The format string for log messages
- `ENABLE_CONSOLE_LOGGING`: Whether to output logs to the console
- `ENABLE_FILE_LOGGING`: Whether to output logs to files
- `LOG_FILE_PATH`: Where log files are stored
- `LOG_MAX_BYTES`: Maximum size before rotating log files
- `LOG_BACKUP_COUNT`: Number of backup log files to keep

This logging setup provides a robust foundation for any Python application, balancing ease of use with flexibility and power.
