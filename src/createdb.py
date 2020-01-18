import sqlite3
conn = sqlite3.connect('fantasyleague.db')
c = conn.cursor()

# c.execute('''CREATE TABLE PLAYERS([generated_id] INTEGER PRIMARY KEY,[Summoner_ID] integer,[Summoner_Name] text, [Rank] text, [Tier] integer, [League_MMR] integer, [MMR] integer, [Points] integer)''')

c.execute('''DELETE FROM PLAYERS WHERE Summoner_ID = 1 ''')


c.execute('''INSERT INTO PLAYERS(Summoner_ID, Summoner_Name, Rank, Tier, League_MMR, MMR, Points)
            VALUES(1, 'Horro', 'PLATINUM', 4, 1500, 1500, 100)''')
c.execute('''INSERT INTO PLAYERS(Summoner_ID, Summoner_Name, Rank, Tier, League_MMR, MMR, Points)
            VALUES(2, 'Horro2', 'PLATINUM', 4, 1500, 1500, 100)''')
c.execute('''INSERT INTO PLAYERS(Summoner_ID, Summoner_Name, Rank, Tier, League_MMR, MMR, Points)
            VALUES(3, 'Horro3', 'PLATINUM', 4, 1500, 1500, 100)''')
c.execute('''INSERT INTO PLAYERS(Summoner_ID, Summoner_Name, Rank, Tier, League_MMR, MMR, Points)
            VALUES(4, 'Horro4', 'PLATINUM', 4, 1500, 1500, 100)''')
c.execute('''INSERT INTO PLAYERS(Summoner_ID, Summoner_Name, Rank, Tier, League_MMR, MMR, Points)
            VALUES(5, 'Horro5', 'PLATINUM', 4, 1500, 1500, 100)''')
c.execute('''INSERT INTO PLAYERS(Summoner_ID, Summoner_Name, Rank, Tier, League_MMR, MMR, Points)
            VALUES(6, 'Horro6', 'PLATINUM', 4, 1500, 1500, 100)''')           
conn.commit()