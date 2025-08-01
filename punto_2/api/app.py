from fastapi import FastAPI, Requests
from pydantic import BaseModel
from embeddings.index_movies import query_similar_movies
from utils.connector import generate_answer

app=FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post('/ask')
def ask_question(req: QuestionRequest):
    question=req.question
    context_docs=query_similar_movies(question)
    context_text='\n'.join([f"{r['title']}: {r['plot']}"] for r in context_docs)
    answer=generate_answer(context_text,question)
    return {'answer':answer}