import psycopg2


try:
    conn = psycopg2.connect(
            host = '198.251.66.139',
            user = 'postgres',
            password = '41eb9838f37947cd820249d7c4df4a26',
            database = 'bradexpenses',
            port = '13020'
        )
    cur = conn.cursor()
    create_table = """
                CREATE TABLE IF NOT EXISTS expenses (
                    id SERIAL PRIMARY KEY,
                    month VARCHAR (50) NOT NULL, 
                    concept VARCHAR (50) NOT NULL,
                    amount FLOAT (50) NOT NULL,
                    notes VARCHAR (50) NOT NULL
                )
                """
    cur.execute(create_table)
    conn.commit()
    print('conexión buena')
except Exception as error:
    print('ERROOOOOOOR')
