from psycopg2 import connect, extensions, sql

# declare a new PostgreSQL connection object
conn = connect(
dbname = "loyo_db",
user = "postgres",
host = "localhost",
password = "horrigan902"
)

# object type: psycopg2.extensions.connection
print ("\ntype(conn):", type(conn))

# string for the new database name to be created
DB_NAME = "loyo_db"

# get the isolation leve for autocommit
autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
print ("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)

"""
ISOLATION LEVELS for psycopg2
0 = READ UNCOMMITTED
1 = READ COMMITTED
2 = REPEATABLE READ
3 = SERIALIZABLE
4 = DEFAULT
"""

# set the isolation level for the connection's cursors
# will raise ActiveSqlTransaction exception otherwise
conn.set_isolation_level( autocommit )

# instantiate a cursor object from the connection
cursor = conn.cursor()

# use the execute() method to make a SQL request
#cursor.execute('CREATE DATABASE ' + str(DB_NAME))

# use the sql module instead to avoid SQL injection attacks
cursor.execute(sql.SQL(
"CREATE DATABASE {}"
).format(sql.Identifier( DB_NAME )))

# close the cursor to avoid memory leaks
cursor.close()

# close the connection to avoid memory leaks
conn.close()