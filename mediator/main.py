from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import Dict, Any
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.canonicalize import canonicalize_json

app = FastAPI()

class IngestRequest(BaseModel):
    data: Dict[str, Any]
    ingot_id: str

@app.get("/")
def root():
    return {"status": "y.AI.y mediator running", "mode": "localhost-only"}

@app.post("/ingest")
def ingest(request: IngestRequest):
    try:
        canonical = canonicalize_json(request.data)
        ingot_path = Path("packet") / f"{request.ingot_id}_unsigned.json"
        ingot_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ingot_path, "w") as f:
            f.write(canonical)
        return {"status": "ingested", "path": str(ingot_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export_for_sign/{ingot_id}")
def export_for_sign(ingot_id: str):
    ingot_path = Path("packet") / f"{ingot_id}_unsigned.json"
    if not ingot_path.exists():
        raise HTTPException(status_code=404, detail="Ingot not found")
    with open(ingot_path, "r") as f:
        content = f.read()
    return {"ingot_id": ingot_id, "canonical_bytes": content, "note": "Sign offline, manual approval required"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
