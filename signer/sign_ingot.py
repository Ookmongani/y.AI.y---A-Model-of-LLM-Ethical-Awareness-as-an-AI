#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
import base64

def generate_keypair(output_dir: Path):
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "private_key.pem").write_bytes(priv_pem)
    (output_dir / "public_key.pem").write_bytes(pub_pem)
    print(f"Keypair generated in {output_dir}")
    print("WARNING: Keep private_key.pem offline and secure!")

def sign_ingot(ingot_path: Path, private_key_path: Path, output_path: Path):
    with open(ingot_path, "r") as f:
        ingot_data = json.load(f)
    
    ingot_bytes = json.dumps(ingot_data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    
    signature = private_key.sign(ingot_bytes)
    
    signed_data = {
        "ingot": ingot_data,
        "signature": base64.b64encode(signature).decode("utf-8"),
        "signed": True
    }
    
    with open(output_path, "w") as f:
        json.dump(signed_data, f, indent=2, sort_keys=True)
    
    print(f"Signed ingot saved to {output_path}")

def verify_signature(signed_ingot_path: Path, public_key_path: Path):
    with open(signed_ingot_path, "r") as f:
        signed_data = json.load(f)
    
    ingot_bytes = json.dumps(signed_data["ingot"], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode("utf-8")
    signature = base64.b64decode(signed_data["signature"])
    
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    
    try:
        public_key.verify(signature, ingot_bytes)
        print("Signature verified successfully!")
        return True
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Ed25519 signer for ingots (offline use)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    gen_parser = subparsers.add_parser("generate", help="Generate keypair")
    gen_parser.add_argument("--output-dir", type=Path, default=Path("keys"), help="Output directory")
    
    sign_parser = subparsers.add_parser("sign", help="Sign an ingot")
    sign_parser.add_argument("ingot", type=Path, help="Path to unsigned ingot")
    sign_parser.add_argument("--key", type=Path, default=Path("keys/private_key.pem"), help="Private key path")
    sign_parser.add_argument("--output", type=Path, help="Output path for signed ingot")
    
    verify_parser = subparsers.add_parser("verify", help="Verify signed ingot")
    verify_parser.add_argument("signed_ingot", type=Path, help="Path to signed ingot")
    verify_parser.add_argument("--pubkey", type=Path, default=Path("keys/public_key.pem"), help="Public key path")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        generate_keypair(args.output_dir)
    elif args.command == "sign":
        output = args.output or args.ingot.with_name(args.ingot.stem + "_signed.json")
        sign_ingot(args.ingot, args.key, output)
    elif args.command == "verify":
        verify_signature(args.signed_ingot, args.pubkey)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
