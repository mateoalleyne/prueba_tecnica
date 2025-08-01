import openai
import os

openai.api_key='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'

def embedding(texto):
    res=openai.Embedding.create(
        input=texto,
        model='text-embedding-3-small'
    )
    return res['data'][0]['embedding']

def gen_answer(contexto, pregunta):
    prompt=f'''
Usa la siguiente información sobre películas de los años 80 para responder la pregunta.

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