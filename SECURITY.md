# Security Policy

## Overview

y.AI.y is designed with security as a core principle. This document outlines security best practices and policies.

## Core Security Principles

### 1. Offline-First Operation
- All components work without internet access
- External network communication is **disabled by default**
- Manual approval required for any network operations

### 2. Cryptographic Verification
- Ed25519 signatures for all critical data
- SHA256 hashing for integrity verification
- No automatic acceptance of unsigned data

### 3. Manual Approval Workflow
- All actions require explicit human approval
- No automatic execution of sensitive operations
- Policy engine enforces manual review

### 4. Key Management
- Private keys must be generated offline
- Keys stored with restrictive permissions (0600)
- Public keys can be shared for verification
- **Never commit private keys to version control**

## Best Practices

### Signing Keys

```bash
# Generate keys in a secure location
python -m yaiy.signer.cli generate --output-dir /secure/path/keys

# Verify key permissions
ls -la /secure/path/keys
# Should show: -rw------- for private.key

# Backup private key securely (offline)
cp /secure/path/keys/private.key /offline/backup/location/
```

### Model Weights

```bash
# Never use unverified weights
python scripts/download_models.py --verify weights.bin --hash <EXPECTED_HASH>

# Always verify signatures if provided
python -m yaiy.signer.cli verify \
  --public-key <TRUSTED_PUBLIC_KEY> \
  --signature <SIGNATURE> \
  --data weights.bin
```

### Ingot Validation

```python
# Always verify ingot signatures in production
from yaiy.mediator import app

# POST to /validate-ingot with signature and public_key
# Only use unsigned ingots for testing
```

### Policy Configuration

```python
from yaiy.policy import PolicyEngine, PolicyRule, RiskLevel

engine = PolicyEngine()

# Add strict rules for production
engine.add_rule(PolicyRule(
    name="production_strict",
    description="No auto-approval in production",
    risk_level=RiskLevel.CRITICAL,
    auto_approve=False  # Always require manual approval
))
```

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT open a public issue**
2. Email security concerns to: [CONTACT_EMAIL]
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

## Security Checklist

Before deploying y.AI.y:

- [ ] Private keys generated and secured offline
- [ ] All ingots are signed with verified keys
- [ ] Model weights verified against known hashes
- [ ] Network access disabled for sensitive operations
- [ ] Policy engine configured for manual approvals
- [ ] All team members trained on security procedures
- [ ] Backup and recovery procedures documented
- [ ] Logging and monitoring enabled
- [ ] Regular security audits scheduled

## Threat Model

### Protected Against
- ✅ Unauthorized code execution
- ✅ Tampering with ingots/configurations
- ✅ Use of unverified model weights
- ✅ Automatic approval of sensitive operations
- ✅ Man-in-the-middle attacks (offline operation)

### Out of Scope
- ❌ Physical access to systems
- ❌ Compromised operating system
- ❌ Social engineering attacks
- ❌ Side-channel attacks on cryptography

## Cryptographic Details

### Ed25519 Signing
- Algorithm: Ed25519 (RFC 8032)
- Key size: 256 bits
- Library: PyNaCl (libsodium)
- Purpose: Signing ingots and critical data

### SHA256 Hashing
- Algorithm: SHA-256
- Output size: 256 bits
- Purpose: Data integrity verification

### Canonical JSON
- Deterministic serialization
- Sorted keys
- No whitespace
- Purpose: Reproducible hashing

## Compliance

This framework is designed to support:
- Reproducibility requirements
- Audit trail maintenance
- Data integrity verification
- Principle of least privilege
- Defense in depth

## Updates

This security policy is reviewed quarterly and updated as needed.

**Last Updated:** 2024-01-01  
**Version:** 0.1.0

---

**Security is not a feature - it's a requirement.**
