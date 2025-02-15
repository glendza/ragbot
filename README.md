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

### Running the project

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
uv pip install -e .[dev,discord]

# ...or, if you don't want dev packages:
uv pip install .[discord]
```

Optional dependencies:

- `dev` - Include development packages for linting, formatting etc., which are otherwise not needed for running the app;
- `discord` - Include packages necessary for [`Discord`](https://discord.com/) integration

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

### Setting up the Discord bot

1. Create a new application [here](https://discord.com/developers/applications).
2. Navigate to your application and acquire the `APPLICATION ID`.
3. Go to `https://discord.com/developers/applications/<APPLICATION ID>/bot`, then:
   - Name your bot.
   - Ensure **"Message Content Intent"** is enabled.
   - Click **"Reset Token"**, copy the token, and store it in your `.env` file as:
     ```
     RAGBOT__DISCORD__TOKEN=<YOUR_BOT_TOKEN>
     ```
4. Add the bot to your server by visiting:
   ```
   https://discord.com/oauth2/authorize?client_id=<APPLICATION ID>&scope=bot&permissions=563484677372992
   ```
