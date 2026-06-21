import os
from crypto_utils import encrypt_file, decrypt_file
from config import VAULT_DIR
from logger import log_event

def encrypt_to_vault():
    print("\n--- Encrypt to Vault ---")
    file_path = input("Enter full file path to encrypt: ").strip('"') # Remove quotes if user drags and drops
    
    if not os.path.exists(file_path):
        print("Error: File not found!")
        return

    filename = os.path.basename(file_path)
    output = os.path.join(VAULT_DIR, filename + ".enc")

    try:
        encrypt_file(file_path, output)
        log_event(f"Encrypted file: {filename}")
        print(f"Success! File encrypted and stored in vault as: {filename}.enc")
    except Exception as e:
        print(f"Error encrypting file: {e}")
        log_event(f"Encryption failed for {filename}: {e}")

def decrypt_from_vault():
    print("\n--- Decrypt from Vault ---")
    # List available files
    files = [f for f in os.listdir(VAULT_DIR) if f.endswith(".enc")]
    if not files:
        print("Vault is empty!")
        return

    print("Available files:")
    for f in files:
        print(f" - {f}")

    enc_file = input("Enter encrypted filename (with .enc): ")
    if enc_file not in files:
        print("Error: File not found in vault!")
        return

    output_name = input("Enter output filename (e.g. recovered.txt): ")
    output = os.path.join(os.getcwd(), output_name) # Save to current dir by default or use full path

    try:
        decrypt_file(os.path.join(VAULT_DIR, enc_file), output)
        log_event(f"Decrypted file: {enc_file}")
        print(f"Success! File decrypted to: {output}")
    except Exception as e:
        print(f"Error decrypting file: {e}")
        log_event(f"Decryption failed for {enc_file}: {e}")
