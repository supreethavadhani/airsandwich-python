from datetime import datetime, timedelta
import hashlib
import os
from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    encrypted_otp = db.Column(db.String(255), nullable=True)
    otp_salt = db.Column(db.String(255), nullable=True)
    is_otp_verified = db.Column(db.Boolean, default=False)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_otp(self):
        """Generate and encrypt OTP."""
        otp = str(os.urandom(3).hex()[:6])
        salt = os.urandom(16).hex()
        hashed_otp = self.hash_otp(otp, salt)
        self.encrypted_otp = hashed_otp
        self.otp_salt = salt
        self.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        return otp  # Return plain OTP for now (should be sent via email)

    def verify_otp(self, otp):
        """Verify an OTP by comparing the hashed version."""
        if not self.encrypted_otp or not self.otp_salt or not self.otp_expiry:
            return False
        if datetime.utcnow() > self.otp_expiry:
            return False
        return self.hash_otp(otp, self.otp_salt) == self.encrypted_otp

    @staticmethod
    def hash_otp(otp, salt):
        """Hash the OTP with SHA-256 and salt."""
        return hashlib.sha256((otp + salt).encode()).hexdigest()
