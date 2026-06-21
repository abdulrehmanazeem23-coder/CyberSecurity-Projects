import os
import sys
from auth import register_user, authenticate_user
from crypto_utils import generate_key
from vault import encrypt_to_vault, decrypt_from_vault
from config import USER_FILE, KEY_FILE, VAULT_DIR, DATA_DIR

def first_time_setup():
    os.makedirs(VAULT_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DATA_DIR), exist_ok=True) # Ensure data dir parent exists if needed

    if not os.path.exists(KEY_FILE):
        generate_key()
    
    # Check if user exists
    if not os.path.exists(USER_FILE):
        print("No user found. Starting registration...")
        register_user()

def menu():
    while True:
        print("\n=== Secure File Vault ===")
        print("1. Encrypt File to Vault")
        print("2. Decrypt File from Vault")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            encrypt_to_vault()
        elif choice == "2":
            decrypt_from_vault()
        elif choice == "3":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    print("Welcome to Secure File Vault")
    first_time_setup()
    
    # Authenticate before showing menu
    if authenticate_user():
        menu()
    else:
        print("Authentication failed. Exiting.")
