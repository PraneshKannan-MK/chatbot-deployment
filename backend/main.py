from fastapi import FastAPI
from pydantic import BaseModel
import logging
import traceback
import threading

from backend.rag import hybrid_retrieve
from backend.prompt import build_prompt
from backend.llm import llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 🔒 GLOBAL LOCK — THIS IS THE KEY FIX
llm_lock = threading.Lock()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        logger.info(f"Incoming question: {req.question}")

        docs = hybrid_retrieve(req.question)
        logger.info(f"Retrieved {len(docs)} documents")

        prompt = build_prompt(docs, req.question)
        logger.info(f"Prompt length: {len(prompt)}")

        # 🔒 SERIALIZE LLM ACCESS
        with llm_lock:
            answer = llm.invoke(prompt)

        if not answer or not answer.strip():
            answer = "I do not know based on the provided context."

        logger.info(f"Answer length: {len(answer)}")
        return {"answer": answer}

    except Exception:
        logger.error("Chat endpoint crashed")
        logger.error(traceback.format_exc())
        return {
            "answer": "Internal error occurred while generating the answer."
        }