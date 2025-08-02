from fastapi import FastAPI, Request
from vector_store import query_similar_movies
from embedding import gen_answer
import streamlit as st
app = FastAPI()

@app.post("/ask")
def ask_question(question):
    context_docs = query_similar_movies(question)
    context_text = "\n".join([f"{r[0]}: {r[1]}" for r in context_docs])
    answer = gen_answer(context_text, question)
    return {"answer": answer}


# print(ask_question("¿Cuál es el nombre de la película, donde los humanos y las IA’s coexisten y tienen una batalla por el control de la realidad?"))
# print(ask_question("¿En qué consiste la película Echoes of Tomorrow? Muestre la respuesta indicando el contextode la pregunta. Ejemplo: Esta película consiste en…"))
# print(ask_question("Muestre la imagen relacionada a la película Stellar Odyssey"))
# print(ask_question("En la película Enigma cual es el nombre del protagonista y quien interpreta al agente de la CIA."))

st.set_page_config('Reto Técnico IA')
st.header('Preguntas de Películas')

user_question = st.text_input("Pregunta: ")
if user_question:
    respuesta=ask_question(user_question)
    st.write(respuesta['answer'])