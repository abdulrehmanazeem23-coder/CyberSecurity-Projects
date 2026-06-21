from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()

    # Helper to add a slide with title and content
    def add_slide(title_text, content_text_list):
        slide_layout = prs.slide_layouts[1] # Title and Content
        slide = prs.slides.add_slide(slide_layout)
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = title_text
        
        # Format content
        tf = content.text_frame
        tf.clear() # Clear default
        
        for item in content_text_list:
            p = tf.add_paragraph()
            p.text = item
            p.level = 0
            if isinstance(item, tuple): # Handle sub-bullets if needed (simple implementation here)
                p.text = item[0]

    # --- Slide 1: Title ---
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Secure File Vault"
    subtitle.text = "Advanced Web-Based Encryption System with MFA\n\nPresented by: [Your Name]"

    # --- Slide 2: Introduction ---
    add_slide("Introduction", [
        "A secure file storage solution designed to protect sensitive data from unauthorized access.",
        "Combines military-grade AES-256 encryption with a modern, user-friendly web interface.",
        "Ensures data confidentiality, integrity, and availability.",
        "Key Differentiator: Multi-Factor Authentication (MFA) integration."
    ])

    # --- Slide 3: Business Scope ---
    add_slide("Business Scope", [
        "Target Audience: Enterprises, Legal Firms, Healthcare Providers, and Privacy-Conscious Individuals.",
        "Compliance: Assists in meeting GDPR, HIPAA, and CCPA data protection requirements.",
        "Scalability: Multi-user architecture supports team deployment.",
        "Use Case: Protecting intellectual property, financial records, and personal identification documents."
    ])

    # --- Slide 4: Objectives ---
    add_slide("Objectives", [
        "1. Secure Storage: Encrypt files using AES-256 (Advanced Encryption Standard).",
        "2. Access Control: Implement robust Multi-Factor Authentication (Password + 2FA OTP).",
        "3. User Isolation: Ensure strict data separation between multiple users.",
        "4. Usability: Provide a seamless web dashboard for file management and local in-place encryption."
    ])

    # --- Slide 5: Security Challenges / Risks ---
    add_slide("Security Challenges & Risks", [
        "Problem Statement:",
        "• Data Breaches: Unencrypted data is easily readable if stolen.",
        "• Weak Passwords: 81% of breaches utilize stolen or weak passwords.",
        "• Insider Threats: Lack of isolation allows users to access others' private data.",
        "• Ransomware: Local files are vulnerable to modification by malware."
    ])

    # --- Slide 6: Proposed Solution (Overview & Implementation) ---
    add_slide("Proposed Solution", [
        "Overview: A Flask-based Web Vault with end-to-end security measures.",
        "Implementation Details:",
        "• Encryption Engine: AES-256 in CBC mode with secure key management.",
        "• Authentication: Bcrypt for password hashing + Time-based OTP (Google Authenticator).",
        "• Architecture: Multi-User Segregation (Private implementations of vault paths).",
        "• Resilience: Automated backup to Vault before performing local in-place encryption."
    ])

    # --- Slide 7: Tools & Technologies ---
    add_slide("Tools & Technologies", [
        "Backend Framework: Python Flask",
        "Cryptography: 'cryptography' library (AES), 'bcrypt'",
        "Authentication: 'pyotp' (TOTP generation/validation)",
        "Frontend: HTML5, CSS3 (Custom Glassmorphism Design)",
        "Data Storage: JSON (User Metadata), File System (Encrypted Blobs)"
    ])

    # --- Slide 8: Conclusion ---
    add_slide("Conclusion", [
        "The Secure File Vault successfully addresses critical security gaps in local file storage.",
        "By enforcing 2FA and Strong Encryption, it mitigates risk of data theft.",
        "The project delivers a professional, scalable, and compliant security tool.",
        "Future enhancements could include Cloud Sync and Enterprise SSO (Single Sign-On).",
        "",
        "Thank You!"
    ])

    prs.save('SecureFileVault_Presentation.pptx')
    print("Presentation created successfully!")

if __name__ == "__main__":
    create_presentation()
