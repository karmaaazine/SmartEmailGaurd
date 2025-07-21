#!/usr/bin/env python3
"""
SSL Certificate Generator for Email Security App
Generates self-signed SSL certificates for HTTPS development.
"""

import os
import ipaddress
from datetime import datetime, timedelta, timezone
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_ssl_certificate():
    """Generate a self-signed SSL certificate for development."""
    
    # Create SSL directory if it doesn't exist
    ssl_dir = "ssl"
    if not os.path.exists(ssl_dir):
        os.makedirs(ssl_dir)
    
    # Generate private key
    print("🔑 Generating private key...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Save private key
    private_key_path = os.path.join(ssl_dir, "private_key.pem")
    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Generate certificate
    print("📜 Generating SSL certificate...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Email Security App"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc)
    ).not_valid_after(
        datetime.now(timezone.utc) + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Save certificate
    cert_path = os.path.join(ssl_dir, "certificate.pem")
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print(f"✅ SSL certificate generated successfully!")
    print(f"📁 Certificate: {cert_path}")
    print(f"🔑 Private key: {private_key_path}")
    print(f"🌐 Valid for: localhost and 127.0.0.1")
    print(f"⏰ Expires: {cert.not_valid_after}")
    
    return cert_path, private_key_path

if __name__ == "__main__":
    generate_ssl_certificate() 