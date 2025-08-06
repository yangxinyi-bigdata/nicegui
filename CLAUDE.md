# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NiceGUI is a Python-based UI framework that creates web-based user interfaces which run in the browser. It follows a backend-first philosophy where all user interactions are sent to the backend and invoke Python functions. The framework is built on FastAPI, Vue.js/Quasar for the frontend, and uses socket.io for real-time communication.

## Development Commands

### Running the Application
- **Development mode**: `poetry run python main.py` (starts on localhost:8080 with auto-reload)
- **Run with specific host/port**: `poetry run python main.py --host 0.0.0.0 --port 8080`

### Testing
- **Run all tests**: `poetry run pytest`
- **Run single test**: `poetry run pytest tests/test_specific_file.py`
- **Run with coverage**: `poetry run pytest --cov=nicegui`
- **Run tests with watcher**: `poetry run pytest-watcher`

### Code Quality
- **Linting**: `poetry run ruff check nicegui/ tests/`
- **Auto-fix linting**: `poetry run ruff check --fix nicegui/ tests/`
- **Type checking**: `poetry run mypy nicegui/`
- **Auto-format**: `poetry run autopep8 --in-place --recursive nicegui/`
- **Sort imports**: `poetry run isort nicegui/`

### Build and Packaging
- **Pack for distribution**: `poetry run nicegui-pack`
- **Build Docker image**: `docker build -t nicegui .`

## Architecture Overview

### Core Components
- **Element System**: All UI components inherit from `Element` class in `nicegui/element.py`
- **Client Management**: `nicegui/client.py` handles browser connections and state
- **Application Core**: `nicegui/app/app.py` manages the FastAPI application lifecycle
- **UI Interface**: `nicegui/ui.py` provides the main user interface API
- **Event System**: `nicegui/events.py` handles user interactions and callbacks

### Key Design Patterns
- **Element Composition**: All UI components are composable elements that can be nested
- **Slot System**: Uses slots for content distribution and layout
- **Binding System**: Reactive data binding between Python state and UI elements
- **Async Communication**: Uses socket.io for real-time frontend-backend communication
- **Single Worker**: Only uses one uvicorn worker to avoid synchronization complexity

### Directory Structure
- **`nicegui/`**: Core library code
  - **`elements/`**: UI element implementations
  - **`functions/`**: UI utility functions
  - **`testing/`**: Testing framework and utilities
  - **`static/`**: Static assets (JS, CSS, fonts)
  - **`templates/`**: HTML templates
- **`tests/`**: Comprehensive test suite
- **`examples/`**: Usage examples and demos
- **`website/`**: Documentation site (built with NiceGUI itself)

## Development Guidelines

### Code Style
- Follow existing code patterns and conventions
- Use single quotes for strings, double quotes for docstrings
- Maximum line length: 120 characters
- Use type hints consistently
- Follow the existing element pattern when creating new UI components

### Testing Approach
- Tests use pytest with Selenium for browser automation
- Test files are in `tests/` directory with `test_` prefix
- Use the testing framework in `nicegui/testing/` for UI tests
- Tests can simulate user interactions and verify UI state

### Element Development
- All UI elements inherit from the base `Element` class
- Elements are defined in `nicegui/elements/` directory
- Use mixins for shared functionality (see `nicegui/elements/mixins/`)
- Elements automatically register their Vue components and dependencies

### Frontend-Backend Communication
- All user interactions trigger Python callbacks
- Use socket.io for real-time updates
- Avoid frontend state management - keep state in Python
- Use the `run_javascript` function for direct DOM manipulation when needed

## Configuration

### Environment Variables
- `NICEGUI_RELOAD`: Enable/disable auto-reload (default: true)
- `NICEGUI_HOST`: Default host binding
- `NICEGUI_PORT`: Default port
- `NICEGUI_STORAGE**: Storage backend (memory, file, redis)

### Optional Dependencies
- **Native mode**: `poetry install --extras native` (for desktop applications)
- **Plotly**: `poetry install --extras plotly` (for charting)
- **Matplotlib**: `poetry install --extras matplotlib` (for plotting)
- **Redis**: `poetry install --extras redis` (for distributed storage)

## Common Development Tasks

### Adding New UI Elements
1. Create element class in `nicegui/elements/` inheriting from `Element`
2. Define Vue component and register it
3. Add element to `nicegui/ui.py` exports
4. Create corresponding documentation in `website/documentation/content/`
5. Add tests in `tests/`

### Debugging
- Use `ui.log()` for debugging output
- Enable debug logging: `import logging; logging.basicConfig(level=logging.DEBUG)`
- Use browser dev tools to inspect frontend communication
- Check the browser console for JavaScript errors

### Performance Considerations
- Minimize DOM updates by using batch operations
- Use `ui.refreshable` for expensive recomputations
- Be careful with timer frequency to avoid overwhelming the browser
- Use efficient data structures for large datasets