import psycopg2
from embedding import get_embedding
import pandas as pd

connection=psycopg2.connect(
    # host='localhost',
    host='movies.cqf44we820b0.us-east-1.rds.amazonaws.com',
    port=5432,
    user='postgres',
    password='c0ntr453n4',
    database='postgres'
)
cur=connection.cursor()
data=pd.read_csv('movies-dataset.csv')


def init_db(data=data):
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
size=cur.fetchall()
print(size)

try:
    init_db() if size[0,0]==0 else None
except:
    pass

# text=f"{data.iloc[0,0]} - {data.iloc[0,1]} : {data.iloc[0,2]}"
# emb=get_embedding(text)
# print(f'{text}\n{emb}')

# )
# cur.execute(
#         """INSERT INTO movies (title, plot, image, embedding) VALUES (%s, %s, %s, %s)""",
#         (data.iloc[0,0], data.iloc[0,1], data.iloc[0,2], emb)
# )
connection.commit()
cur.close()
connection.close()