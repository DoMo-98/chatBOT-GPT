# Python Telegram Bot with OpenAI API and Audio Sending

This project is a Telegram bot built in Python, which connects to the OpenAI API. It works similar to ChatGPT, with the added feature of sending audios. It can be run in two ways: directly from a Python environment or through Docker.

## Requirements

- Python 3.11.4
- Docker (optional) https://docs.docker.com/engine/install/
- Telegram account and bot token
- OpenAI account and API key
- ffmpeg (if not using Docker)

If you don't have FFmpeg installed, you can do so by following these steps:

### On Debian/Ubuntu-based systems:

```
sudo apt update
sudo apt install ffmpeg
```

### On Red Hat/CentOS-based systems:

```
sudo yum install ffmpeg
```

### On macOS systems (using Homebrew):

```
brew install ffmpeg
```

### On Windows:

Installing FFmpeg on Windows can be a bit more complex, as Windows does not include a package manager like apt or yum. Instead, you will need to manually download the software from the official FFmpeg page (https://ffmpeg.org/download.html), extract the files, and add the path to your system's PATH.

### Installation Verification

To verify that FFmpeg installed correctly, you can run the following command in your terminal:

```
ffmpeg -version
```

You should see output indicating the version of FFmpeg you have installed.

Remember that these steps can vary depending on the specific operating system and its version. It's always a good idea to consult the official FFmpeg documentation for the most up-to-date installation instructions.

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/DoMo-98/privateBOT.git
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

1. **Python** - Run the `main.py` file:

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




