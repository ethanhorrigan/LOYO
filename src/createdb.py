import sqlite3
conn = sqlite3.connect('fantasyleague.db')
c = conn.cursor()

# c.execute('''DROP TABLE Users''')
# c.execute('''CREATE TABLE Users([generated_id] INTEGER PRIMARY KEY,[username] text,[summonerName] text, [password] text, [token] integer)''')
# c.execute('''INSERT INTO Users (username, summonerName, password, token)
# VALUES('Ethanhorro', 'Yupouvit', 'ethan123', 'fake_token_123')''')


# c.execute('''DROP TABLE PLAYERS''')
# c.execute('''
# CREATE TABLE Players(
#     [generated_id] INTEGER PRIMARY KEY, 
#     [summonerName] text, 
#     [rank] text, 
#     [tier] integer,
#     [mmr] integer,
#     [wins] integer,
#     [losses] integer,
#     [gamesPlayed] integer,
#     [primaryRole] text,
#     [secondaryRole] text
#     )
#     ''')

# c.execute('''
# INSERT INTO Players 
# (summonerName, rank, tier, mmr, wins, losses, gamesPlayed, primaryRole, secondaryRole)
# VALUES
# ('Tommy Shlug', 'Silver', '4', '1220', 0, 0, 0, 'Top', 'ADC')''')

# c.execute('''
# INSERT INTO Players 
# (summonerName, rank, tier, mmr, wins, losses, gamesPlayed, primaryRole, secondaryRole)
# VALUES
# ('Communism', 'Platinum', '4', '1920', 0, 0, 0, 'Top', 'Mid')''')

# c.execute('''
# INSERT INTO Players 
# (summonerName, rank, tier, mmr, wins, losses, gamesPlayed, primaryRole, secondaryRole)
# VALUES
# ('Thrasius123', 'Silver', '3', '1290', 0, 0, 0, 'Mid', 'ADC')''')

# c.execute('''
# INSERT INTO Players 
# (summonerName, rank, tier, mmr, wins, losses, gamesPlayed, primaryRole, secondaryRole)
# VALUES
# ('Zethose', 'Silver', '2', '1360', 0, 0, 0, 'Support', 'ADC')''')

c.execute('''DROP TABLE IF EXISTS Lobby''')
c.execute('''CREATE TABLE Lobby([generated_id] INTEGER PRIMARY KEY,[username] text, [summonerName] text)''')
conn.commit()