import requests
import string
import random
import time
import os
import sys
import json
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Constants
RANDOM_STRING_LENGTH = 5
WAIT_TIME_SUCCESS = 3
WAIT_TIME_FAILURE = 25

# Function to generate a random string
def generate_random_string(length):
    return "s" + "".join(random.choices(string.ascii_lowercase, k=length))

# Function to send URL to Discord webhook
def send_url_to_discord(url):
    payload = {"content": f"Sent to URL: {url}"}
    response = requests.post(discord_webhook_url, data=payload)
    return response

# Load configuration from config.json
with open("config.json", "r") as file:
    config = json.load(file)
    discord_webhook_url = config["discord_webhook_url"]

# Start the Flask server to keep the script alive
keep_alive()

# Continuously generate and send random URLs to Discord webhook
try:
    while True:
        # Generate a random string of 5 lowercase characters
        random_suffix = generate_random_string(RANDOM_STRING_LENGTH)

        # Get the URL of the subdirectory
        url = "https://prnt.sc/" + random_suffix

        # Print the current random string being tested
        print(f"Testing {random_suffix}...")

        # Send the URL to the Discord webhook
        response = send_url_to_discord(url)

        # Check if the response was successful
        if response.ok:
            print(f"Sent to URL: {url}")
        else:
            print(f"Failed to send URL: {url}")

        # Sleep for 3 seconds before generating the next URL
        time.sleep(WAIT_TIME_SUCCESS)

except KeyboardInterrupt:
    print("Script interrupted manually. Exiting...")
    sys.exit(0)
except Exception as e:
    # Print any exceptions that occur
    print(f"Exception occurred: {e}")

    # Wait for 25 seconds before restarting the loop
    time.sleep(WAIT_TIME_FAILURE)

    # Restart the script
    python = sys.executable
    os.execl(python, python, *sys.argv)
