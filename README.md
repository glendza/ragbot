# ragbot

Example of a chatbot specialized in a subject.

## Project Goals

This project aims to create an AI bot specialized in a domain of choice (e.g., energy, medicine, mathematics, movies, music, programming, etc.). The bot will respond to user queries related to its specialized domain through various communication interfaces.

### Requirements

1. **Bot Specialization**
   - Implement domain specialization using retrieval-augmented generation
   - Support for domain-specific knowledge ingestion

2. **Prompt Engineering**
   - Define bot's domain expertise boundaries
   - Implement domain scope controls

3. **Application Architecture**
   - Core components:
     - Communication interface adapters
     - Knowledge retrieval system
     - Conversation engine
     - State persistence layer
     - Core orchestration component
   - Support for multiple communication backends
   - Thread-based conversation management

4. **Scalability**
   - Support for concurrent users
   - Asynchronous request handling

## Project setup

Python project is bootstrapped using [`uv`](https://github.com/astral-sh/uv).

Project is initialized with:

```sh
uv init --package --build-backend hatchling
```

To set up the project locally:

```sh
# Create virtual environment:
uv venv

# Activate virtual environment:
source .venv/bin/activate

# Install the package and it's dependencies in development mode:
uv pip install -e .[dev]

# ...or, if you don't want dev packages:
uv pip install .
```

To run the project:

```sh
# Using uv:
uv run -m ragbot

# Using Python:
python -m ragbot

# Using scripts:
ragbot
```

Some useful `uv` commands:

```sh
# To add a Python package:
uv add package-name

# To remove a Python package:
uv remove package-name

# To update a Python package:
uv lock --upgrade-package package-name
```
