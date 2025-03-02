---
sidebar_position: 1
---

# Unit Tests

## Testing Library

1. [Pytest](#1-pytest)
2. [Jest](#2-jest)
3. [VSCode Testing Suite](#3-vscode-testing-suite)

---

## 1. Pytest
Used for testing the Flask API
**Modules:**
- Pytest-cov
    - Generates test coverage reports in HTML format.
- Pytest-mock
    - Enables the creation of mock objects for simulating dependencies.

### Key Features
- Supports fixtures to set up test environments.
- Provides detailed test failure reports with traceback information.
- Enables parameterized tests for efficient testing of multiple scenarios.
- Generates test coverage reports with **pytest-cov** to track untested code.
- Supports mocking API calls and database interactions with **pytest-mock**.
### Why it was chosen
- Simple syntax and easy integration with Flask applications.
- Built-in support for fixtures, assertions, and test discovery.
- Comprehensive test coverage capabilities to ensure API stability.
- Widely used in Python testing frameworks.

### Running the unit tests

To run the unit tests for the Flask API:

#### Windows
```python
cd webserver
py -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
pytest tests -v  # -v for verbose output
coverage run -m pytest
coverage html  # Generates HTML coverage report
```
#### Mac/Linux
```python
cd webserver
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests -v  # -v for verbose output
coverage run -m pytest
coverage html  # Generates HTML coverage report
```

## 2. Jest
Used for unit testing core functionalities within the Visual Studio Code extension.

**Modules:**
- `jest` – The main testing framework that runs unit tests efficiently in a Node.js environment.
- `ts-jest` – Integrates Jest with TypeScript, enabling seamless testing of TypeScript code.

### Key features
- Built-in mocking capabilities for API calls and dependencies.
- Code coverage reports to monitor untested portions of the extension.
- Asynchronous test support for handling Promises and async functions.

### Why it was chosen
- Simple and intuitive API, making unit testing easy to write and maintain.
- Optimized for Node.js-based applications, aligning well with VS Code Extensions.
- Good mocking features for testing interactions with VS Code’s API without running a full VS Code instance.
- Fast execution compared to other testing frameworks, reducing development cycle time.

### Running the unit tests

To run the Jest tests:
```sh
cd extension
npm install
npx jest [name of test file]  # Run a specific test
npx jest --coverage  # Run all tests with coverage report
```

### Test Structure

- Each feature's methods will be encapsulated in a dedicated test file. For example:
    - `suggestions.test.ts` – Contains all related tests for fetching, modifying, and handling suggestions.
- Running a Specific Test File

```sh
npx jest suggestions.test.ts
```

## 3. VSCode Testing Suite
**Modules:**
- @vscode/test-cli – Provides command-line tools for running VS Code extension tests.
- @vscode/test-electron – Runs tests in an Electron environment, simulating VS Code’s runtime.

### Key Features
- Allows running integration tests in a real VS Code instance.
- Supports launching VS Code in a headless mode for automated testing.
- Provides API hooks to interact with the VS Code extension environment.
### Why it was chosen
- Preinstalled when creating VS Code extensions.
- Enables thorough testing of UI interactions and command execution.

### Running the unit tests

To run the VS Code extension tests:
```
cd extension
npm install
npm test
```

