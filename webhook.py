import os
import time
import json
from datetime import datetime

LOG_FILE_DIR = './'
LOG_FILE_FORMAT = '%y%m%d.log'
CONFIG_FILE = 'config.json'
DELAY = 5  # Check for new messages every 5 seconds. Adjust this value as needed.

def main():
    last_position = get_end_of_log_file()
    sent_lines = set()
    webhook_url = get_webhook_url()
    while True:
        try:
            log_file_path = get_current_log_file_path()
            with open(log_file_path, 'r') as log_file:
                log_file.seek(last_position)
                lines = log_file.readlines()
                if lines:
                    last_position = log_file.tell()
                    for line in lines:
                        line = line.strip()
                        if line not in sent_lines:
                            sent_lines.add(line)
                            message = line.split(None, 6)[-1] if len(line.split()) > 6 else line
                            send_message_to_discord(message, webhook_url)
                            print(f'Sent message: {message}')
                    
                # check if a new day has started and if so, reset the last_position and sent_lines
                if get_current_log_file_path() != log_file_path:
                    last_position = 0
                    sent_lines = set()

        except FileNotFoundError as e:
            print(f'Error: {e}. Check if the log file exists and has the correct format.')
        except Exception as e:
            print(f'Unexpected error: {e}')

        time.sleep(DELAY)

def get_current_log_file_path():
    current_date = datetime.now()
    log_file_name = current_date.strftime(LOG_FILE_FORMAT)
    log_file_path = os.path.join(LOG_FILE_DIR, log_file_name)
    return log_file_path

def get_end_of_log_file():
    log_file_path = get_current_log_file_path()
    try:
        with open(log_file_path, 'r') as log_file:
            log_file.seek(0, os.SEEK_END)
            return log_file.tell()
    except FileNotFoundError:
        return 0

def send_message_to_discord(message, webhook_url):
    data = {
        'embeds': [
            {
                'description': message,
                'color': 16777215  # You can change the color of the embed here.
            }
        ]
    }
    try:
        response = requests.post(webhook_url, json=data)

        if response.status_code != 204:
            print(f'Error sending message to Discord: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'Error sending message to Discord: {e}')

def get_webhook_url():
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data['webhook_url']
    except FileNotFoundError as e:
        print(f'Error: {e}. Check if the config file exists and has the correct format.')
        exit(1)
    except KeyError as e:
        print(f'Error: {e}. Check if the webhook_url key exists in the config file.')
        exit(1)

if __name__ == '__main__':
    try:
        import requests
    except ImportError:
        print('requests module not found. Installing it now...')
        os.system('pip install requests')
        import requests
    main()
