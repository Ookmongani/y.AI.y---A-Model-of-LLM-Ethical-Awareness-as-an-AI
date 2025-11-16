"""Tests for canonical JSON utilities."""
import pytest
from yaiy.utils.canonical_json import (
    canonicalize,
    parse_canonical,
    verify_canonical,
    hash_canonical
)


def test_canonicalize_dict():
    """Test dictionary canonicalization."""
    obj = {"b": 2, "a": 1, "c": 3}
    result = canonicalize(obj)
    assert result == '{"a":1,"b":2,"c":3}'


def test_canonicalize_nested():
    """Test nested structure canonicalization."""
    obj = {"outer": {"z": 3, "a": 1}, "inner": [2, 1]}
    result = canonicalize(obj)
    assert result == '{"inner":[2,1],"outer":{"a":1,"z":3}}'


def test_parse_canonical():
    """Test parsing canonical JSON."""
    json_str = '{"a":1,"b":2}'
    result = parse_canonical(json_str)
    assert result == {"a": 1, "b": 2}


def test_verify_canonical_valid():
    """Test verification of valid canonical JSON."""
    canonical = '{"a":1,"b":2}'
    assert verify_canonical(canonical) is True


def test_verify_canonical_invalid():
    """Test verification of non-canonical JSON."""
    non_canonical = '{"b": 2, "a": 1}'  # Has spaces
    assert verify_canonical(non_canonical) is False


def test_hash_canonical_deterministic():
    """Test that hashing is deterministic."""
    obj1 = {"b": 2, "a": 1}
    obj2 = {"a": 1, "b": 2}
    
    hash1 = hash_canonical(obj1)
    hash2 = hash_canonical(obj2)
    
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 hex length


def test_hash_canonical_different():
    """Test that different objects have different hashes."""
    obj1 = {"a": 1, "b": 2}
    obj2 = {"a": 1, "b": 3}
    
    hash1 = hash_canonical(obj1)
    hash2 = hash_canonical(obj2)
    
    assert hash1 != hash2
