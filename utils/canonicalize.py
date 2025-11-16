import json
from typing import Any

def canonicalize_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def canonicalize_bytes(data: Any) -> bytes:
    return canonicalize_json(data).encode('utf-8')

def load_canonical(filepath: str) -> Any:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
