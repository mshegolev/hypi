-- select data by uuid
SELECT DATA FROM INVOICE WHERE DATA ->> 'UUID' = '<UUID>';


-- check exists db
SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME= '<DBNAME>';

-- create table
CREATE TABLE INVOICE ( ID SERIAL PRIMARY KEY,DATA JSONB);




def is_exists_table(name):
    conn = psycopg2.connect(connect_str)
    cur = conn.cursor()
    querry = """select * from information_schema.tables where table_name='{}'""".format(name)
    print('QUERRY: '.format(querry))
    cur.execute(querry)
    print('RESPONSE: '.format(cur.rowcount))
    return cur