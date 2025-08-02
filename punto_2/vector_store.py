from embedding import get_embedding
import psycopg2
import psycopg2.extras

def query_similar_movies(question,top_k=3):
    embedding = get_embedding(question)

    connection=psycopg2.connect(
        # host='localhost',
        host='movies.cqf44we820b0.us-east-1.rds.amazonaws.com',
        port=5432,
        user='postgres',
        password='c0ntr453n4',
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
