import sqlite3

# create table

conn = sqlite3.connect('WorkUADB.db')
c = conn.cursor()

query = '''create table workua
             (title text,
             company text,
             conditions text,
             salary text,
             job_description text);
'''

c.execute(query)
conn.commit()







