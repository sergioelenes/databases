import os
import psycopg2

conn = psycopg2.connect(
        host="198.251.66.139:13020",
        database="bradexpenses",
        user='postgresql',
        password='41eb9838f37947cd820249d7c4df4a26')

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS expenses;')
cur.execute('CREATE TABLE expenses (id serial PRIMARY KEY,'
                                 'month varchar (150) NOT NULL,'
                                 'concept varchar (50) NOT NULL,'
                                 'amount integer NOT NULL,'
                                 'notes varchar (150) NOT NULL,'
                                 )

# Insert data into the table


conn.commit()

cur.close()
conn.close()
