import os

BASE_DIR = os.getcwd()

VAULT_DIR = os.path.join(BASE_DIR, "vault_files")
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_FILE = os.path.join(BASE_DIR, "logs", "activity.log")

USER_FILE = os.path.join(DATA_DIR, "user.json")
KEY_FILE = os.path.join(DATA_DIR, "key.bin")
