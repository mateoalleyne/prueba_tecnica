import openai

openai.api_key='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'

def get_embedding(texto):
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


# print(get_embedding('¿Cuál es el nombre de la película, donde los humanos y las IA’s coexisten y tienen una batallapor el control de la realidad?'))