"""Canonical JSON utilities for reproducible serialization."""
import json
from typing import Any, Dict


def canonicalize(obj: Any) -> str:
    """
    Convert Python object to canonical JSON string.
    
    Ensures deterministic output by:
    - Sorting dictionary keys
    - No extra whitespace
    - Consistent formatting
    
    Args:
        obj: Python object to serialize
        
    Returns:
        Canonical JSON string
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=True
    )


def parse_canonical(json_str: str) -> Any:
    """
    Parse canonical JSON string to Python object.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed Python object
    """
    return json.loads(json_str)


def verify_canonical(json_str: str) -> bool:
    """
    Verify that a JSON string is in canonical form.
    
    Args:
        json_str: JSON string to verify
        
    Returns:
        True if canonical, False otherwise
    """
    try:
        obj = parse_canonical(json_str)
        return canonicalize(obj) == json_str
    except (json.JSONDecodeError, TypeError):
        return False


def hash_canonical(obj: Any) -> str:
    """
    Generate deterministic hash of object via canonical JSON.
    
    Args:
        obj: Object to hash
        
    Returns:
        SHA256 hex digest
    """
    import hashlib
    canonical = canonicalize(obj)
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()
