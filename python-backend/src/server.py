# python-backend/src/server.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.importer.import_engine import ImportEngine  # this expects python-backend/src/importer...
import os

app = FastAPI()
engine = ImportEngine()

class ImportReq(BaseModel):
    path: str

@app.post("/import")
def import_chat(req: ImportReq):
    # simple pass-through to your ImportEngine
    return engine.import_file(req.path)
