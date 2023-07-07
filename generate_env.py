""" This module requests certain tokens from the user and writes them to a new .env file """

import os

def main():
    """Requests the tokens from the user and generates the .env file."""
    # Names of the tokens required for this application
    tokens = ['OPENAI_API_KEY', 'TELEGRAM_BOT_TOKEN']

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Combine the directory with the .env filename
    env_path = os.path.join(script_dir, 'src/.env')

    with open(env_path, 'w', encoding="utf-8") as _f:
        for token in tokens:
            # Request each token from the user and write it to the .env file
            token_value = input(f'Please enter your {token}: ')
            _f.write(f'{token}={token_value}\n')

if __name__ == "__main__":
    main()
