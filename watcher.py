import time
from datetime import datetime, timedelta
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from twilio.rest import Client
import re
import urllib.parse

class LogHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_processed_time = datetime.now()- timedelta(days=1)

    def on_modified(self, event):
        if event.src_path == "/var/log/nginx/pixel-access.log":
            current_time = datetime.now()

            if current_time - self.last_processed_time > timedelta(seconds=3):
                print("Log file changed, checking for new access...")
                try:
                    with open(event.src_path, 'r') as file:
                        lines = file.readlines()
                        last_line = lines[-1]
                        self.process_log_entry(last_line)
                    self.last_processed_time = current_time
                except Exception as e:
                    print(f"Failed to read or process log file: {e}")

            else:
                    print("Change ignored, within the cooldown period.")


    def process_log_entry(self, log_entry):
        match = re.search(r'"GET /tracking-pixel\?(.+) HTTP', log_entry)
        if match:
            query_string = match.group(1)
            params = urllib.parse.parse_qs(query_string)
            email = params.get('email', [''])[0]
            campaign = params.get('campaign', [''])[0]
            email = urllib.parse.unquote(email)
            campaign = urllib.parse.unquote(campaign)
            send_sms(email, campaign)

def send_sms(email, campaign):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_ACCOUNT_AUTH')
    client = Client(account_sid, auth_token)
    body = f"Tracking pixel was just accessed. Email: {email}, Campaign: {campaign}"
    message = client.messages.create(
        to="+",  # Your phone number
        from_="+",  # Your Twilio number
        body=body
    )
    print(f"Message sent with ID: {message.sid}")

def main():
    path = "/var/log/nginx"
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()

