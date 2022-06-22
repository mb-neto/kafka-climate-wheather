import os, sys
import psycopg2 as pg

def verify_vars(**params):
    print('Verifying environment variables...')
    missing = False
    for i in params:
        if params[i] == None or params[i] == ''
            missing = True
            print(f'Environment variable missing. {i} is not filled, value is {params[i]}')
    if missing:
        sys.stdout.flush()
        sys.exit()
    print('Environment variables well fullfilled.')

def config_vars(database='inpe'):
    db = (database == 'inpe') and os.environ['PG_INPE_DB'] or os.environ['PG_INMET_DB']

    print('\nDatabase information: ')
    print('HOST:  {} \n\
            PORT:  {} \n\
            DB: {}'
            .format(os.environ['PG_HOST'],os.environ['PG_PORT'], db))
    
    params = {
        'host': os.environ['PG_HOST'],
        'port': os.environ['PG_PORT'],
        'database': db,
        'user': os.environ['PG_USERNAME'],
        'password': os.environ['PG_PASSWORD']
    }

    verify_vars(**params)

    return params

def create_

def insert_firerisks_data(df):
    params = config_vars()
    data_tp = [tuple(i) for i in df.to_numpy()]
    data_col = ','.join(list(df.columns))
    sql = "INSERT INTO firerisks VALUES(%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)" % (data_col)

    conn = None

    try:
        print("Connection with firerisks database.")
        conn = pg.connect(**params)
        cursor = conn.cursor()
        print("Inserting data with dataframe.")
        cursor.executemany(sql, data_tp)
        conn.commit()
        print("Data inserted.")
        cursor.close()
    except (Exception, pg.DatabaseError) as e:
        print("Connection failed.")
        conn.rollback()
        cursor.close()
        print(e)
        sys.stdout.flush()
        sys.exit(1)
    finally:
        if is not None:
            conn.close()
        else:
            print("Failed to connect.")
            sys.stdout.flush()
            sys.exit(1)
    
    print("Connection closed with firerisks database.")