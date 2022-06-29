import os, sys
import psycopg2 as pg

def verify_vars(**params):
    print('Verifying environment variables...')
    missing = False
    for i in params:
        if not params.get(i):
            missing = True
            print(f"Environment variable missing. {i} is not filled, value is {params[i]}")
    if missing:
        sys.stdout.flush()
        sys.exit(1)
    print('Environment variables well fullfilled.')

def config_vars():
    print('\nDatabase information: ')
    print(f"HOST:  {os.getenv('PG_HOST')}; PORT:  {os.getenv('PG_PORT')}; DB: {os.getenv('PG_INPE_DB')}")
    
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
    updated_at_trigger = (
        f"""
        CREATE OR REPLACE FUNCTION set_updated_at_field()
        RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = NOW();
                RETURN NEW;
            END; 
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER set_updated_at_field BEFORE UPDATE ON {table_name}
            FOR EACH ROW EXECUTE FUNCTION set_updated_at_field();
        """
    )
    sql = (
        f"""
        CREATE TABLE IF NOT EXISTS {table_name}(
            firerisks_id SERIAL PRIMARY KEY,
            id VARCHAR(100) UNIQUE NOT NULL,
            type VARCHAR(20) NOT NULL,
            geometry_name VARCHAR(20) NOT NULL,
            geometry VARCHAR(100) NOT NULL,
            properties TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )
    sql = sql + updated_at_trigger

    conn = None

    try:
        print("> Connection with firerisks database.")
        conn = pg.connect(**params)
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        print("> Table fire_outbreaks created.")
    except (Exception, pg.DatabaseError) as e:
        print("> Connection failed.")
        conn.rollback()
        cursor.close()
        raise print(e)
    finally:
        if conn is not None:
            conn.close()
        else:
            print("> Failed to connect.")
            sys.stdout.flush()
            sys.exit(1)
    
    print("> Connection closed with firerisks database.")

def upsert_firerisks_data(df):
    params = config_vars()
    data_tp = [tuple(i) for i in df.to_numpy()]
    data_col = ','.join(list(df.columns))
    data_tbl = os.getenv('PG_INPE_TABLE')
    sql = (
        f'''
        INSERT INTO {data_tbl}({data_col}) VALUES(%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            properties = EXCLUDED.properties
        '''
        )

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
        raise print(e)
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