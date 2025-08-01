import psycopg2
import openai
from embedding import get_embedding
import pandas as pd

connection=psycopg2.connect(
    host='localhost',
    user='postgres',
    password='luisma129',
    database='movies'
)
cur=connection.cursor()

data=pd.read_csv('movies-dataset.csv')
for i,row in data.iterrows():
    text=f"{row['title']} - {row['image']} : {row['plot']}"
    print(row['title'])
    emb=get_embedding(text)
    cur.execute(
        """INSERT INTO movies (title, plot, image, embedding) VALUES (%s, %s, %s, %s)""",
        (row['title'], row['plot'], row['image'], emb)
    )

# text=f"{data.iloc[0,0]} - {data.iloc[0,1]} : {data.iloc[0,2]}"
# # emb=get_embedding(text)
# print(f'{text}\n{emb}')
# cur.execute(
#         """INSERT INTO movies (title, plot, image, embedding) VALUES (%s, %s, %s, %s)""",
#         (data.iloc[0,0], data.iloc[0,1], data.iloc[0,2], emb)
# )
connection.commit()
cur.close()
connection.close()