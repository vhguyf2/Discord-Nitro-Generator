
import requests
import string
import random
import time

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1530927391117938710/h3j7uhidpxm5TOWar71im6Jr7PxJqLCzG1l_AY2zFbWsL9kqJSo4RviENKZiBlMzGQ_o"

def generate_random_string(length):
    """Generate a random alphanumeric string of given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_request(code):
    """Send a request to the Discord API with the generated code."""
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    print(f"Time: {time.time()} - Request URL: {url}")  # Print the request timestamp and URL
    response = requests.get(url)
    print("Response content:", response.content.decode())  # Print the response content
    if response.status_code == 200:
        print(f"Request successful for code: {code}")
        send_to_discord(f"Request successful for code: {code}")
    elif response.status_code == 429:  # Handle rate limiting
        retry_after = response.json().get('retry_after', 0)  # Default to 0 seconds if retry_after is not provided
        print(f"Rate limited, retry after {retry_after} milliseconds")
        if retry_after:
            time.sleep(retry_after / 1000)  # Convert milliseconds to seconds
            send_request(code)  # Retry the request after waiting
        else:
            send_request(code)  # Retry the request immediately
    else:
        print(f"Request failed for code: {code}")

def send_to_discord(message):
    """Send a message to Discord webhook."""
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message sent to Discord")
    else:
        print("Failed to send message to Discord")

def generate_and_send():
    """Generate a random code and send a request."""
    code = generate_random_string(18)
    send_request(code)

if __name__ == "__main__":
    while True:
        generate_and_send()
        time.sleep(5)  # Adjust the interval between requests to 5 seconds
