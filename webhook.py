import os
import time
import requests
from datetime import datetime

LOG_FILE_DIR = './'
LOG_FILE_FORMAT = '%y%m%d.log'
WEBHOOK_URL = 'PUT YOUR WEBHOOK HERE'
DELAY = 5  # Check for new messages every 5 seconds. Adjust this value as needed.

def main():
    last_line = ''
    while True:
        try:
            log_file_path = get_current_log_file_path()
            with open(log_file_path, 'r') as log_file:
                lines = log_file.readlines()
                if lines and lines[-1] != last_line:
                    last_line = lines[-1]
                    message = last_line.strip().split(None, 6)[-1]
                    send_message_to_discord(message)
                    print(f'Sent message: {message}')

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

def send_message_to_discord(message):
    data = {
        'embeds': [
            {
                'description': message,
                'color': 16777215  # You can change the color of the embed here.
            }
        ]
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)

        if response.status_code != 204:
            print(f'Error sending message to Discord: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'Error sending message to Discord: {e}')

if __name__ == '__main__':
    main()