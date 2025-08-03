import openai
import os

openai.api_key=os.getenv("OPENAI_API_KEY")

def get_embedding(texto):
    res=openai.Embedding.create(
        input=texto,
        model='text-embedding-3-small'
    )
    return res['data'][0]['embedding']

def gen_answer(contexto, pregunta):
    prompt=f'''
Usa la siguiente información sobre películas de los años 80 para responder la pregunta. Si te preguntan por la imagen responde con la ULR de wikimedia.

Contexto:
{contexto}

Pregunta:
{pregunta}
'''
    res=openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{'role':'user',
                   'content':prompt}]
    )
    return res['choices'][0]['message']['content']


# print(get_embedding('¿Cuál es el nombre de la película, donde los humanos y las IA’s coexisten y tienen una batallapor el control de la realidad?'))