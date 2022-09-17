import psycopg2
import glob
import os

connection = psycopg2.connect(
    database="telegram_my_messages", user='postgres', password='3228', host='127.0.0.1', port='5432'
)

connection.autocommit = True
cursor = connection.cursor()


for filename in glob.glob('sql/*.sql'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        text = f.name
        print("starting execution: ", f.name)
        command = open(f.name, "r").read()
        print(command)
        cursor.execute(command)