import bcrypt
import json
import pyotp
import qrcode
import os # Added os import
from config import USER_FILE
from logger import log_event

# --- Core Logic ---

def register_user_core(password_str):
    password = password_str.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    otp_secret = pyotp.random_base32()
    totp = pyotp.TOTP(otp_secret)

    uri = totp.provisioning_uri(name="SecureFileVault", issuer_name="IS Project")
    
    # Return data needed for UI (secret) and storage
    return hashed.decode(), otp_secret, uri

def save_user(username, hashed_password, otp_secret):
    # Load existing data
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                data = json.load(f)
        except:
            data = {"users": {}}
    else:
        data = {"users": {}}

    # Initialize users dict if legacy format or empty
    if "users" not in data:
        data = {"users": {}}

    data["users"][username] = {
        "password": hashed_password,
        "otp_secret": otp_secret
    }

    with open(USER_FILE, "w") as f:
        json.dump(data, f)
    log_event(f"User registered: {username}")

def verify_login(username, password_input, otp_input):
    try:
        with open(USER_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return False, "No users registered."

    if "users" not in data or username not in data["users"]:
        return False, "User not found."

    user = data["users"][username]

    if not bcrypt.checkpw(password_input.encode(), user["password"].encode()):
        log_event(f"Wrong password attempt for {username}")
        return False, "Invalid password."

    totp = pyotp.TOTP(user["otp_secret"])
    if not totp.verify(otp_input):
        log_event(f"Wrong OTP attempt for {username}")
        return False, "Invalid OTP."

    log_event(f"User authenticated successfully: {username}")
    return True, "Success"

# --- CLI Wrappers (Refactored) ---

def register_user():
    print("\n=== User Registration ===")
    password = input("Create Password: ")
    
    hashed, otp_secret, uri = register_user_core(password)
    
    img = qrcode.make(uri)
    img.save("otp_qr.png")
    
    save_user(hashed, otp_secret)

    print("\nScan otp_qr.png using Google Authenticator")
    print("Registration Successful!")

def authenticate_user():
    print("\n=== User Authentication ===")
    
    # Check if user exists first to match original flow
    if not os.path.exists(USER_FILE):
         print("No user registered! Please run the program again to register.")
         return False

    password = input("Enter Password: ")
    otp = input("Enter OTP from Authenticator App: ")
    
    success, message = verify_login(password, otp)
    
    if not success:
        print(message)
        return False

    print("Authentication Successful!")
    return True
