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







LINE 2:         insert into invoice ( data ) VALUES ('{"ptl": 1, "uu...
                                                     ^
DETAIL:  Token "None" is invalid.
CONTEXT:  JSON data, line 1: ...52e67-26a4-4ec4-a89d-042bc8bb2ff5", "error": None...
{'ptl': 1, 'uuid': '0cdce5a5-3c2f-4537-92ae-a9b08a544df0', 'error': None, 'status': 'done', 'payload': {'total': 175, 'f
ns_site': 'https://www.nalog.ru/rn77/', 'fn_number': '9999078900003959', 'shift_number': 8, 'receipt_datetime': '21.03.2
018 12:50:00', 'fiscal_receipt_number': 19, 'fiscal_document_number': 35, 'ecr_registration_number': '1234567890020854',
 'fiscal_document_attribute': 4286911692}, 'timestamp': '21.03.2018 12:50:14', 'group_code': 'zemkov_1_05', 'daemon_code
': 'test_agent', 'device_code': 'KSR13.1-1-40', 'external_id': '2018-03-21 12:50:09.506442848312972714177303343284171054
5.8841677', 'callback_url': 'http://localhost:5000/receiver'}
127.0.0.1 - - [21/Mar/2018 12:50:17] "POST /receiver HTTP/1.1" 500 -
Traceback (most recent call last):
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\app.py", line 1997, in
__call__
    return self.wsgi_app(environ, start_response)
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\app.py", line 1985, in
wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\app.py", line 1540, in
handle_exception
    reraise(exc_type, exc_value, tb)
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\_compat.py", line 33, i
n reraise
    raise value
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\app.py", line 1982, in
wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\app.py", line 1614, in
full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\app.py", line 1517, in
handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\_compat.py", line 33, i
n reraise
    raise value
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\app.py", line 1612, in
full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\lib\site-packages\flask\app.py", line 1598, in
dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "C:\hypi2.py", line 44, in insert_invoice
    """.format(data.__format__("").replace("'", "\"")))
psycopg2.DataError: invalid input syntax for type json
LINE 2:         insert into invoice ( data ) VALUES ('{"ptl": 1, "uu...
                                                     ^
DETAIL:  Token "None" is invalid.
CONTEXT:  JSON data, line 1: ...ce5a5-3c2f-4537-92ae-a9b08a544df0", "error": None...
