from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import os
import shutil
from auth import register_user_core, save_user, verify_login, USER_FILE
from crypto_utils import generate_key, encrypt_file, decrypt_file
from config import VAULT_DIR, DATA_DIR, KEY_FILE
import qrcode
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24) # Secure secret key for sessions

# Ensure Vault Root Exists
os.makedirs(VAULT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(KEY_FILE):
    generate_key()

def get_user_vault():
    if 'username' not in session:
        return None
    user_vault = os.path.join(VAULT_DIR, session['username'])
    os.makedirs(user_vault, exist_ok=True)
    return user_vault

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username') # Get username
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and Password are required', 'error')
            return redirect(url_for('register'))
            
        # Check if user exists (Simple check)
        if os.path.exists(USER_FILE):
            try:
                with open(USER_FILE, "r") as f:
                    data = json.load(f)
                    if "users" in data and username in data["users"]:
                         flash('Username already taken.', 'error')
                         return redirect(url_for('register'))
            except:
                pass
        
        # Determine QR path for web display (Unique per user to avoid collision/caching issues ideally, but generic ok for now)
        qr_filename = 'qr_code.png' 
        qr_path = os.path.join(app.static_folder, qr_filename)
        
        hashed, otp_secret, uri = register_user_core(password)
        
        # Save QR code
        img = qrcode.make(uri)
        img.save(qr_path)
        
        save_user(username, hashed, otp_secret) # Pass username
        
        return render_template('register.html', qr_uri=qr_filename)
    
    return render_template('register.html', qr_uri=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        otp = request.form.get('otp')
        
        success, message = verify_login(username, password, otp) # Pass username
        
        if success:
            session['logged_in'] = True
            session['username'] = username # Store username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(message, 'error')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    user_vault = get_user_vault()
    files = [f for f in os.listdir(user_vault) if f.endswith('.enc')]
    return render_template('dashboard.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('dashboard'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('dashboard'))
    
    if file:
        filename = file.filename
        temp_path = os.path.join(DATA_DIR, 'temp_' + filename)
        file.save(temp_path)
        
        try:
            user_vault = get_user_vault()
            output_path = os.path.join(user_vault, filename + ".enc")
            encrypt_file(temp_path, output_path)
            flash(f'File {filename} encrypted successfully!', 'success')
        except Exception as e:
            flash(f'Encryption failed: {str(e)}', 'error')
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    return redirect(url_for('dashboard'))

@app.route('/decrypt/<filename>')
def decrypt(filename):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    user_vault = get_user_vault()
    encrypted_path = os.path.join(user_vault, filename)
    
    if not os.path.exists(encrypted_path):
        flash('File not found', 'error')
        return redirect(url_for('dashboard'))
    
    # Decrypt to a unique temp file for download
    if filename.endswith('.enc'):
        original_name = filename[:-4]
    else:
        original_name = filename # Should not happen based on filters but safe fallback
        
    unique_temp = f"dec_{uuid.uuid4()}_{original_name}"
    decrypted_path = os.path.join(DATA_DIR, unique_temp)
    
    try:
        decrypt_file(encrypted_path, decrypted_path)
        return send_file(decrypted_path, as_attachment=True, download_name=original_name)
    except Exception as e:
        flash(f'Decryption failed: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/download_encrypted/<filename>')
def download_encrypted(filename):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    user_vault = get_user_vault()
    encrypted_path = os.path.join(user_vault, filename)
    if not os.path.exists(encrypted_path):
        flash('File not found', 'error')
        return redirect(url_for('dashboard'))
        
    return send_file(encrypted_path, as_attachment=True, download_name=filename)

@app.route('/local_encrypt', methods=['POST'])
def local_encrypt():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        
    filepath = request.form.get('filepath')
    if not filepath or not os.path.exists(filepath):
        flash('File path invalid or not found', 'error')
        return redirect(url_for('dashboard'))
        
    try:
        # Backup to User's Vault first
        user_vault = get_user_vault()
        filename = os.path.basename(filepath)
        vault_path = os.path.join(user_vault, filename + ".enc")
        encrypt_file(filepath, vault_path)
        
        # Then encrypt in-place
        output_path = filepath + ".enc"
        encrypt_file(filepath, output_path)
        os.remove(filepath) 
        
        flash(f'File encrypted in-place AND saved to Vault: {output_path}', 'success')
    except Exception as e:
        flash(f'Local encryption failed: {str(e)}', 'error')
        
    return redirect(url_for('dashboard'))

@app.route('/local_decrypt', methods=['POST'])
def local_decrypt():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        
    filepath = request.form.get('filepath')
    if not filepath or not os.path.exists(filepath) or not filepath.endswith('.enc'):
        flash('Invalid encrypted file path', 'error')
        return redirect(url_for('dashboard'))
        
    try:
        output_path = filepath[:-4] 
        decrypt_file(filepath, output_path)
        os.remove(filepath) 
        flash(f'File decrypted in-place: {output_path}', 'success')
    except Exception as e:
        flash(f'Local decryption failed: {str(e)}', 'error')
        
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
