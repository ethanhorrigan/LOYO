import sqlite3
conn = sqlite3.connect('fantasyleague.db')
c = conn.cursor()

c.execute('''CREATE TABLE Users([generated_id] INTEGER PRIMARY KEY,[firstName] test,[lastName] text, [username] text, [password] text)''')
      
conn.commit()