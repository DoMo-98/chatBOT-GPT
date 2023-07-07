# Python Telegram Bot with OpenAI API and Audio Sending

This project is a Telegram bot built in Python, which connects to the OpenAI API. It works similar to ChatGPT, with the added feature of sending audios. It can be run in two ways: directly from a Python environment or through Docker.

## Requirements

- Python 3.11.4
- Docker (optional) https://docs.docker.com/engine/install/
- Telegram account and bot token
- OpenAI account and API key
- ffmpeg (if not using Docker)

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/your-repository.git
```

2. Navigate to the project directory:

```bash
cd your-repository
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. If you're not using Docker, you'll also need to install ffmpeg on your machine. The installation process may vary depending on your operating system.

## Configuration

To set up your tokens and API keys, you need to run the `generate_env.py` script. This script will ask you to input your OpenAI and Telegram credentials.

```bash
python3 generate_env.py
```

## Execution

You can start the application in two ways:

1. **Direct Python** - Run the `main.py` file:

```bash
python3 main.py
```

2. **Docker Compose** - Bring up the service with Docker Compose:

```bash
docker-compose up
```

Both methods will start the application and begin listening for messages sent to the Telegram bot.

## Contributing

Contributions are welcome. To do so, please open an issue first to discuss what you would like to change. Be sure to update tests as appropriate.

## License

See the [LICENSE](LICENSE) file for more details.
