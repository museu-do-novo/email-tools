import requests
import re
import random
import logging
import argparse
import os
from time import sleep
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Configure logs
logging.basicConfig(
    filename='automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Faker for random data generation
from faker import Faker
faker = Faker()

def generate_password(length=8):
    """Generate a random alphanumeric password."""
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choices(chars, k=length))

def create_temp_email(domain="ehra.com"):
    """Create a temporary email using the temp-mail.io API."""
    name = faker.first_name().lower()
    url = 'https://api.internal.temp-mail.io/api/v3/email/new'
    data = {'name': name, 'domain': domain}
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        email = response.json().get('email')
        logging.info(f"Temporary email created: {email}")
        return email
    except requests.exceptions.RequestException as e:
        logging.error(f"Error creating email: {e}")
        print(Fore.RED + "Failed to create email." + Style.RESET_ALL)
        return None

def list_messages(email):
    """List messages received in the temporary email in a continuous loop."""
    url = f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages'
    print(Fore.CYAN + "\nWaiting for messages... (Press Ctrl + C to exit)\n" + Style.RESET_ALL)
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            messages = response.json()

            if messages:
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
                for msg in messages:
                    print(Fore.GREEN + f"Subject: {msg.get('subject', 'No subject')}" + Style.RESET_ALL)
                    print(Fore.YELLOW + f"Content: {msg.get('body_text', 'No content')}" + Style.RESET_ALL)
                    print("---")
            else:
                print(Fore.RED + "No messages found." + Style.RESET_ALL)
            sleep(10)  # Check for new messages every 10 seconds
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching messages: {e}")
            print(Fore.RED + "Failed to fetch messages." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.CYAN + "\nExiting..." + Style.RESET_ALL)
            break

def main():
    """Main function of the script."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen at the start
    print(Fore.BLUE + "=== Temporary Email Script ===" + Style.RESET_ALL)
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Script to create temporary emails and receive messages.")
    parser.add_argument('-c', '--create', action='store_true', help="Create a temporary email.")
    parser.add_argument('-l', '--list', metavar='EMAIL', help="List messages from a temporary email.")
    parser.add_argument('-d', '--domain', default="ehra.com", help="Set the domain for the temporary email.")
    parser.add_argument('-p', '--password-length', type=int, default=8, help="Set the length of the generated password.")
    args = parser.parse_args()

    # Create a temporary email
    if args.create:
        email = create_temp_email(args.domain)
        if not email:
            return

        # Generate a random password
        password = generate_password(args.password_length)
        print(Fore.GREEN + f"\nYour temporary email is: {email}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Generated password: {password}\n" + Style.RESET_ALL)

        # Start the message listing loop
        list_messages(email)

    # List messages from an existing email
    elif args.list:
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', args.list):
            print(Fore.RED + "Invalid email. Please provide a valid email address." + Style.RESET_ALL)
            return
        list_messages(args.list)

    # Show help if no arguments are provided
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
