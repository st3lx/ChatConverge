from fastapi import FastAPI
from pydantic import BaseModel
from src.importer.engine import ImportEngine

app = FastAPI()
engine = ImportEngine()

class ImportRequest(BaseModel):
    path: str

@app.post("/import")
def import_chat(req: ImportRequest):
    return engine.import_file(req.path)
