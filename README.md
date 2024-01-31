# CLI Tool Documentation

This is a command-line interface (CLI) tool written in Python. It uses the OpenAI API to interact with GPT-3 models. The tool provides a way to have a conversation with the model, list available GPT agents, and perform a test command.

## Installation

Before you can use this tool, you need to install the required Python packages. You can do this by running the following command:

```bash
pip install openai typer python-dotenv toml json re
```

## Usage

### Conversation Command

To start a conversation with a GPT-3 model, use the `convo` command. The command takes several arguments and options:

```bash
python cli_tool.py convo [AGENT] [PROMPT] --agentfile [AGENTFILE] --sep0 [SEP0] --sep1 [SEP1] --sep2 [SEP2] --sep3 [SEP3] --sepl [SEPL]
```

- `AGENT`: The name of the GPT-3 model to use for the conversation.
- `PROMPT`: The initial prompt for the conversation.
- `--agentfile`: The path to the TOML file containing the agent configurations. Defaults to `agents.toml` in the same directory as the script.
- `--sep0` to `--sep3`: Custom separators for formatting the conversation output. Defaults to `* `, ` `, `─`, and `*` respectively.
- `--sepl`: The length of the separation line in the conversation output. Defaults to `80`.

### Agents Command

To list the available GPT-3 models, use the `agents` command:

```bash
python cli_tool.py agents --agents [AGENTS]
```

- `--agents`: The path to the TOML file containing the agent configurations. Defaults to `agents.toml` in the same directory as the script.

### Test Command

To perform a test command, use the `test` command:

```bash
python cli_tool.py test
```

## Environment Variables

The tool uses the `API_KEY` environment variable to authenticate with the OpenAI API. You can set this variable in a `.env` file in the same directory as the script.

## Note

This tool is a command-line interface for the OpenAI API. It does not provide a graphical user interface. All interactions with the tool happen in the terminal.
