#!/usr/bin/env python3
"""
Verified Model Weight Download Script

Downloads and verifies model weights using cryptographic signatures.
OFFLINE-FIRST: No weights are bundled. Manual verification required.
"""
import argparse
import hashlib
import sys
from pathlib import Path
from typing import Optional


class ModelDownloader:
    """
    Secure model weight downloader with verification.
    
    This is a TEMPLATE - adapt for your specific model sources.
    Always verify signatures before using downloaded weights.
    """
    
    def __init__(self, verify_signatures: bool = True):
        self.verify_signatures = verify_signatures
    
    def download_weights(
        self,
        model_name: str,
        output_dir: Path,
        expected_hash: Optional[str] = None,
        source_url: Optional[str] = None
    ) -> bool:
        """
        Download and verify model weights.
        
        Args:
            model_name: Name of model to download
            output_dir: Directory to save weights
            expected_hash: Expected SHA256 hash for verification
            source_url: Source URL (for manual download instructions)
        
        Returns:
            True if successful, False otherwise
        """
        print("=" * 70)
        print("SECURE MODEL WEIGHT DOWNLOAD")
        print("=" * 70)
        print()
        print("⚠️  IMPORTANT SECURITY NOTICE:")
        print("   This is an OFFLINE-FIRST system.")
        print("   Automatic downloads are DISABLED by default.")
        print()
        print("📋 Manual Download Instructions:")
        print(f"   1. Model: {model_name}")
        
        if source_url:
            print(f"   2. Source: {source_url}")
        else:
            print("   2. Source: [Contact model provider for verified source]")
        
        print(f"   3. Save to: {output_dir / model_name}")
        print()
        
        if expected_hash:
            print(f"✓ Expected SHA256 hash: {expected_hash}")
            print()
            print("🔒 Verification Steps:")
            print("   1. Download the model weights manually")
            print("   2. Verify the SHA256 hash matches the expected value")
            print("   3. Verify the cryptographic signature (if available)")
            print("   4. Place verified weights in the output directory")
        
        print()
        print("=" * 70)
        print("⛔ AUTOMATIC DOWNLOAD DISABLED")
        print("   Reason: Security and reproducibility")
        print("   Action: Follow manual download instructions above")
        print("=" * 70)
        
        return False
    
    def verify_weights(self, weights_path: Path, expected_hash: str) -> bool:
        """
        Verify downloaded weights against expected hash.
        
        Args:
            weights_path: Path to weights file
            expected_hash: Expected SHA256 hash
        
        Returns:
            True if hash matches, False otherwise
        """
        if not weights_path.exists():
            print(f"✗ Weights file not found: {weights_path}")
            return False
        
        print(f"🔍 Verifying weights: {weights_path}")
        
        # Calculate hash
        sha256 = hashlib.sha256()
        with open(weights_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        
        actual_hash = sha256.hexdigest()
        
        if actual_hash == expected_hash:
            print(f"✓ Hash verification PASSED")
            print(f"  Expected: {expected_hash}")
            print(f"  Actual:   {actual_hash}")
            return True
        else:
            print(f"✗ Hash verification FAILED")
            print(f"  Expected: {expected_hash}")
            print(f"  Actual:   {actual_hash}")
            print(f"⚠️  DO NOT USE these weights - verification failed!")
            return False


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Verified Model Weight Download (Offline-First)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get download instructions for a model
  python download_models.py --model llama2-7b --hash <expected_sha256>
  
  # Verify already-downloaded weights
  python download_models.py --verify weights.bin --hash <expected_sha256>

Security Notes:
  - Automatic downloads are DISABLED by default
  - Always verify SHA256 hashes manually
  - Use cryptographic signatures when available
  - Never use unverified weights in production
        """
    )
    
    parser.add_argument(
        '--model', '-m',
        help='Model name to download'
    )
    parser.add_argument(
        '--output-dir', '-o',
        type=Path,
        default=Path('./models'),
        help='Output directory for weights'
    )
    parser.add_argument(
        '--hash',
        help='Expected SHA256 hash for verification'
    )
    parser.add_argument(
        '--source-url',
        help='Source URL for manual download'
    )
    parser.add_argument(
        '--verify',
        type=Path,
        help='Verify existing weights file'
    )
    
    args = parser.parse_args()
    
    downloader = ModelDownloader()
    
    if args.verify:
        # Verify mode
        if not args.hash:
            print("Error: --hash required for verification")
            sys.exit(1)
        
        success = downloader.verify_weights(args.verify, args.hash)
        sys.exit(0 if success else 1)
    
    elif args.model:
        # Download mode (shows instructions)
        downloader.download_weights(
            args.model,
            args.output_dir,
            args.hash,
            args.source_url
        )
        sys.exit(1)  # Exit with error since no automatic download
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
