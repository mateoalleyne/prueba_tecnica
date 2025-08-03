import psycopg2
from embedding import get_embedding
import pandas as pd
import os

connection=psycopg2.connect(
    # host='localhost',
    host='movies.cqf44we820b0.us-east-1.rds.amazonaws.com',
    port=5432,
    user='postgres',
    password='c0ntr453n4',
    database=os.getenv("DB_PASSWORD")
)
cur=connection.cursor()
data=pd.read_csv('movies-dataset.csv')


def init_db(cur=cur,data=data):
    cur.execute(
    """
    CREATE EXTENSION IF NOT EXISTS vector;

    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        title TEXT,
        plot TEXT,
        image TEXT,
        embedding VECTOR(1536)
    );
    """)
    for i,row in data.iterrows():
        text=f"{row['title']} - {row['image']} : {row['plot']}"
        print(row['title'])
        emb=get_embedding(text)
        cur.execute(
            """INSERT INTO movies (title, plot, image, embedding) VALUES (%s, %s, %s, %s)""",
            (row['title'], row['plot'], row['image'], emb)
        )

cur.execute("SELECT COUNT(1) FROM movies")
size=0
try: 
    size=cur.fetchall()[0][0]
except:
    pass
print(f'SIZE OF TABLE: {size}')

init_db() if size == 0 else None

connection.commit()
cur.close()
connection.close()