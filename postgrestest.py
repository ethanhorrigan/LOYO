import psycopg2
from psycopg2 import Error

try:
    # dsn=None, connection_factory=None, cursor_factory=None, **kwargs
    connection = psycopg2.connect(user = "postgres", password = "horrigan902", host = "127.0.0.1", port ="5432", database = "loyo_db")
    cursor = connection.cursor()

    # print(connection.get_dsn_parameteres())
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
    

    # Inserting into a postrgresDB
    query = """ INSERT INTO Users (summoner_name, user_name, password, rank, tier, mmr, wins, losses, primary_role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = ('Yupouvit', 'Ethan', 'test123', 'PLATINUM', 4, 1700, 0, 0, 'Top')

    cursor.execute(query, values)
    connection.commit()
    
except (Exception, psycopg2.Error) as error:
    print ("Error while connecting to PostgreSQL", error)
# finally:
#     if(connection):
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")