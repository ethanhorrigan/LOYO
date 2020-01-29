import sqlite3
conn = sqlite3.connect('fantasyleague.db')
c = conn.cursor()

c.execute('''DROP TABLE Users''')
c.execute('''CREATE TABLE Users([generated_id] INTEGER PRIMARY KEY,[username] text,[summonerName] text, [password] text, [token] integer)''')
c.execute('''INSERT INTO Users (username, summonerName, password, token)
VALUES('Ethanhorro', 'Yupouvit', 'ethan123', 'fake_token_123')''')
      
conn.commit()