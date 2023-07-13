# chatBOT-GPT

This project is a Python-based Telegram bot integrated with the OpenAI API, operating similar to ChatGPT, and offers additional audio sending features. It can be executed in a Python environment or within a Docker container for added flexibility.

![chatBOT-GPT demo](./docs/chatBOT-GPT.gif)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11.4 installed. You can download it from [here](https://www.python.org/downloads/).
- Docker (optional). If you want to use Docker, install it from [here](https://docs.docker.com/engine/install/).
- A Telegram account along with a bot token. Follow [this guide](https://core.telegram.org/bots#creating-a-new-bot) to create a new bot if you don't have one already.
- An OpenAI account and API key. You can create an account [here](https://www.openai.com/).
- `ffmpeg` installed on your machine if you are not using Docker. For installation instructions, refer to the [official guide](https://ffmpeg.org/download.html) based on your OS.

## Installation

Follow these steps to get the bot up and running:

1. Clone this repository to your local machine:

```bash
git clone https://github.com/DoMo-98/chatBOT-GPT.git
```

2. Navigate to the project directory:

```bash
cd chatBOT-GPT
```

3. If you're not using Docker, install the necessary Python dependencies:

```bash
pip install -r requirements.txt
```

4. For non-Docker users, ensure `ffmpeg` is installed on your system.

## Configuration

To set up your API keys and bot tokens, execute the `generate_env.py` script. This script will prompt you to input your OpenAI and Telegram credentials.

```bash
python3 generate_env.py
```

## Running the Bot

There are two ways to start the bot:

1. **Python** - Run the `src.main` module:

```bash
python3 -m src.main
```

2. **Docker Compose** - Start the service with Docker Compose:

```bash
docker-compose up
```

Both methods will initiate the bot, and it will start listening for incoming messages.


## Using the Bot

The bot recognizes several commands to help you interact with it. Here are the available commands:

1. **/start** - Initialize the bot. The bot will reply with: "Hello! I'm an assistant bot. I can answer all your text and voice messages."

2. **/text** - Switch the bot to text mode. The bot will respond with text messages only, and will confirm with: "I will now send text messages."

3. **/audio** - Switch the bot to audio mode. The bot will send audio messages, and will confirm with: "I will now send voice messages."

4. **/new** - Start a new chat. The bot will clear the message history and reply with: "New chat!"

5. **/gpt3** - Switch the bot to use GPT-3.5-Turbo. The bot will confirm with: "I will now use GPT-3.5-Turbo."

6. **/gpt4** - Switch the bot to use GPT-4. The bot will confirm with: "I will now use GPT-4."

To use these commands, simply type them in the chat with the bot on Telegram.

## Contributing

Your contributions are welcome and appreciated. Before proposing a contribution, please open an issue to discuss your proposed changes. Remember to update or add tests as appropriate.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
