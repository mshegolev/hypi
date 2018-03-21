#!flask/bin/python
import json

import psycopg2
from flask import Flask, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth
from psycopg2.extras import RealDictCursor

connect_str = "dbname='hyperion' user='hyperion' host='localhost' " + \
              "password='hyperion'"
app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'atolonline':
        return 'atolonline'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.route('/invoices', methods=['GET'])
@auth.login_required
def get_invoices():
    conn = psycopg2.connect(connect_str)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT
        id,data
        FROM invoice
        LIMIT 100
    """)

    return jsonify({'result': json.dumps(cur.fetchall(), indent=2)}), 200


#   curl -i -H "Content-Type: application/json" -X POST -d '{"data": {"uuid":"sldfkj-lasdfj-lsdfj-lsdjf", "foo": "bar"}}'
#   http://localhost:5000/receiver
@app.route('/receiver', methods=['POST'])
@auth.login_required
def insert_invoice():
    if not request.json or not 'data' in request.json:
        abort(400)
    data = {
        'data': request.json['data']
    }
    conn = psycopg2.connect(connect_str)
    cur = conn.cursor()
    cur.execute("""
        insert into invoice ( data ) VALUES ('{}');
    """.format(data.__format__("").replace("'", "\"")))
    conn.commit()
    conn.close()
    return jsonify({'result': data}), 201


@app.route('/invoices/<string:uuid>', methods=['GET'])
@auth.login_required
def get_invoice_by_uuid(uuid):
    conn = psycopg2.connect(connect_str)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select data from invoice where data #> '{data,uuid}'='\"" + uuid + "\"';")
    return jsonify({'result': json.dumps(cur.fetchall(), indent=2)}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)
