#!/usr/bin/env python3
"""
Ed25519 Signer CLI - Offline cryptographic signing tool.

This tool performs Ed25519 signing operations in an offline-first manner.
Keys should be generated and stored securely, never transmitted.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import nacl.encoding
import nacl.signing

from yaiy.utils.canonical_json import canonicalize, parse_canonical


def generate_keypair(output_dir: Path) -> None:
    """
    Generate new Ed25519 keypair and save to files.
    
    Args:
        output_dir: Directory to save keys
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate keypair
    signing_key = nacl.signing.SigningKey.generate()
    verify_key = signing_key.verify_key
    
    # Save private key (with strong warning)
    private_key_path = output_dir / "private.key"
    with open(private_key_path, 'wb') as f:
        f.write(signing_key.encode())
    private_key_path.chmod(0o600)  # Read/write for owner only
    
    # Save public key
    public_key_path = output_dir / "public.key"
    with open(public_key_path, 'wb') as f:
        f.write(verify_key.encode())
    
    print(f"✓ Keypair generated successfully")
    print(f"  Private key: {private_key_path} (KEEP SECURE!)")
    print(f"  Public key:  {public_key_path}")
    print(f"  Public key (hex): {verify_key.encode(encoder=nacl.encoding.HexEncoder).decode()}")


def sign_data(private_key_path: Path, data_path: Optional[Path] = None) -> None:
    """
    Sign data with Ed25519 private key.
    
    Args:
        private_key_path: Path to private key file
        data_path: Path to data file (or stdin if None)
    """
    # Load private key
    with open(private_key_path, 'rb') as f:
        signing_key = nacl.signing.SigningKey(f.read())
    
    # Read data
    if data_path:
        with open(data_path, 'r') as f:
            data = f.read()
    else:
        data = sys.stdin.read()
    
    # Parse and canonicalize JSON
    try:
        obj = json.loads(data)
        canonical = canonicalize(obj)
    except json.JSONDecodeError:
        # If not JSON, use raw data
        canonical = data
    
    # Sign
    signed = signing_key.sign(canonical.encode('utf-8'))
    signature_hex = signed.signature.hex()
    
    # Output signed payload
    result = {
        "data": obj if isinstance(obj, dict) else canonical,
        "signature": signature_hex,
        "public_key": signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode()
    }
    
    print(canonicalize(result))


def verify_signature(public_key_hex: str, signature_hex: str, data_path: Optional[Path] = None) -> None:
    """
    Verify Ed25519 signature.
    
    Args:
        public_key_hex: Public key in hex format
        signature_hex: Signature in hex format
        data_path: Path to data file (or stdin if None)
    """
    # Load public key
    verify_key = nacl.signing.VerifyKey(public_key_hex, encoder=nacl.encoding.HexEncoder)
    
    # Read data
    if data_path:
        with open(data_path, 'r') as f:
            data = f.read()
    else:
        data = sys.stdin.read()
    
    # Parse and canonicalize JSON
    try:
        obj = json.loads(data)
        canonical = canonicalize(obj)
    except json.JSONDecodeError:
        canonical = data
    
    # Verify
    try:
        signature = bytes.fromhex(signature_hex)
        verify_key.verify(canonical.encode('utf-8'), signature)
        print("✓ Signature valid")
        return True
    except nacl.exceptions.BadSignatureError:
        print("✗ Signature invalid", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ed25519 Signer - Offline cryptographic signing",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate new keypair')
    gen_parser.add_argument(
        '--output-dir', '-o',
        type=Path,
        default=Path('./keys'),
        help='Output directory for keys (default: ./keys)'
    )
    
    # Sign command
    sign_parser = subparsers.add_parser('sign', help='Sign data')
    sign_parser.add_argument(
        '--private-key', '-k',
        type=Path,
        required=True,
        help='Path to private key file'
    )
    sign_parser.add_argument(
        '--data', '-d',
        type=Path,
        help='Path to data file (default: stdin)'
    )
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify signature')
    verify_parser.add_argument(
        '--public-key', '-p',
        required=True,
        help='Public key (hex)'
    )
    verify_parser.add_argument(
        '--signature', '-s',
        required=True,
        help='Signature (hex)'
    )
    verify_parser.add_argument(
        '--data', '-d',
        type=Path,
        help='Path to data file (default: stdin)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'generate':
        generate_keypair(args.output_dir)
    elif args.command == 'sign':
        sign_data(args.private_key, args.data)
    elif args.command == 'verify':
        verify_signature(args.public_key, args.signature, args.data)


if __name__ == '__main__':
    main()
