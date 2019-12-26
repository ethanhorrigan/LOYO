import sqlite3
conn = sqlite3.connect('fantasyleague.db')
c = conn.cursor()

c.execute('''CREATE TABLE PLAYERS([generated_id] INTEGER PRIMARY KEY,[Summoner_ID] integer,[Summoner_Name] text, [Rank] text, [Tier] integer, [League_MMR] integer, [MMR] integer, [Points] integer)''')

conn.commit()