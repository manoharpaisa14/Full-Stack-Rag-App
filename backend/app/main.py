from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils.auth import get_current_user
from app.utils.minio import upload_to_minio
from app.utils.parser import parse_document
from app.utils.elasticsearch import index_document
from app.utils.redis import save_metadata
from app.utils.jwt import create_access_token
from app.api import auth
from app.services.rag_agent import get_answer_from_documents  # ✅ NEW

import uvicorn

app = FastAPI()
app.include_router(auth.router)

# Enable CORS for frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Doc RAG API!"}

@app.post("/upload")
async def upload(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    content = await file.read()
    text, metadata = parse_document(content, file.filename)
    file_id = upload_to_minio(file.filename, content)
    save_metadata(file_id, metadata)
    index_document(file_id, text)
    return {"message": "Upload successful", "file_id": file_id}

@app.get("/ask")
def ask(q: str, user: str = Depends(get_current_user)):
    answer = get_answer_from_documents(q)  # ✅ Use full Gemini RAG pipeline
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
