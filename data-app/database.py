import os, sys
import psycopg2 as pg

def verify_vars(**params):
    print('Verifying environment variables...')
    missing = False
    for i in params:
        if params[i] == None or params[i] == '':
            missing = True
            print(f'Environment variable missing. {i} is not filled, value is {params[i]}')
    if missing:
        sys.stdout.flush()
        sys.exit(1)
    print('Environment variables well fullfilled.')

def config_vars():
    print('\nDatabase information: ')
    print('HOST:  {}; PORT:  {}; DB: {}'
    .format(
        os.getenv('PG_HOST'), 
        os.getenv('PG_PORT'), 
        os.getenv('PG_INPE_DB')
        )
    )
    
    params = {
        'host': os.getenv('PG_HOST'),
        'port': os.getenv('PG_PORT'),
        'database': os.getenv('PG_INPE_DB'),
        'user': os.getenv('PG_USERNAME'),
        'password': os.getenv('PG_PASSWORD')
    }

    verify_vars(**params)

    return params

def create_fire_outbreaks_table():
    params = config_vars()
    table_name = os.getenv('PG_INPE_TABLE')
    sql = (
        """
        CREATE TABLE IF NOT EXISTS {}(
            id VARCHAR(100) NOT NULL,
            type VARCHAR(20) NOT NULL,
            geometry_name VARCHAR(20) NOT NULL,
            geometry VARCHAR(100) NOT NULL,
            properties TEXT NOT NULL
        )
        """.format(table_name)
    )

    conn = None

    try:
        print("> Connection with firerisks database.")
        conn = pg.connect(**params)
        cursor = conn.cursor()
        print("> Inserting data with dataframe.")
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        print("> Table created.")
    except (Exception, pg.DatabaseError) as e:
        print("> Connection failed.")
        conn.rollback()
        cursor.close()
        print(e)
        sys.stdout.flush()
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
        else:
            print("> Failed to connect.")
            sys.stdout.flush()
            sys.exit(1)
    
    print("> Connection closed with firerisks database.")

def insert_firerisks_data(df):
    params = config_vars()
    data_tp = [tuple(i) for i in df.to_numpy()]
    data_col = ','.join(list(df.columns))
    data_tbl = os.getenv('PG_INPE_TABLE')
    sql = "INSERT INTO %s(%s) VALUES(%%s, %%s, %%s, %%s, %%s)" % (data_tbl, data_col)

    conn = None

    try:
        print("> Connection with firerisks database.")
        conn = pg.connect(**params)
        cursor = conn.cursor()
        print("> Inserting data with dataframe.")
        cursor.executemany(sql, data_tp)
        cursor.close()
        print("> Data inserted.")
        conn.commit()
    except (Exception, pg.DatabaseError) as e:
        print("> Connection failed.")
        conn.rollback()
        cursor.close()
        print(e)
        sys.stdout.flush()
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
        else:
            print("> Failed to connect.")
            sys.stdout.flush()
            sys.exit(1)
    
    print("> Connection closed with firerisks database.")

if __name__ == '__main__':
    create_fire_outbreaks_table()