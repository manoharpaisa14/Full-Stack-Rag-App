from fastapi import APIRouter, Query
from app.services.rag_agent import get_answer_from_documents

router = APIRouter()

@router.get("/ask")
def ask_question(q: str = Query(...)):
    answer = get_answer_from_documents(q)
    print("QUESTION:", q)
    print("ANSWER:", answer)
    return {"question": q, "answer": answer}
