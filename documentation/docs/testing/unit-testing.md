---
sidebar_position: 1
---

# Library Explanation
## Pytest
Used for testing the Flask API
**Modules:**
- Pytest-cov
    - Creates html coverage documentation
- Pytest-mock
    - Allows for creating mock objects

### Key Features

### Why it was chosen

## Jest
Used for testing the Visual Studio Code extension

### Key features

### Why it was chosen

## Visual Studio Code Testing Suite
**Modules:**
- test-cli"
- test-electron

# Running the unit tests
## Flask API
Commands to run
```
cd webserver
# Windows
py -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
pytest tests -v # -v for verbose output
coverage run
coverage html
# Mac
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests -v # -v for verbose output
coverage run
coverage html
```
## Visual Studio Code Extension
Commands to run
```
cd extension
npm install
npx jest [name of test file]
```

