from embedding import get_embedding
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def query_similar_movies(question,top_k=3):
    embedding = get_embedding(question)

    connection=psycopg2.connect(
        # host='localhost',
        host='movies.cqf44we820b0.us-east-1.rds.amazonaws.com',
        port=5432,
        user='postgres',
        password=os.getenv('BD_PASSWORD'),
        database='postgres'
    )
    cur=connection.cursor()

    cur.execute("""
        SELECT title, plot, image
        FROM movies
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
    """, (embedding, top_k))
    results = cur.fetchall()
    cur.close()
    connection.close()
    return results
